// Loads the planned posts into Wormhole. Safe to run again: posts that already
// exist are left alone, so nobody's edits get overwritten.
//   DATABASE_URL=... node scripts/wormhole-seed.mjs
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const pg = createRequire(new URL('../packages/db/package.json', import.meta.url))('pg');
import { toRow } from './wormhole-seed-rows.mjs';

const posts = JSON.parse(readFileSync(new URL('../supabase/seed/wormhole-posts.json', import.meta.url)));
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL, ssl: /localhost|127\.0\.0\.1/.test(process.env.DATABASE_URL ?? '') ? undefined : { rejectUnauthorized: false } });
let added = 0;
for (const p of posts) {
  const r = toRow(p);
  const res = await pool.query(
    `insert into wormhole_posts (id, iso_date, topic, platform, caption, slides, cta, link, sources, visual_note, note, status)
     values ($1,$2,$3,$4,$5,$6::jsonb,$7,$8,$9::jsonb,$10,$11,$12) on conflict (id) do nothing`,
    [r.id, r.iso_date, r.topic, r.platform, r.caption, JSON.stringify(r.slides), r.cta, r.link,
     JSON.stringify(r.sources), r.visual_note, r.note, r.status],
  );
  added += res.rowCount;
}
console.log(`Wormhole: ${added} new posts, ${posts.length - added} already there.`);
await pool.end();
