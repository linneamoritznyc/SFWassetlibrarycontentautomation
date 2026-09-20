import { embedOne, toVector } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { db } from '../db.js';

/**
 * Gives an asset its embedding, so "steaming compost at sunrise" finds the
 * right photo and "find similar" works.
 *
 * The text embedded is the description, the confirmed and suggested tags, the
 * people in it, and the first part of any transcript. Idempotent: the same
 * asset produces the same text produces the same vector.
 */
export const embed = handler<{ asset_id: string }>(async ({ job }) => {
  const pool = db();
  const assetId = job.payload.asset_id;

  const { rows } = await pool.query<{ text: string }>(
    `select concat_ws(E'\\n',
              a.description,
              a.notes,
              (select string_agg(t.facet || ': ' || t.name, ', ' order by t.facet, t.name)
                 from asset_tags at join tags t on t.id = at.tag_id
                where at.asset_id = a.id),
              (select 'people: ' || string_agg(p.name, ', ' order by p.name)
                 from asset_people ap join people p on p.id = ap.person_id
                where ap.asset_id = a.id),
              (select left(tr.text, 4000) from transcripts tr where tr.asset_id = a.id)
            ) as text
     from assets a where a.id = $1`,
    [assetId],
  );

  const text = rows[0]?.text?.trim();
  if (!text) {
    // Nothing to describe yet. Not an error: ingest may still be waiting, and
    // the next status change will enqueue this again.
    console.log(`[embed] asset ${assetId} has no text yet, skipping`);
    return;
  }

  const vector = await embedOne(text);
  await pool.query('update assets set embedding = $2::vector where id = $1', [
    assetId,
    toVector(vector),
  ]);
});
