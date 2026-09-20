-- The scout goes global.
--
-- Three changes: feeds know which part of the world they speak for, feeds
-- remember whether they are actually working, and news items keep their
-- original language alongside the English summary.

-- Where a feed's news comes from. Shown on every Scout card, because "a soil
-- policy decision" means something different in Brussels and in Andhra Pradesh.
alter table feeds add column if not exists region text;

comment on column feeds.region is
  'Global, Africa, Asia, Europe, Latin America, North America, Oceania, or a '
  'country. Free text on purpose: the list grows as the Foundation does.';

-- Feed health. A URL that worked last year may not work today, and a feed
-- silently returning nothing is worse than one that fails loudly.
alter table feeds add column if not exists last_ok_at timestamptz;
alter table feeds add column if not exists last_error text;
alter table feeds add column if not exists last_checked_at timestamptz;
alter table feeds add column if not exists consecutive_failures integer not null default 0;

comment on column feeds.consecutive_failures is
  'Reset on any successful fetch. scout_fetch switches a feed off after five '
  'in a row rather than retrying a dead URL every morning forever.';

create index if not exists feeds_failing_idx on feeds (consecutive_failures desc)
  where consecutive_failures > 0;

-- Non-English items keep what they actually said. The summary is always
-- English so the ranker, the planner and the writer can all read it, but a
-- caption that quotes a Brazilian study should be able to quote the Portuguese.
alter table news_items add column if not exists language text;
alter table news_items add column if not exists original_title text;
alter table news_items add column if not exists original_summary text;

comment on column news_items.language is
  'BCP 47 tag of the source, as the ranker read it. Null means English or '
  'not yet ranked. summary and title are always English.';
