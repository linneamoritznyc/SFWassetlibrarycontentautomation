-- Row Level Security on every table, with no policies on any of them.
--
-- That is deliberate, and it is the whole access model (backend spec section 9).
-- Supabase's service_role bypasses RLS; anon and authenticated do not. With RLS
-- on and zero policies, a key that ever reaches a browser can read nothing and
-- write nothing, and every read and write has to go through an API route
-- holding the service role key server-side. Auth still happens in front of the
-- app: Supabase magic link, allowlisted by APP_ALLOWLIST.
--
-- The grants are revoked as well as RLS enabled, so the answer is "no" twice.

do $$
declare
  t text;
begin
  for t in
    select tablename from pg_tables where schemaname = 'public'
  loop
    execute format('alter table public.%I enable row level security', t);
    execute format('alter table public.%I force row level security', t);
  end loop;
end;
$$;

do $$
declare
  r text;
begin
  -- These roles exist on Supabase and not on a plain Postgres, so this is a
  -- no-op when the migrations are applied to a local test database.
  foreach r in array array['anon', 'authenticated']
  loop
    if exists (select 1 from pg_roles where rolname = r) then
      execute format('revoke all on all tables in schema public from %I', r);
      execute format('revoke all on all sequences in schema public from %I', r);
      execute format('revoke all on all functions in schema public from %I', r);
      execute format(
        'alter default privileges in schema public revoke all on tables from %I', r);
      execute format(
        'alter default privileges in schema public revoke all on sequences from %I', r);
    end if;
  end loop;
end;
$$;

-- The queue functions run as the caller, so only the service role reaches them.
do $$
declare
  r text;
  f text;
begin
  foreach r in array array['anon', 'authenticated']
  loop
    if exists (select 1 from pg_roles where rolname = r) then
      foreach f in array array[
        'claim_job(text[], integer)',
        'complete_job(bigint)',
        'fail_job(bigint, text)',
        'retry_job(bigint)',
        'enqueue_job(text, jsonb, integer, text, timestamptz)'
      ]
      loop
        execute format('revoke all on function %s from %I', f, r);
      end loop;
    end if;
  end loop;
end;
$$;
