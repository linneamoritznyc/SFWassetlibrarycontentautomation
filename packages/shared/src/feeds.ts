/**
 * The soil source list the scout reads every morning.
 *
 * Global on purpose. The Foundation has graduates in over 100 countries, so a
 * source list that is all English-language North American press would keep
 * handing the planner the same five stories. These reach across the UN bodies,
 * the research networks, and the regional programmes actually doing the work:
 * Embrapa in Brazil, APCNF in Andhra Pradesh, AGRA across Africa, Soils for
 * Life in Australia.
 *
 * Non-English feeds are welcome. `scout_rank` summarises everything in English
 * and keeps the original language on the card, so a Portuguese study from
 * Embrapa is as usable as an English one from CGIAR.
 *
 * ## About these URLs
 *
 * None of them could be reached from the sandbox this was built in: its egress
 * proxy refuses every host that is not on its allowlist. So they are the best
 * known URL for each organisation, not confirmed-working ones.
 *
 * That is handled rather than hoped about. `scout_fetch` records
 * `last_ok_at`, `last_error` and `consecutive_failures` on every feed, switches
 * one off after five failures in a row, and the Settings screen shows exactly
 * which are broken. `pnpm feeds:check` tests all of them in one go and prints
 * a table.
 */

export type Region =
  'Global' | 'Africa' | 'Asia' | 'Europe' | 'Latin America' | 'North America' | 'Oceania';

export const REGIONS: Region[] = [
  'Global',
  'Africa',
  'Asia',
  'Europe',
  'Latin America',
  'North America',
  'Oceania',
];

export type FeedSeed = {
  name: string;
  url: string;
  /** `rss` is parsed as a feed; `page` is read as a source page by web_fetch. */
  kind: 'rss' | 'page';
  region: Region;
  /** Shown in Settings so a dead feed can be replaced with the right thing. */
  note?: string;
};

