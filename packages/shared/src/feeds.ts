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
 * Checked by hand on 23 October 2026. Where an organisation publishes no
 * working RSS, the feed is a Google News search limited to its site
 * (`site:cgiar.org`), which lists its new pages with real dates. `fallback`
 * is tried when the main URL fails, so a feed that blocks one server still
 * answers from the other.
 *
 * Wormhole's Soil news tab (apps/web/lib/scout.ts) reads this list live and
 * shows which feeds answered. `python3 tools/scout/fetch_feeds.py` does the
 * same from a terminal.
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
  /** Tried when `url` fails or returns nothing. */
  fallback?: string;
};

export const FEEDS: FeedSeed[] = [
  // ---------------------------------------------------------------- Global
  {
    name: 'FAO Global Soil Partnership',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Afao.org%20soil%20when%3A30d',
    kind: 'rss',
    region: 'Global',
    note: 'No RSS published, so a Google News search of fao.org for soil.',
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
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Acgiar.org%20soil%20OR%20farmers%20OR%20land%20when%3A14d',
    kind: 'rss',
    region: 'Global',
    note: 'The fifteen international agricultural research centres.',
  },
  {
    name: 'World Resources Institute',
    url: 'https://www.wri.org/insights/rss.xml',
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
    url: 'https://www.sciencedaily.com/rss/plants_animals/soil_types.xml',
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
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Aeurekalert.org%20soil%20when%3A14d',
    kind: 'rss',
    region: 'Global',
  },

  {
    name: 'ScienceDaily: Fungi',
    url: 'https://www.sciencedaily.com/rss/plants_animals/fungus.xml',
    kind: 'rss',
    region: 'Global',
  },
  {
    name: 'Frontiers in Soil Science',
    url: 'https://www.frontiersin.org/journals/soil-science/rss',
    kind: 'rss',
    region: 'Global',
    note: 'Open-access journal. New papers, so read the paper, not only the abstract.',
  },
  {
    name: 'Nature: soil microbiology',
    url: 'https://www.nature.com/subjects/soil-microbiology.rss',
    kind: 'rss',
    region: 'Global',
    note: 'Papers and news across the Nature journals.',
  },
  {
    name: 'Mongabay',
    url: 'https://news.mongabay.com/feed/',
    kind: 'rss',
    region: 'Global',
    note: 'Environmental journalism with strong coverage of the Global South.',
  },

  {
    name: 'Soil Health Institute',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=%22Soil%20Health%20Institute%22%20OR%20site%3Asoilhealthinstitute.org%20when%3A30d',
    kind: 'rss',
    region: 'North America',
    note: 'Led by Ashley McKeon since June 2026. No public RSS, so a news search.',
  },
  {
    name: 'Rodale Institute',
    url: 'https://rodaleinstitute.org/feed/',
    kind: 'rss',
    region: 'North America',
    note: 'Regenerative organic research, home of the 40-year Farming Systems Trial.',
    fallback:
      'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=%22Rodale%20Institute%22%20when%3A30d',
  },

  // ---------------------------------------------------------------- Africa
  {
    name: 'African Union: news and events',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=%22African%20Union%22%20soil%20health%20OR%20fertilizer%20when%3A30d',
    kind: 'rss',
    region: 'Africa',
    note: 'Soil health is an AU priority under the Fertilizer and Soil Health Summit. No RSS, so a news search.',
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
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Aicrisat.org%20when%3A30d',
    kind: 'rss',
    region: 'Asia',
    note: 'Semi-arid tropics research, based in Hyderabad.',
    fallback: 'https://www.icrisat.org/feed/',
  },
  {
    name: 'APCNF (Andhra Pradesh natural farming)',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=APCNF%20OR%20%22Andhra%20Pradesh%20natural%20farming%22%20OR%20%22Andhra%20Pradesh%20Community-managed%20Natural%20Farming%22%20when%3A30d',
    kind: 'rss',
    region: 'Asia',
    note: 'A million farmers moving to natural farming. No RSS, so a news search.',
  },
  {
    name: 'Down To Earth: Agriculture',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Adowntoearth.org.in%20soil%20OR%20farming%20when%3A14d',
    kind: 'rss',
    region: 'Asia',
  },
  {
    name: 'Isha Foundation blog',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Aisha.sadhguru.org%20soil%20when%3A60d',
    kind: 'rss',
    region: 'Asia',
    note: 'Partner. Conscious Planet and the Save Soil campaign.',
  },
  {
    name: 'Save Soil',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=%22Save%20Soil%22%20when%3A30d',
    kind: 'rss',
    region: 'Asia',
    note: 'Partner campaign.',
  },

  // ---------------------------------------------------------------- Europe
  {
    name: 'EU Soil Observatory',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=%22EU%20Soil%20Observatory%22%20OR%20%22Soil%20Monitoring%20Law%22%20OR%20%22soil%20health%20law%22%20when%3A30d',
    kind: 'rss',
    region: 'Europe',
    note: 'The Commission JRC soil observatory. No RSS, so a news search for the observatory and the EU soil law.',
  },
  {
    name: 'European Environment Agency',
    url: 'https://www.eea.europa.eu/en/newsroom/news/rss.xml',
    kind: 'rss',
    region: 'Europe',
  },
  {
    name: 'Permaculture News',
    url: 'https://www.permaculturenews.org/feed/',
    kind: 'rss',
    region: 'Europe',
    note: 'Partner network.',
    fallback:
      'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=permaculture%20when%3A14d',
  },
  {
    name: 'Permaculture Magazine',
    url: 'https://www.permaculture.co.uk/feed',
    kind: 'rss',
    region: 'Europe',
    note: 'Partner network.',
  },

  // --------------------------------------------------------- Latin America
  {
    name: 'Embrapa',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Aembrapa.br%20solo%20OR%20soil%20when%3A30d',
    kind: 'rss',
    region: 'Latin America',
    note: 'Brazilian agricultural research. Publishes in Portuguese; summarised in English.',
    fallback: 'https://www.embrapa.br/en/busca-de-noticias/-/noticia/rss',
  },
  {
    name: 'IICA',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Aiica.int%20soil%20OR%20suelo%20OR%20suelos%20when%3A60d',
    kind: 'rss',
    region: 'Latin America',
    note: 'Inter-American Institute for Cooperation on Agriculture. Spanish and English.',
  },

  // --------------------------------------------------------- North America
  {
    name: 'USDA NRCS newsroom',
    url: 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=site%3Anrcs.usda.gov%20when%3A30d',
    kind: 'rss',
    region: 'North America',
    fallback: 'https://www.nrcs.usda.gov/rss/news.xml',
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
    note: 'The feed answers curl but challenges server-side fetches, hence the news search.',
    fallback:
      'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=civileats.com%20when%3A14d',
  },

  // --------------------------------------------------------------- Oceania
  {
    name: 'Soils For Life',
    url: 'https://soilsforlife.org.au/feed/',
    kind: 'rss',
    region: 'Oceania',
    note: 'Australian regenerative agriculture case studies.',
    fallback:
      'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=%22Soils%20For%20Life%22%20OR%20site%3Asoilsforlife.org.au%20when%3A90d',
  },
];
