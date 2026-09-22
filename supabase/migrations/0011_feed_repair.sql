-- The scout repairs its own source list.
--
-- Every feed URL in the seed is the best known URL for that organisation
-- rather than a tested one, and feeds move anyway. Three things follow:
-- remember what kind of failure it was, remember where a feed moved to, and
-- stop re-downloading a feed that has not changed.

-- What sort of failure the last one was: moved, empty, blocked or transient.
-- Null when the feed is healthy. This is what decides whether a feed is
-- switched off: only a feed whose URL looks genuinely dead is, so a partner
-- site behind bot protection and a site down for maintenance both stay in the
-- list where a person can see them.
alter table feeds add column if not exists failure_kind text
  check (failure_kind in ('moved', 'empty', 'blocked', 'transient'));

-- Where the feed used to be, when the scout found it somewhere else and moved
-- it. Kept so the change is visible and reversible rather than silent.
alter table feeds add column if not exists previous_url text;
alter table feeds add column if not exists url_fixed_at timestamptz;

comment on column feeds.previous_url is
  'Set when scout_fetch found this feed at a new URL after the old one broke. '
  'Settings shows it so the repair can be checked or undone.';

-- Conditional requests. A feed that gives us an ETag or Last-Modified gets
-- them back on the next ask, and answers 304 with no body when nothing has
-- been published. Cheaper for us and considerably politer to the small
-- institutional servers we hit every morning.
alter table feeds add column if not exists etag text;
alter table feeds add column if not exists last_modified text;

comment on column feeds.etag is
  'Validator from the last successful fetch, sent back as If-None-Match.';
