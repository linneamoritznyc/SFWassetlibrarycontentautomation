import { callClaude, embedOne, proposeStorySchema, toVector } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { DEFAULT_QUESTION_RECIPIENT } from '@sfw/shared';
import { BRAND_RULES } from '@sfw/prompts';
import { db } from '../db.js';

/** Below this, it is not a story, it is a link somebody found interesting. */
const WORTH_A_SLOT = 0.5;

/**
 * Decides whether something that came in has a post in it, and what the angle
 * would be.
 *
 * This is where a pasted link becomes work. It gets the facts extracted from
 * the page, the library assets that came closest on a meaning search, and the
 * brand rules, and it has to choose a pillar, a platform and a visual.
 *
 * The rule that matters: it may only choose a visual from the library assets it
 * was given. Neither the screenshot nor the linked page's own photograph is
 * allowed to carry a post. If nothing fits, the story stalls with a shot-list
 * note rather than borrowing someone else's picture.
 */
export const proposeStory = handler<{ source_id: number; from_asset_id?: string }>(
  async ({ job }) => {
    const pool = db();
    const sourceId = job.payload.source_id;

    const sourceRows = await pool.query<{ id: number; ref: string; title: string | null }>(
      'select id, ref, title from sources where id = $1',
      [sourceId],
    );
    const source = sourceRows.rows[0];
    if (!source) throw new Error(`No source ${sourceId}`);

    const facts = await pool.query<{ id: number; text: string }>(
      `select id, text from facts where source_id = $1 and status = 'active' order by confidence desc limit 40`,
      [sourceId],
    );

    if (facts.rows.length === 0) {
      console.log(
        `[propose_story] nothing was extracted from ${source.ref}, so there is nothing to propose`,
      );
      return;
    }

    // What the library has that is close to this, cleared and not yet used.
    const gist = [source.title, ...facts.rows.slice(0, 8).map((f) => f.text)]
      .filter(Boolean)
      .join('. ');
    const vector = toVector(await embedOne(gist));

    const candidates = await pool.query<{
      id: string;
      description: string | null;
      workshop: string | null;
    }>(
      `select a.id, a.description, b.workshop
       from assets a left join batches b on b.id = a.batch_id
       where a.embedding is not null
         and a.type in ('photo', 'clip', 'video', 'graphic')
         and a.status in ('cleared', 'tagged')
       order by a.embedding <=> $1::vector
       limit 12`,
      [vector],
    );

    const pasted = job.payload.from_asset_id
      ? (
          await pool.query<{ description: string | null; notes: string | null }>(
            'select description, notes from assets where id = $1',
            [job.payload.from_asset_id],
          )
        ).rows[0]
      : null;

    const result = await callClaude({
      pool,
      jobId: job.id,
      prompt: 'propose_story',
      schema: proposeStorySchema,
      input: JSON.stringify(
        {
          came_in_as: pasted
            ? { kind: 'pasted screenshot', summary: pasted.description, notes: pasted.notes }
            : { kind: 'link' },
          source: { url: source.ref, title: source.title },
          facts: facts.rows,
          library_assets: candidates.rows,
          brand: BRAND_RULES.slice(0, 400),
        },
        null,
        2,
      ),
    });

    if (!result.has_story || result.score < WORTH_A_SLOT) {
      await pool.query(
        `update assets set notes = concat_ws(E'\\n', nullif(notes, ''), $2) where id = $1`,
        [
          job.payload.from_asset_id ?? null,
          `No story here: ${result.no_story_reason || 'too thin'}`,
        ],
      );
      console.log(`[propose_story] no story in ${source.ref}: ${result.no_story_reason}`);
      return;
    }

    // Only assets that were actually offered. A hallucinated id would become a
    // post with a picture nobody chose.
    const offered = new Set(candidates.rows.map((c) => c.id));
    const assetIds = result.asset_ids.filter((id) => offered.has(id));

    const story = await pool.query<{ id: number }>(
      `insert into stories
         (origin, origin_ref, angle, pillar, material_asset_ids, material_fact_ids, score, status)
       values ('news', $1, $2, $3, $4::uuid[], $5::int[], $6, 'candidate')
       returning id`,
      [
        String(sourceId),
        [result.angle, result.attribution && `Credit: ${result.attribution}`]
          .filter(Boolean)
          .join(' '),
        result.pillar,
        assetIds,
        result.fact_ids.filter((id) => facts.rows.some((f) => f.id === id)),
        result.score,
      ],
    );

    const storyId = story.rows[0]!.id;

    for (const question of result.questions) {
      await pool.query(
        `insert into questions (text, asked_to, context, status)
         values ($1,
                 coalesce((select id from people where $2 = any(topics) limit 1),
                          (select id from people where name = $3)),
                 $4::jsonb, 'open')`,
        [
          question.question,
          question.topic,
          DEFAULT_QUESTION_RECIPIENT,
          JSON.stringify({ story_id: storyId, topic: question.topic }),
        ],
      );
    }

    if (assetIds.length === 0 && result.material_needed) {
      await pool.query(
        `insert into questions (text, asked_to, context, status)
         values ($1, (select id from people where 'partners' = any(topics) limit 1), $2::jsonb, 'open')`,
        [
          `Which image should carry this? ${result.material_needed}`,
          JSON.stringify({ story_id: storyId, topic: 'material' }),
        ],
      );
    }

    console.log(
      `[propose_story] story ${storyId} from ${source.ref}: ${result.platform}, ${result.pillar}` +
        (assetIds.length === 0 ? ' (no visual yet, asked for one)' : ''),
    );
  },
);
