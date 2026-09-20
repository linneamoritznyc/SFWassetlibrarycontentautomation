/**
 * The soil source list the scout reads every morning.
 *
 * Five groups, from PRD 5.3: research, soil policy in the EU, US and India,
 * partner news, the permaculture network, and the regenerative agriculture
 * press.
 *
 * URLs go stale. `scout_fetch` reports a feed that keeps failing rather than
 * failing itself, and the Settings view is where one gets turned off or
 * replaced. Treat this list as a starting point, not a fact.
 */

export type FeedSeed = { name: string; url: string; kind: 'rss' | 'page' | 'api' };

export const FEEDS: FeedSeed[] = [
  // Research
  {
    name: 'ScienceDaily: Soil',
    url: 'https://www.sciencedaily.com/rss/earth_climate/soil.xml',
    kind: 'rss',
  },
  {
    name: 'ScienceDaily: Microbes and More',
    url: 'https://www.sciencedaily.com/rss/plants_animals/microbes_and_more.xml',
    kind: 'rss',
  },
  {
    name: 'Phys.org: Agriculture',
    url: 'https://phys.org/rss-feed/biology-news/agriculture/',
    kind: 'rss',
  },
  {
    name: 'EurekAlert: Agriculture',
    url: 'https://www.eurekalert.org/rss/agriculture.xml',
    kind: 'rss',
  },

  // Soil policy
  {
    name: 'European Environment Agency',
    url: 'https://www.eea.europa.eu/en/newsroom/news/RSS',
    kind: 'rss',
  },
  { name: 'USDA NRCS newsroom', url: 'https://www.nrcs.usda.gov/rss/news.xml', kind: 'rss' },
  {
    name: 'Down To Earth: Agriculture (India)',
    url: 'https://www.downtoearth.org.in/rss/agriculture',
    kind: 'rss',
  },

  // Partners
  { name: 'Save Soil', url: 'https://consciousplanet.org/en/save-soil/news', kind: 'page' },
  { name: 'Isha Foundation blog', url: 'https://isha.sadhguru.org/en/blog/feed', kind: 'rss' },

  // Permaculture network
  { name: 'Permaculture News', url: 'https://www.permaculturenews.org/feed/', kind: 'rss' },
  { name: 'Permaculture Magazine', url: 'https://www.permaculture.co.uk/rss.xml', kind: 'rss' },

  // Regenerative agriculture press
  {
    name: 'Regeneration International',
    url: 'https://regenerationinternational.org/feed/',
    kind: 'rss',
  },
  { name: 'AgFunderNews', url: 'https://agfundernews.com/feed', kind: 'rss' },
  { name: 'Civil Eats', url: 'https://civileats.com/feed/', kind: 'rss' },
];
