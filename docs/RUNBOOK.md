# Runbook

Operating the system. Filled in as phases land.

## Local development

```bash
cp .env.example .env.local     # then fill in the keys
pnpm install
pnpm build
pnpm dev                       # web on http://localhost:3000, workers polling
```

## Database

```bash
pnpm db:setup      # apply migrations, then seed. Safe to re-run.
pnpm db:migrate    # migrations only
pnpm db:seed       # seed only
```

Migrations are recorded in `schema_migrations` and each runs once, inside a
transaction. The seed upserts by natural key and never deletes, so a tag added
by hand and an email filled in by hand both survive a re-seed.

A prompt is activated by the seed only the first time its name is seen. A new
version of an existing prompt arrives inactive and has to pass the test set
before it goes live.

## Running the tests with a database

The schema and queue tests build their own throwaway databases. They need a
Postgres with `vector` and `pgcrypto`, and a user that can create databases.

```bash
# Ubuntu
apt-get install -y postgresql-16 postgresql-16-pgvector

TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5432/postgres pnpm test
```

Without `TEST_DATABASE_URL` those tests skip and the rest still run.

## Deploy

Phase 8. Not written yet.

## Rollback

Phase 8. Not written yet.

## Adding a workshop

Phase 8. Not written yet.

## Running the contractor test on a real workshop video

Phase 3. Not written yet.
