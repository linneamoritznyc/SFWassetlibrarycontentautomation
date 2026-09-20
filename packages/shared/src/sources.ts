/**
 * The pages the Foundation's facts live on, from CLAUDE.md section 9.
 *
 * These are seeded as `sources(kind = 'url')` and re-read weekly by
 * `web_refresh`. When a price or a date changes on one of them, the old fact is
 * retired and the new one takes its place, so a caption written next month does
 * not quote last month's price.
 */

export type SourceSeed = { url: string; title: string };

export const SOURCE_PAGES: SourceSeed[] = [
  {
    url: 'https://school.soilfoodweb.com/courses/india-workshop-2026',
    title: 'India Accelerator Workshop 2026',
  },
  {
    url: 'https://school.soilfoodweb.com/pages/workshop-interest',
    title: 'Workshop interest form',
  },
  {
    url: 'https://school.soilfoodweb.com/courses/life-in-the-soils-seminar-2-day',
    title: 'Life in the Soils 2-day seminar',
  },
  { url: 'https://school.soilfoodweb.com/collections', title: 'All courses' },
  { url: 'https://webinar.soilfoodweb.com', title: 'Webinars' },
  { url: 'https://soilfoodweb.com', title: 'Soil Food Web Foundation' },
];
