-- Soil news stories the team set aside with "Not for us", shared across devices.
-- The scout route also creates this on first use, so the app never waits on it.
create table if not exists wormhole_news_hidden (
  url        text primary key,
  hidden_by  text not null,
  hidden_at  timestamptz not null default now()
);
alter table wormhole_news_hidden enable row level security;
