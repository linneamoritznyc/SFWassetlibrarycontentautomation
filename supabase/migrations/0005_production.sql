-- Production: stories, posts, versions, renders, Canva links.
-- Backend spec section 4.4.

create table stories (
  id                bigint generated always as identity primary key,
  origin            text not null check (origin in ('asset', 'news', 'fact', 'manual')),
  -- Points at whatever the origin was: an asset id, a news_items id, a fact id.
  origin_ref        text,
  angle             text,
  pillar            text check (pillar in ('PROVE IT', 'TEACH IT', 'PRACTICE IT', 'GROW IT')),
  material_asset_ids uuid[] not null default '{}',
  material_fact_ids  integer[] not null default '{}',
  score             real,
  status            text not null default 'candidate'
                    check (status in ('candidate', 'planned', 'used', 'dropped')),
  created_at        timestamptz not null default now()
);

create index stories_status_idx on stories (status);
create index stories_score_idx  on stories (score desc nulls last);

create table renders (
  id         uuid primary key default gen_random_uuid(),
  template   text not null,
  input      jsonb not null default '{}'::jsonb,
  bucket     text check (bucket in ('sfw-raw', 'sfw-media')),
  r2_key     text,
  status     text not null default 'queued'
             check (status in ('queued', 'running', 'done', 'failed')),
  duration_s real,
  cost_usd   numeric(10, 4),
  created_at timestamptz not null default now()
);

create table posts (
  id            uuid primary key default gen_random_uuid(),
  story_id      bigint references stories (id) on delete set null,
  slot_date     date,
  slot_time     time,
  platform      text not null
                check (platform in ('instagram', 'facebook', 'linkedin', 'youtube')),
  format        text not null
                check (format in ('feed', 'carousel', 'reel', 'story', 'linkedin', 'short')),
  asset_ids     uuid[] not null default '{}',
  render_id     uuid references renders (id) on delete set null,

  hook          text,
  caption       text,
  hashtags      text[] not null default '{}',
  cta_text      text,
  cta_url       text,
  collaborators text[] not null default '{}',

  status        text not null default 'proposed'
                check (status in ('proposed', 'revising', 'in_review', 'approved',
                                  'rejected', 'exported', 'published')),
  reject_reason text check (reject_reason in ('too_vague', 'wrong_image', 'ai_tone',
                                              'fact_wrong', 'off_brand')),
  experiment    boolean not null default false,

  critic_score  real,
  critic_notes  jsonb,

  -- learn_weekly promotes the best approved posts; brief reads them back as the
  -- three examples the writer sees first.
  is_example    boolean not null default false,

  published_url text,
  published_at  timestamptz,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),

  -- PRD principle 1, enforced in the database as well as in code: a post exists
  -- only when its material exists. Nothing but a proposed slot may sit empty.
  constraint post_has_material check (
    status = 'proposed'
    or cardinality(asset_ids) > 0
    or render_id is not null
  ),
  -- A rejection says why.
  constraint rejection_has_reason check (
    status <> 'rejected' or reject_reason is not null
  )
);

create index posts_slot_idx    on posts (slot_date, slot_time);
create index posts_status_idx  on posts (status);
create index posts_story_idx   on posts (story_id);
create index posts_example_idx on posts (format, platform) where is_example;

create trigger posts_set_updated_at
  before update on posts
  for each row execute function set_updated_at();

create table post_versions (
  id             bigint generated always as identity primary key,
  post_id        uuid not null references posts (id) on delete cascade,
  version        integer not null,
  author         text not null check (author in ('ai', 'human')),
  caption        text,
  hook           text,
  hashtags       text[] not null default '{}',
  asset_ids      uuid[] not null default '{}',
  -- Set by log_edit: what the human changed about the AI's version.
  diff           jsonb,
  prompt_version text,
  created_at     timestamptz not null default now(),
  unique (post_id, version)
);

create index post_versions_post_idx on post_versions (post_id, version desc);

create table canva_links (
  id                 bigint generated always as identity primary key,
  post_id            uuid not null references posts (id) on delete cascade,
  canva_design_id    text not null,
  edit_url           text,
  exported_asset_id  uuid references assets (id) on delete set null,
  status             text not null default 'created'
                     check (status in ('created', 'edited', 'exported', 'failed')),
  created_at         timestamptz not null default now(),
  unique (post_id, canva_design_id)
);

-- link_asset_usage writes these when a post goes out, so the library can show
-- "used in" on every asset and the Unused view means what it says.
create table asset_usage (
  asset_id uuid not null references assets (id) on delete cascade,
  post_id  uuid not null references posts (id) on delete cascade,
  used_at  timestamptz not null default now(),
  primary key (asset_id, post_id)
);

create index asset_usage_post_idx on asset_usage (post_id);
