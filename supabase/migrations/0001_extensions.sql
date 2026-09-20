-- Extensions. pgvector for meaning search over assets, facts and news items.
-- pgcrypto for gen_random_uuid() and for encrypting the Canva tokens at rest
-- (backend spec section 9).
create extension if not exists vector;
create extension if not exists pgcrypto;

-- Every table with an updated_at column uses this.
create or replace function set_updated_at() returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;
