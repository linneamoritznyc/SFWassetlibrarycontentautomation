-- Event triggers from backend spec section 5 that belong in the database
-- rather than in an API route.

-- Enqueue a job without caring whether an identical one is already waiting.
create or replace function enqueue_job(
  job_type text,
  job_payload jsonb default '{}'::jsonb,
  job_priority integer default 5,
  job_dedupe_key text default null,
  job_run_after timestamptz default now()
)
returns bigint
language plpgsql
as $$
declare
  new_id bigint;
begin
  insert into jobs (type, payload, priority, dedupe_key, run_after)
  values (job_type, job_payload, job_priority, job_dedupe_key, job_run_after)
  on conflict do nothing
  returning id into new_id;

  -- Already queued or running under the same key: hand back the live one.
  if new_id is null and job_dedupe_key is not null then
    select id into new_id
    from jobs
    where dedupe_key = job_dedupe_key and status in ('queued', 'running')
    limit 1;
  end if;

  return new_id;
end;
$$;

-- Asset status moves to 'tagged' -> embed it.
create or replace function on_asset_tagged() returns trigger
language plpgsql
as $$
begin
  if new.status = 'tagged' and (tg_op = 'INSERT' or old.status is distinct from 'tagged') then
    perform enqueue_job(
      'embed',
      jsonb_build_object('asset_id', new.id),
      5,
      'embed:' || new.id::text
    );
  end if;
  return new;
end;
$$;

create trigger assets_tagged_enqueues_embed
  after insert or update of status on assets
  for each row execute function on_asset_tagged();
