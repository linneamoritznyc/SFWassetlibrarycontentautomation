import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { getAsset } from '@/lib/assets';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

/** Reads the database on every call, so it is never prerendered. */
export const dynamic = 'force-dynamic';

type Params = { params: Promise<{ id: string }> };

export const GET = route(async (_request: NextRequest, { params }: Params) => {
  const { id } = await params;
  const asset = await getAsset(id);
  if (!asset) return fail('No such asset', 404);
  return NextResponse.json(asset);
});

type Patch = {
  description?: string;
  notes?: string;
  status?: string;
  quality?: number | null;
  releaseStatus?: string;
  heroCandidate?: boolean;
  creditLine?: string;
  driveLink?: string;
  /** Accept every AI suggestion on this asset. */
  acceptAllTags?: boolean;
  /** Confirm or remove individual tags, as "facet:name". */
  confirmTags?: string[];
  rejectTags?: string[];
  addTags?: string[];
  confirmPeople?: string[];
  rejectPeople?: string[];
};

const FIELDS: { key: keyof Patch; column: string }[] = [
  { key: 'description', column: 'description' },
  { key: 'notes', column: 'notes' },
  { key: 'status', column: 'status' },
  { key: 'quality', column: 'quality' },
  { key: 'releaseStatus', column: 'release_status' },
  { key: 'heroCandidate', column: 'hero_candidate' },
  { key: 'creditLine', column: 'credit_line' },
  { key: 'driveLink', column: 'drive_link' },
];

/**
 * Everything a human can change about an asset: the fields, the tags, the
 * people, the status.
 *
 * Confirming a tag flips `confirmed` and leaves `source` alone, so the library
 * still knows the AI suggested it and `learn_weekly` can see how often its
 * suggestions survive. Rejecting deletes the row outright: a rejected
 * suggestion should not come back the next time ingest runs, and ingest only
 * clears its own unconfirmed rows.
 */
export const PATCH = route(async (request: NextRequest, { params }: Params) => {
  const { id } = await params;
  const body = (await request.json()) as Patch;
  const pool = db();
  const client = await pool.connect();

  try {
    await client.query('begin');

    const sets: string[] = [];
    const values: unknown[] = [id];

    for (const { key, column } of FIELDS) {
      if (body[key] !== undefined) {
        values.push(body[key]);
        sets.push(`${column} = $${values.length}`);
      }
    }

    if (sets.length > 0) {
      await client.query(`update assets set ${sets.join(', ')} where id = $1`, values);
    }

    if (body.acceptAllTags) {
      await client.query(
        `update asset_tags set confirmed = true where asset_id = $1 and source = 'ai'`,
        [id],
      );
      await client.query(
        `update asset_people set confirmed = true where asset_id = $1 and source = 'ai'`,
        [id],
      );
    }

    for (const tag of body.confirmTags ?? []) {
      const [facet, ...rest] = tag.split(':');
      await client.query(
        `update asset_tags set confirmed = true
         where asset_id = $1
           and tag_id = (select id from tags where facet = $2 and name = $3)`,
        [id, facet, rest.join(':')],
      );
    }

    for (const tag of body.rejectTags ?? []) {
      const [facet, ...rest] = tag.split(':');
      await client.query(
        `delete from asset_tags
         where asset_id = $1 and tag_id = (select id from tags where facet = $2 and name = $3)`,
        [id, facet, rest.join(':')],
      );
    }

    for (const tag of body.addTags ?? []) {
      const [facet, ...rest] = tag.split(':');
      await client.query(
        `insert into asset_tags (asset_id, tag_id, source, confirmed, confidence)
         select $1, t.id, 'human', true, 1.0 from tags t where t.facet = $2 and t.name = $3
         on conflict (asset_id, tag_id) do update set confirmed = true, source = 'human'`,
        [id, facet, rest.join(':')],
      );
    }

    for (const name of body.confirmPeople ?? []) {
      await client.query(
        `insert into asset_people (asset_id, person_id, source, confirmed)
         select $1, p.id, 'human', true from people p where p.name = $2
         on conflict (asset_id, person_id) do update set confirmed = true`,
        [id, name],
      );
    }

    for (const name of body.rejectPeople ?? []) {
      await client.query(
        `delete from asset_people
         where asset_id = $1 and person_id = (select id from people where name = $2)`,
        [id, name],
      );
    }

    await client.query('commit');
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }

  // Tags and description feed the embedding, so anything a human changed means
  // the vector is stale. The dedupe key keeps this to one job per asset.
  await enqueue(pool, { type: 'embed', payload: { asset_id: id }, dedupeKey: `embed:${id}` });

  const asset = await getAsset(id);
  return NextResponse.json(asset);
});
