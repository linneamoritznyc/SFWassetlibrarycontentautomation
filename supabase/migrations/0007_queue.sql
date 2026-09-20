-- The queue. Every automation in this system is a row here. Workers pull jobs;
-- nothing calls a worker directly. Backend spec section 4.6.

create table jobs (
  id           bigint generated always as identity primary key,
  type         text not null,
  payload      jsonb not null default '{}'::jsonb,
  priority     integer not null default 5,
  status       text not null default 'queued'
               check (status in ('queued', 'running', 'done', 'failed', 'dead')),
  attempts     integer not null default 0,
  max_attempts integer not null default 3,
  run_after    timestamptz not null default now(),
  error        text,
  dedupe_key   text,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

-- The claim query's index: queued jobs that are due, best first.
create index jobs_claimable_idx
  on jobs (priority, created_at)
  where status = 'queued';

create index jobs_type_idx   on jobs (type);
create index jobs_dead_idx   on jobs (updated_at desc) where status = 'dead';

-- A dedupe key blocks a duplicate only while the job is still live. Once it is
-- done, failed or dead the same key can be enqueued again, which is what makes
-- "re-tag this asset" and the Errors view's retry button work. The spec writes
-- this as a plain unique column; a plain unique would mean each key could ever
-- be used once, for the lifetime of the database.
create unique index jobs_dedupe_live_idx
  on jobs (dedupe_key)
  where dedupe_key is not null and status in ('queued', 'running');

create trigger jobs_set_updated_at
  before update on jobs
  for each row execute function set_updated_at();

-- Claim up to `lim` due jobs of the given types and mark them running.
-- SKIP LOCKED so several workers can poll the same types without blocking
-- each other or handing the same job to two of them.
create or replace function claim_job(types text[], lim integer default 1)
returns setof jobs
language sql
volatile
as $$
  update jobs
  set status = 'running',
      attempts = attempts + 1,
      updated_at = now()
  where id in (
    select id
    from jobs
    where status = 'queued'
      and run_after <= now()
      and type = any (types)
    order by priority, created_at
    for update skip locked
    limit greatest(lim, 1)
  )
  returning *;
$$;

comment on function claim_job(text[], integer) is
  'Claim due jobs of these types. Increments attempts on claim, so a worker '
  'that dies mid-job still burns an attempt and cannot loop forever.';

create or replace function complete_job(job_id bigint)
returns jobs
language sql
volatile
as $$
  update jobs
  set status = 'done',
      error = null,
      updated_at = now()
  where id = job_id
  returning *;
$$;

-- Exponential backoff: 2^attempts minutes. attempts was already incremented on
-- claim, so the first failure waits 2 minutes, the second 4, the third 8.
-- Once attempts reaches max_attempts the job is dead and shows up in the
-- Errors view with a retry button.
create or replace function fail_job(job_id bigint, err text)
returns jobs
language sql
volatile
as $$
  update jobs
  set status = case when attempts >= max_attempts then 'dead' else 'queued' end,
      run_after = case
                    when attempts >= max_attempts then run_after
                    else now() + (power(2, attempts) * interval '1 minute')
                  end,
      error = err,
      updated_at = now()
  where id = job_id
  returning *;
$$;

-- Retry button in the Errors view: put a dead job back on the queue with a
-- fresh budget. If something has already re-enqueued the same dedupe key since
-- this one died, there is nothing to do and the dead row is left alone: the
-- live job is the retry.
create or replace function retry_job(job_id bigint)
returns jobs
language sql
volatile
as $$
  update jobs j
  set status = 'queued',
      attempts = 0,
      run_after = now(),
      error = null,
      updated_at = now()
  where j.id = job_id
    and j.status in ('dead', 'failed')
    and not exists (
      select 1
      from jobs live
      where live.dedupe_key is not null
        and live.dedupe_key = j.dedupe_key
        and live.status in ('queued', 'running')
    )
  returning *;
$$;
