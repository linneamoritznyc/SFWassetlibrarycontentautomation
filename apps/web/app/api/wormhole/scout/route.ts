import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { guard } from '@/lib/wormhole';
import { scout } from '@/lib/scout';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
// Thirty-odd feeds at once; each is cached for three hours, so this is slow only on a cold start.
export const maxDuration = 60;

let ready = false;

/** Stories the team marked "Not for us", shared by everyone who opens Wormhole. */
async function hiddenTable() {
  if (ready) return;
  await db().query(
    `create table if not exists wormhole_news_hidden (
       url        text primary key,
       hidden_by  text not null,
       hidden_at  timestamptz not null default now()
     )`,
  );
  await db().query(`alter table wormhole_news_hidden enable row level security`);
  ready = true;
}

/** Fresh soil stories from every feed, best match first, which feeds answered, and what the team hid. */
export async function GET(request: Request) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const asked = Number(new URL(request.url).searchParams.get('days'));
  const days = Number.isFinite(asked) && asked >= 1 && asked <= 60 ? asked : 14;
  await hiddenTable();
  const [{ stories, health }, hidden] = await Promise.all([
    scout(days),
    db().query<{ url: string }>(`select url from wormhole_news_hidden`),
  ]);
  return NextResponse.json({
    stories,
    health,
    hidden: hidden.rows.map((r) => r.url),
    days,
    checked_at: new Date().toISOString(),
  });
}

/** { urls: string[], hidden: boolean } sets stories aside for the whole team, or puts them back. */
export async function POST(request: Request) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const body = (await request.json().catch(() => ({}))) as { urls?: unknown; hidden?: unknown };
  const urls = (Array.isArray(body.urls) ? body.urls : [])
    .map((u) => String(u).slice(0, 2000))
    .filter((u) => /^https?:\/\//.test(u))
    .slice(0, 500);
  if (urls.length === 0) return NextResponse.json({ error: 'Which story?' }, { status: 400 });

  await hiddenTable();
  if (body.hidden === false) {
    await db().query(`delete from wormhole_news_hidden where url = any($1::text[])`, [urls]);
  } else {
    await db().query(
      `insert into wormhole_news_hidden (url, hidden_by)
       select unnest($1::text[]), $2 on conflict (url) do nothing`,
      [urls, g.editor],
    );
  }
  return NextResponse.json({ ok: true });
}
