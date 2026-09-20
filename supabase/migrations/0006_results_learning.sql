-- Results and learning: metrics, test cases, eval runs, prompts, AI call log.
-- Backend spec section 4.5.

create table metrics (
  post_id       uuid not null references posts (id) on delete cascade,
  captured_at   timestamptz not null default now(),
  reach         integer,
  likes         integer,
  comments      integer,
  saves         integer,
  shares        integer,
  link_clicks   integer,
  watch_time_s  real,
  primary key (post_id, captured_at)
);

comment on table metrics is
  'One row per pull, so the history is kept rather than overwritten. '
  'Measure by saves, shares and comments. Likes come last (CLAUDE.md section 6).';

create table test_cases (
  id       bigint generated always as identity primary key,
  name     text not null unique,
  kind     text not null check (kind in ('good', 'bad')),
  input    jsonb not null default '{}'::jsonb,
  expected jsonb not null default '{}'::jsonb,
  notes    text,
  created_at timestamptz not null default now()
);

create table prompts (
  id         bigint generated always as identity primary key,
  name       text not null,
  version    integer not null,
  body       text not null,
  active     boolean not null default false,
  created_at timestamptz not null default now(),
  unique (name, version)
);

-- Exactly one active version per prompt. eval_nightly's auto-rollback flips
-- this pair inside one transaction.
create unique index prompts_one_active_idx on prompts (name) where active;

create table eval_runs (
  id             bigint generated always as identity primary key,
  prompt_name    text not null,
  prompt_version integer not null,
  passed         integer not null default 0,
  failed         integer not null default 0,
  details        jsonb not null default '{}'::jsonb,
  created_at     timestamptz not null default now()
);

create index eval_runs_prompt_idx on eval_runs (prompt_name, created_at desc);

create table ai_calls (
  id             bigint generated always as identity primary key,
  job_id         bigint,
  prompt_name    text not null,
  prompt_version integer,
  model          text not null,
  input_tokens   integer,
  output_tokens  integer,
  cost_usd       numeric(10, 6),
  latency_ms     integer,
  created_at     timestamptz not null default now()
);

create index ai_calls_job_idx     on ai_calls (job_id);
create index ai_calls_prompt_idx  on ai_calls (prompt_name, created_at desc);
create index ai_calls_created_idx on ai_calls (created_at desc);

comment on table ai_calls is
  'Cost and latency per job and per prompt version. The Monday email and the '
  'per-clip cost in the Clips header both read from here.';

-- Planner weights, updated by learn_weekly with a moving average capped at
-- plus or minus 20% a week. Not a table in the spec, but format_weight and
-- pillar_balance have to live somewhere the planner can read.
create table planner_weights (
  key        text primary key,
  kind       text not null check (kind in ('format', 'pillar')),
  weight     real not null default 1.0 check (weight > 0),
  data_points integer not null default 0,
  updated_at timestamptz not null default now()
);

-- Small key-value settings: cadence config, feature flags. Everything here is
-- editable from the Settings view.
create table settings (
  key        text primary key,
  value      jsonb not null,
  updated_at timestamptz not null default now()
);

-- Worker health. Each process writes one row every 60 s; the app shows a red
-- dot when a heartbeat is more than 5 minutes old (backend spec section 10).
create table worker_heartbeats (
  worker   text primary key,
  types    text[] not null default '{}',
  beat_at  timestamptz not null default now()
);
