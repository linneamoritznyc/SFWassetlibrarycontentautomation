-- Wormhole: the team's preview of planned social posts.
-- Kept apart from the agent pipeline's `posts` table so the team can edit
-- freely without tripping its constraints. The web app reaches these through
-- DATABASE_URL on the server only. RLS is on with no policies, so the public
-- anon key can read nothing here.

create table if not exists wormhole_posts (
  id           text primary key,
  iso_date     date not null,
  topic        text not null default '',
  platform     text not null default 'Instagram, Facebook, LinkedIn',
  caption      text not null default '',
  -- [{ "text": "...", "image": "<wormhole_images.id>" | null }]
  slides       jsonb not null default '[]'::jsonb,
  cta          text not null default '',
  link         text not null default '',
  sources      jsonb not null default '[]'::jsonb,
  visual_note  text not null default '',
  note         text not null default '',
  status       text not null default 'draft'
               check (status in ('draft', 'copy_approved', 'approved', 'scheduled')),
  created_by   text not null default 'seed',
  updated_by   text not null default 'seed',
  updated_at   timestamptz not null default now()
);

create index if not exists wormhole_posts_date on wormhole_posts (iso_date);
create index if not exists wormhole_posts_updated on wormhole_posts (updated_at);

create table if not exists wormhole_versions (
  id          bigserial primary key,
  post_id     text not null references wormhole_posts (id) on delete cascade,
  data        jsonb not null,
  editor      text not null,
  created_at  timestamptz not null default now()
);

create index if not exists wormhole_versions_post on wormhole_versions (post_id, created_at desc);

create table if not exists wormhole_images (
  id          uuid primary key default gen_random_uuid(),
  mime        text not null,
  bytes       bytea not null,
  width       int,
  height      int,
  uploaded_by text not null,
  created_at  timestamptz not null default now()
);

alter table wormhole_posts enable row level security;
alter table wormhole_versions enable row level security;
alter table wormhole_images enable row level security;
