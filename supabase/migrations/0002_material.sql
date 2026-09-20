-- Material: batches, assets, tags, transcripts, people, smart folders.
-- Backend spec section 4.1.

create table batches (
  id            uuid primary key default gen_random_uuid(),
  drive_link    text,
  original_path text,
  creator       text,
  workshop      text,
  uploaded_at   timestamptz not null default now()
);

comment on table batches is
  'One row per upload session. Drive link, path, creator and workshop are '
  'entered once and inherited by every asset in the batch.';

create table assets (
  id             uuid primary key default gen_random_uuid(),
  batch_id       uuid references batches (id) on delete set null,
  -- Clips point at the video they were cut from.
  parent_id      uuid references assets (id) on delete cascade,

  type           text not null
                 check (type in ('photo', 'video', 'graphic', 'doc', 'clip', 'render', 'reference')),

  filename       text not null,
  bucket         text not null check (bucket in ('sfw-raw', 'sfw-media')),
  r2_key         text not null,
  thumb_key      text,
  proxy_key      text,
  audio_key      text,

  width          integer,
  height         integer,
  duration_s     real,
  clip_start_s   real,
  clip_end_s     real,

  status         text not null default 'inbox'
                 check (status in ('inbox', 'tagged', 'cleared', 'used', 'archived')),
  quality        smallint check (quality between 1 and 5),
  hero_candidate boolean not null default false,

  description    text,
  notes          text,

  drive_link     text,
  original_path  text,
  creator        text,
  credit_line    text,

  taken_at       timestamptz,
  camera         text,
  gps_lat        double precision,
  gps_lng        double precision,

  release_status text not null default 'unknown'
                 check (release_status in ('unknown', 'signed', 'missing')),

  embedding      vector(1024),

  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now(),

  -- One asset per object in R2. Makes the bulk-upload register script
  -- idempotent: a re-run after an interrupted rclone copy adds only new files.
  unique (bucket, r2_key),

  -- A clip has to know where in its parent it starts and ends.
  constraint clip_has_range check (
    type <> 'clip' or (parent_id is not null and clip_start_s is not null and clip_end_s is not null)
  ),
  constraint clip_range_ordered check (
    clip_start_s is null or clip_end_s is null or clip_end_s > clip_start_s
  )
);

create index assets_batch_idx     on assets (batch_id);
create index assets_parent_idx    on assets (parent_id);
create index assets_type_idx      on assets (type);
create index assets_status_idx    on assets (status);
create index assets_taken_at_idx  on assets (taken_at desc nulls last);
create index assets_created_idx   on assets (created_at desc);
-- Meaning search. Cosine, because the embeddings are normalised.
create index assets_embedding_idx on assets using hnsw (embedding vector_cosine_ops);

create trigger assets_set_updated_at
  before update on assets
  for each row execute function set_updated_at();

create table tags (
  id    bigint generated always as identity primary key,
  name  text not null,
  facet text not null
        check (facet in ('workshop', 'subject', 'organism', 'pillar',
                         'people', 'place', 'platform_fit', 'format')),
  unique (name, facet)
);

create table asset_tags (
  asset_id   uuid not null references assets (id) on delete cascade,
  tag_id     bigint not null references tags (id) on delete cascade,
  source     text not null check (source in ('ai', 'human')),
  confirmed  boolean not null default false,
  confidence real,
  primary key (asset_id, tag_id)
);

create index asset_tags_tag_idx on asset_tags (tag_id);
-- The Inbox's "untagged" and "unconfirmed" views hit this.
create index asset_tags_unconfirmed_idx on asset_tags (asset_id) where not confirmed;

create table transcripts (
  asset_id  uuid primary key references assets (id) on delete cascade,
  language  text,
  text      text,
  -- [{w, start, end, speaker}, ...]
  words     jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create table people (
  id             bigint generated always as identity primary key,
  name           text not null unique,
  role           text,
  org            text,
  email          text,
  release_status text not null default 'unknown'
                 check (release_status in ('unknown', 'signed', 'missing')),
  notes          text,
  -- Topics this person answers questions about. gap_check routes by these:
  -- programs to Stephanie, mentors and graduates to Carla, India and partners
  -- to Kavi, workshops to Loida (CLAUDE.md section 10).
  topics         text[] not null default '{}'
);

create index people_topics_idx on people using gin (topics);

create table asset_people (
  asset_id  uuid not null references assets (id) on delete cascade,
  person_id bigint not null references people (id) on delete cascade,
  source    text not null check (source in ('ai', 'human')),
  confirmed boolean not null default false,
  primary key (asset_id, person_id)
);

create index asset_people_person_idx on asset_people (person_id);

create table smart_folders (
  id       bigint generated always as identity primary key,
  name     text not null,
  -- Sidebar grouping, per PRD 5.1.
  section  text not null check (section in ('workshops', 'asset_types', 'views', 'saved')),
  filters  jsonb not null default '{}'::jsonb,
  position integer not null default 0,
  unique (section, name)
);

comment on table smart_folders is
  'Saved filters, not containers. One asset shows up in every folder it matches.';
