-- Knowledge: sources, facts, rules, questions. Backend spec section 4.2.

create table sources (
  id           bigint generated always as identity primary key,
  kind         text not null check (kind in ('url', 'doc', 'transcript', 'human', 'post')),
  -- A URL, an asset id, a person's name: what this source points at.
  ref          text not null,
  title        text,
  fetched_at   timestamptz,
  content_hash text,
  created_at   timestamptz not null default now(),
  unique (kind, ref)
);

comment on column sources.content_hash is
  'web_refresh compares this on every re-fetch. A change re-extracts the facts.';

create table facts (
  -- integer, not bigint: stories.material_fact_ids and news_items.linked_facts
  -- are int[] in the spec and have to line up with this.
  id           integer generated always as identity primary key,
  subject      text not null,
  predicate    text not null,
  object       text not null,
  -- The same thing as one plain sentence, which is what the writer reads.
  text         text not null,
  source_id    bigint references sources (id) on delete set null,
  confidence   real not null default 0.5 check (confidence between 0 and 1),
  status       text not null default 'active'
               check (status in ('active', 'conflict', 'retired')),
  confirmed_by text,
  valid_from   timestamptz,
  valid_to     timestamptz,
  embedding    vector(1024),
  created_at   timestamptz not null default now()
);

create index facts_source_idx    on facts (source_id);
create index facts_status_idx    on facts (status);
create index facts_subject_idx   on facts (subject);
create index facts_embedding_idx on facts using hnsw (embedding vector_cosine_ops);

create table rules (
  id            bigint generated always as identity primary key,
  scope         text not null
                check (scope in ('all', 'instagram', 'linkedin', 'reel', 'caption', 'critic')),
  text          text not null,
  origin        text not null check (origin in ('edit', 'rejection', 'result', 'manual')),
  -- Which posts or edits argued for this rule.
  evidence      jsonb not null default '[]'::jsonb,
  active        boolean not null default false,
  applied_count integer not null default 0,
  created_at    timestamptz not null default now()
);

create index rules_active_scope_idx on rules (scope) where active;

create table questions (
  id          bigint generated always as identity primary key,
  text        text not null,
  asked_to    bigint references people (id) on delete set null,
  context     jsonb not null default '{}'::jsonb,
  status      text not null default 'open'
              check (status in ('open', 'answered', 'dropped')),
  answer      text,
  answered_at timestamptz,
  -- Not in the spec's column list, but the 48 h nudge and the 72 h gap_check
  -- timeout both need to know when the question was asked.
  created_at  timestamptz not null default now(),
  nudged_at   timestamptz
);

create index questions_open_idx on questions (created_at) where status = 'open';
