/**
 * Reading a Later export.
 *
 * Later's CSV column names have changed more than once and differ by plan, so
 * this matches on what a header contains rather than on an exact name, and
 * reports what it could not match instead of silently importing zeros.
 */

export type ImportedRow = {
  permalink: string | null;
  postedAt: string | null;
  reach: number | null;
  likes: number | null;
  comments: number | null;
  saves: number | null;
  shares: number | null;
  linkClicks: number | null;
};

const COLUMNS: { field: keyof ImportedRow; matches: string[] }[] = [
  { field: 'permalink', matches: ['permalink', 'post url', 'url', 'link to post'] },
  { field: 'postedAt', matches: ['published', 'posted', 'date', 'scheduled time'] },
  { field: 'reach', matches: ['reach', 'impressions'] },
  { field: 'likes', matches: ['likes', 'like'] },
  { field: 'comments', matches: ['comments', 'comment'] },
  { field: 'saves', matches: ['saves', 'saved', 'bookmarks'] },
  { field: 'shares', matches: ['shares', 'shared'] },
  { field: 'linkClicks', matches: ['link clicks', 'clicks', 'website clicks'] },
];

export function parseLaterCsv(csv: string): { rows: ImportedRow[]; unmatched: string[] } {
  const lines = splitRows(csv).filter((l) => l.some((cell) => cell.trim() !== ''));
  if (lines.length < 2) return { rows: [], unmatched: [] };

  const header = lines[0]!.map((h) => h.trim().toLowerCase());
  const index: Partial<Record<keyof ImportedRow, number>> = {};

  for (const { field, matches } of COLUMNS) {
    const at = header.findIndex((h) => matches.some((m) => h.includes(m)));
    if (at >= 0) index[field] = at;
  }

  const unmatched = COLUMNS.filter((c) => index[c.field] === undefined).map((c) => c.field);

  const rows = lines.slice(1).map((cells) => ({
    permalink: text(cells, index.permalink),
    postedAt: text(cells, index.postedAt),
    reach: number(cells, index.reach),
    likes: number(cells, index.likes),
    comments: number(cells, index.comments),
    saves: number(cells, index.saves),
    shares: number(cells, index.shares),
    linkClicks: number(cells, index.linkClicks),
  }));

  return { rows, unmatched };
}

function text(cells: string[], at: number | undefined): string | null {
  if (at === undefined) return null;
  const value = cells[at]?.trim();
  return value ? value : null;
}

function number(cells: string[], at: number | undefined): number | null {
  const value = text(cells, at);
  if (value === null) return null;
  // Later writes "1,234" and sometimes "1.2k".
  const cleaned = value.replace(/,/g, '').trim();
  const k = /^([\d.]+)k$/i.exec(cleaned);
  if (k) return Math.round(Number(k[1]) * 1000);
  const parsed = Number(cleaned);
  return Number.isFinite(parsed) ? parsed : null;
}

/** A CSV split that copes with quoted cells containing commas and newlines. */
export function splitRows(csv: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = '';
  let quoted = false;

  for (let i = 0; i < csv.length; i += 1) {
    const char = csv[i]!;

    if (quoted) {
      if (char === '"') {
        if (csv[i + 1] === '"') {
          cell += '"';
          i += 1;
        } else {
          quoted = false;
        }
      } else {
        cell += char;
      }
      continue;
    }

    if (char === '"') quoted = true;
    else if (char === ',') {
      row.push(cell);
      cell = '';
    } else if (char === '\n') {
      row.push(cell);
      rows.push(row);
      row = [];
      cell = '';
    } else if (char !== '\r') {
      cell += char;
    }
  }

  if (cell !== '' || row.length > 0) {
    row.push(cell);
    rows.push(row);
  }

  return rows;
}