export const FEEDS: FeedSeed[] = [
  // ---------------------------------------------------------------- Global
  {
    name: 'FAO Global Soil Partnership',
    url: 'https://www.fao.org/global-soil-partnership/resources/highlights/en/',
    kind: 'page',
    region: 'Global',
    note: 'No RSS published. Read as a page; the highlights list is the news.',
  },
  {
    name: 'UNCCD',
    url: 'https://www.unccd.int/rss.xml',
    kind: 'rss',
    region: 'Global',
    note: 'Land degradation, desertification and drought.',
  },
  {
    name: 'IPBES',
    url: 'https://www.ipbes.net/rss.xml',
    kind: 'rss',
    region: 'Global',
    note: 'Biodiversity and ecosystem services assessments.',
  },
  {
    name: 'CGIAR',
    url: 'https://www.cgiar.org/feed/',
    kind: 'rss',
    region: 'Global',
    note: 'The fifteen international agricultural research centres.',
  },
  {
    name: 'World Resources Institute',
    url: 'https://www.wri.org/rss.xml',
    kind: 'rss',
    region: 'Global',
  },
  {
    name: 'Regeneration International',
    url: 'https://regenerationinternational.org/feed/',
    kind: 'rss',
    region: 'Global',
  },
  {
    name: 'ScienceDaily: Soil',
    url: 'https://www.sciencedaily.com/rss/earth_climate/soil.xml',
    kind: 'rss',
    region: 'Global',
  },
  {
    name: 'ScienceDaily: Microbes and More',
    url: 'https://www.sciencedaily.com/rss/plants_animals/microbes_and_more.xml',
    kind: 'rss',
    region: 'Global',
  },
  {
    name: 'Phys.org: Agriculture',
    url: 'https://phys.org/rss-feed/biology-news/agriculture/',
    kind: 'rss',
    region: 'Global',
  },
  {
    name: 'EurekAlert: Agriculture',
    url: 'https://www.eurekalert.org/rss/agriculture.xml',
    kind: 'rss',
    region: 'Global',
  },

  // ---------------------------------------------------------------- Africa
  {
    name: 'African Union: news and events',
    url: 'https://au.int/en/newsevents',
    kind: 'page',
    region: 'Africa',
    note: 'Soil health is an AU priority under the Fertilizer and Soil Health Summit. No RSS found.',
  },
  {
    name: 'AGRA',
    url: 'https://agra.org/feed/',
    kind: 'rss',
    region: 'Africa',
    note: 'Alliance for a Green Revolution in Africa.',
  },

  // ------------------------------------------------------------------ Asia
  {
    name: 'ICRISAT',
    url: 'https://www.icrisat.org/feed/',
    kind: 'rss',
    region: 'Asia',
    note: 'Semi-arid tropics research, based in Hyderabad.',
  },
  {
    name: 'APCNF (Andhra Pradesh natural farming)',
    url: 'https://apcnf.in/fresh-from-farm/',
    kind: 'page',
    region: 'Asia',
    note: 'A million farmers moving to natural farming. No RSS; the news page is "Fresh from Farm".',
  },
  {
    name: 'Down To Earth: Agriculture',
    url: 'https://www.downtoearth.org.in/rss/agriculture',
    kind: 'rss',
    region: 'Asia',
  },
  {
    name: 'Isha Foundation blog',
    url: 'https://isha.sadhguru.org/en/blog/feed',
    kind: 'rss',
    region: 'Asia',
    note: 'Partner. Conscious Planet and the Save Soil campaign.',
  },
  {
    name: 'Save Soil',
    url: 'https://consciousplanet.org/en/save-soil/news',
    kind: 'page',
    region: 'Asia',
    note: 'Partner campaign.',
  },

  // ---------------------------------------------------------------- Europe
  {
    name: 'EU Soil Observatory',
    url: 'https://joint-research-centre.ec.europa.eu/eu-soil-observatory-euso_en',
    kind: 'page',
    region: 'Europe',
    note: 'The Commission JRC soil observatory. Newsletter rather than RSS.',
  },
  {
    name: 'European Environment Agency',
    url: 'https://www.eea.europa.eu/en/newsroom/news/RSS',
    kind: 'rss',
    region: 'Europe',
  },
  {
    name: 'Permaculture News',
    url: 'https://www.permaculturenews.org/feed/',
    kind: 'rss',
    region: 'Europe',
    note: 'Partner network.',
  },
  {
    name: 'Permaculture Magazine',
    url: 'https://www.permaculture.co.uk/rss.xml',
    kind: 'rss',
    region: 'Europe',
    note: 'Partner network.',
  },

  // --------------------------------------------------------- Latin America
  {
    name: 'Embrapa',
    url: 'https://www.embrapa.br/en/busca-de-noticias/-/noticia/rss',
    kind: 'rss',
    region: 'Latin America',
    note: 'Brazilian agricultural research. Publishes in Portuguese; summarised in English.',
  },
  {
    name: 'IICA',
    url: 'https://iica.int/en/press',
    kind: 'page',
    region: 'Latin America',
    note: 'Inter-American Institute for Cooperation on Agriculture. Spanish and English.',
  },

  // --------------------------------------------------------- North America
  {
    name: 'USDA NRCS newsroom',
    url: 'https://www.nrcs.usda.gov/rss/news.xml',
    kind: 'rss',
    region: 'North America',
  },
  {
    name: 'AgFunderNews',
    url: 'https://agfundernews.com/feed',
    kind: 'rss',
    region: 'North America',
  },
  {
    name: 'Civil Eats',
    url: 'https://civileats.com/feed/',
    kind: 'rss',
    region: 'North America',
  },

  // --------------------------------------------------------------- Oceania
  {
    name: 'Soils For Life',
    url: 'https://soilsforlife.org.au/feed/',
    kind: 'rss',
    region: 'Oceania',
    note: 'Australian regenerative agriculture case studies.',
  },
];
