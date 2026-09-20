import * as cheerio from 'cheerio';

export type FetchedPage = { url: string; title: string; text: string };

const MAX_BYTES = 5_000_000;
const TIMEOUT_MS = 20_000;

/**
 * Fetches a page and pulls the readable text out of it.
 *
 * Deliberately plain: the navigation, scripts and boilerplate are dropped and
 * what is left is the prose, which is what the fact extractor needs. It does
 * not run JavaScript, so a page that renders entirely client-side comes back
 * thin, and the caller should notice that rather than store nothing.
 */
export async function fetchPage(url: string): Promise<FetchedPage> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const res = await fetch(url, {
      signal: controller.signal,
      redirect: 'follow',
      headers: {
        // Say who we are. A site that wants to block us should be able to.
        'user-agent': 'SFWContentStudio/0.1 (+https://soilfoodweb.com)',
        accept: 'text/html,application/xhtml+xml',
      },
    });

    if (!res.ok) throw new Error(`${url} returned ${res.status}`);

    const type = res.headers.get('content-type') ?? '';
    if (!type.includes('html') && !type.includes('text')) {
      throw new Error(`${url} is ${type}, not a web page`);
    }

    const body = await res.arrayBuffer();
    if (body.byteLength > MAX_BYTES) throw new Error(`${url} is too large to read`);

    const html = new TextDecoder().decode(body);
    const $ = cheerio.load(html);

    $('script, style, noscript, nav, header, footer, aside, form, iframe, svg').remove();

    const title = (
      $('meta[property="og:title"]').attr('content') ||
      $('title').text() ||
      ''
    ).trim();

    // Block-level elements become their own line, so paragraphs survive.
    $('p, li, h1, h2, h3, h4, h5, h6, blockquote, td').each((_, el) => {
      $(el).append('\n');
    });

    const text = $('body')
      .text()
      .replace(/[ \t\u00a0]+/g, ' ')
      .replace(/\n{3,}/g, '\n\n')
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .join('\n');

    return { url: res.url || url, title, text };
  } finally {
    clearTimeout(timer);
  }
}
