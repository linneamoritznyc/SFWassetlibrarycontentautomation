import { embedOne, toVector } from '@sfw/ai';
import { BRAND_RULES } from '@sfw/prompts';
import { presignGet } from '@sfw/storage';
import type { Pool } from '@sfw/db';

export type BriefAsset = {
  id: string;
  type: string;
  description: string | null;
  credit_line: string | null;
  workshop: string | null;
  release_status: string;
  thumb_key: string | null;
  thumb_url?: string | null;
};

export type BriefFact = { id: number; text: string; source: string | null; confidence: number };

export type BriefPost = {
  id: string;
  platform: string;
  format: string;
  slot_date: string | null;
  slot_time: string | null;
};

export type Briefing = {
  story: {
    id: number;
    angle: string | null;
    pillar: string | null;
    origin: string;
    origin_ref: string | null;
  };
  post?: BriefPost;
  assets: BriefAsset[];
  facts: BriefFact[];
  rules: string[];
  examples: { hook: string | null; caption: string | null; saves: number | null }[];
  brand: string;
  calendar_context: { upcoming: { title: string; when: string }[] };
  people: string[];
};

/**
 * Builds the briefing packet a writer gets, per backend spec section 6.
 *
 * Facts come from three places, in this order: the ones linked to the story
 * outright, the top fifteen by meaning against the angle, and everything known
 * about whoever is in the chosen images. The third is what stops a post naming
 * someone and then getting their role wrong.
 *
 * Used as a step inside `write`, and callable on its own so a briefing can be
 * looked at without writing anything.
 */
export async function buildBrief(
  pool: Pool,
  storyId: number,
  options: { postId?: string; withThumbUrls?: boolean } = {},
): Promise<Briefing> {
  const storyRows = await pool.query<{
    id: number;
    angle: string | null;
    pillar: string | null;
    origin: string;
    origin_ref: string | null;
    material_asset_ids: string[];
    material_fact_ids: number[];
  }>(
    `select id, angle, pillar, origin, origin_ref, material_asset_ids, material_fact_ids
     from stories where id = $1`,
    [storyId],
  );

  const story = storyRows.rows[0];
  if (!story) throw new Error(`No story ${storyId}`);

  const post = options.postId
    ? (
        await pool.query<BriefPost>(
          `select id, platform, format, slot_date::text, slot_time::text
           from posts where id = $1`,
          [options.postId],
        )
      ).rows[0]
    : undefined;

  // The assets are whatever the post chose, falling back to the story's.
  const assetIds = post
    ? ((
        await pool.query<{ asset_ids: string[] }>('select asset_ids from posts where id = $1', [
          post.id,
        ])
      ).rows[0]?.asset_ids ?? [])
    : story.material_asset_ids;

  const assets = assetIds.length
    ? (
        await pool.query<BriefAsset>(
          `select a.id, a.type, a.description, a.credit_line, a.release_status, a.thumb_key,
                  b.workshop
           from assets a left join batches b on b.id = a.batch_id
           where a.id = any($1::uuid[])`,
          [assetIds],
        )
      ).rows
    : [];

  if (options.withThumbUrls) {
    for (const asset of assets) {
      asset.thumb_url = asset.thumb_key ? await presignGet('sfw-media', asset.thumb_key) : null;
    }
  }

  const people = assets.length
    ? (
        await pool.query<{ name: string }>(
          `select distinct p.name
           from asset_people ap join people p on p.id = ap.person_id
           where ap.asset_id = any($1::uuid[]) and ap.confirmed`,
          [assetIds],
        )
      ).rows.map((r) => r.name)
    : [];

  const facts = await selectFacts(pool, story, people);

  const scope = post ? scopeFor(post.platform, post.format) : 'all';
  const rules = (
    await pool.query<{ text: string }>(
      `select text from rules where active and scope in ('all', $1) order by applied_count desc, created_at`,
      [scope],
    )
  ).rows.map((r) => r.text);

  // The three best past posts of this shape, by saves. What good looked like.
  const examples = post
    ? (
        await pool.query<{ hook: string | null; caption: string | null; saves: number | null }>(
          `select p.hook, p.caption, max(m.saves) as saves
           from posts p
           left join metrics m on m.post_id = p.id
           where p.status in ('approved', 'exported', 'published')
             and p.format = $1 and p.platform = $2 and p.caption is not null
           group by p.id, p.hook, p.caption
           order by (p.is_example) desc, max(m.saves) desc nulls last
           limit 3`,
          [post.format, post.platform],
        )
      ).rows
    : [];

  const upcoming = (
    await pool.query<{ title: string; when: string }>(
      `select f.text as title, coalesce(f.valid_from::text, f.created_at::text) as when
       from facts f
       where f.status = 'active'
         and (f.predicate ilike '%date%' or f.predicate ilike '%runs%' or f.predicate ilike '%closes%')
       order by f.valid_from nulls last
       limit 8`,
    )
  ).rows;

  return {
    story: {
      id: story.id,
      angle: story.angle,
      pillar: story.pillar,
      origin: story.origin,
      origin_ref: story.origin_ref,
    },
    post,
    assets,
    facts,
    rules,
    examples,
    brand: BRAND_RULES,
    calendar_context: { upcoming },
    people,
  };
}

async function selectFacts(
  pool: Pool,
  story: { angle: string | null; material_fact_ids: number[] },
  people: string[],
): Promise<BriefFact[]> {
  const byId = new Map<number, BriefFact>();

  const add = (rows: BriefFact[]) => {
    for (const row of rows) if (!byId.has(row.id)) byId.set(row.id, row);
  };

  const select = `select f.id, f.text, s.ref as source, f.confidence
                  from facts f left join sources s on s.id = f.source_id
                  where f.status = 'active'`;

  // 1. Linked outright.
  if (story.material_fact_ids.length > 0) {
    add(
      (
        await pool.query<BriefFact>(`${select} and f.id = any($1::int[])`, [
          story.material_fact_ids,
        ])
      ).rows,
    );
  }

  // 2. Closest fifteen by meaning against the angle.
  if (story.angle) {
    const vector = toVector(await embedOne(story.angle));
    add(
      (
        await pool.query<BriefFact>(
          `${select} and f.embedding is not null order by f.embedding <=> $1::vector limit 15`,
          [vector],
        )
      ).rows,
    );
  }

  // 3. Everything about whoever is in the pictures.
  if (people.length > 0) {
    add((await pool.query<BriefFact>(`${select} and f.subject = any($1::text[])`, [people])).rows);
  }

  return [...byId.values()];
}

/** Which rule scope applies to a post. */
export function scopeFor(platform: string, format: string): string {
  if (platform === 'linkedin') return 'linkedin';
  if (format === 'reel' || format === 'short') return 'reel';
  if (platform === 'instagram') return 'instagram';
  return 'caption';
}
