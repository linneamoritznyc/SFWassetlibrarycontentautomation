-- Scout: feeds and news items. Backend spec section 4.3.

create table feeds (
  id     bigint generated always as identity primary key,
  name   text not null,
  url    text not null unique,
  kind   text not null check (kind in ('rss', 'page', 'api')),
  active boolean not null default true
);

create table news_items (
  id            bigint generated always as identity primary key,
  feed_id       bigint references feeds (id) on delete cascade,
  url           text not null unique,
  title         text,
  published_at  timestamptz,
  summary       text,
  relevance     real check (relevance between 0 and 1),
  linked_facts  integer[] not null default '{}',
  linked_assets uuid[] not null default '{}',
  status        text not null default 'new' check (status in ('new', 'drafted', 'dismissed')),
  embedding     vector(1024),
  created_at    timestamptz not null default now()
);

create index news_items_feed_idx      on news_items (feed_id);
create index news_items_status_idx    on news_items (status);
create index news_items_relevance_idx on news_items (relevance desc nulls last);
create index news_items_embedding_idx on news_items using hnsw (embedding vector_cosine_ops);
