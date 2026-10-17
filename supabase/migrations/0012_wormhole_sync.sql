-- Wormhole <-> Google Doc sync.
-- Some posts in the planning doc have no day yet ("Date TBD"). They keep a
-- placeholder iso_date for sorting, and this flag says the date is not set.
alter table wormhole_posts add column if not exists date_tbd boolean not null default false;
