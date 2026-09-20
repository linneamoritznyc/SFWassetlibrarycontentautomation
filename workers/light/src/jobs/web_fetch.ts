import { createHash } from 'node:crypto';
import { callClaude, embed as embedTexts, extractFactsSchema, toVector } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { db } from '../db.js';
import { fetchPage } from '../fetch-page.js';

const CHUNK_CHARS = 12_000;

/**
 * Fetches one URL and turns it into sourced facts.
 *
 * This is the single-page version of `web_refresh`. It is what a pasted link
 * runs through: fetch the page, hash it, and if the text has changed, extract
 * facts from it. Facts from a previous read of the same URL are retired rather
 * than deleted, so a caption that cited one can still be traced.
 *
 * Whoever published the page keeps their claim: the fact text carries the page
 * title, and `propose_story` is told to cite rather than absorb it.
 */
export const webFetch = handler<{ url: string; from_asset_id?: string }>(
  async ({ job, enqueue }) => {
    const pool = db();
    const { url } = job.payload;

    const page = await fetchPage(url);
    const hash = createHash('sha256').update(page.text).digest('hex');

    const source = await pool.query<{ id: number; content_hash: string | null }>(
      `insert into sources (kind, ref, title, fetched_at, content_hash)
     values ('url', $1, $2, now(), null)
     on conflict (kind, ref) do update set title = excluded.title, fetched_at = now()
     returning id, content_hash`,
      [url, page.title || url],
    );

    const sourceId = source.rows[0]!.id;
    const unchanged = source.rows[0]!.content_hash === hash;

    if (!unchanged) {
      if (page.text.length < 200) {
        throw new Error(
          `${url} gave only ${page.text.length} characters of text. It probably renders client-side.`,
        );
      }

      const extracted: {
        subject: string;
        predicate: string;
        object: string;
        text: string;
        page: string;
        confidence: number;
        conflict: boolean;
      }[] = [];

      for (const part of chunkText(page.text)) {
        const result = await callClaude({
          pool,
          jobId: job.id,
          prompt: 'extract_facts',
          schema: extractFactsSchema,
          input: [`Page: ${page.title || url}`, `URL: ${url}`, '', part].join('\n'),
        });
        extracted.push(...result.facts);
      }

      const keep = extracted.filter((f) => f.confidence >= 0.5);
      const vectors = keep.length ? await embedTexts(keep.map((f) => f.text)) : [];

      const client = await pool.connect();
      try {
        await client.query('begin');
        await client.query(
          `update facts set status = 'retired', valid_to = now()
         where source_id = $1 and status <> 'retired'`,
          [sourceId],
        );

        for (const [i, fact] of keep.entries()) {
          await client.query(
            `insert into facts
             (subject, predicate, object, text, source_id, confidence, status, embedding)
           values ($1, $2, $3, $4, $5, $6, $7, $8::vector)`,
            [
              fact.subject,
              fact.predicate,
              fact.object,
              `${fact.text} (${page.title || url})`,
              sourceId,
              fact.confidence,
              fact.conflict ? 'conflict' : 'active',
              toVector(vectors[i]!),
            ],
          );
        }

        await client.query('update sources set content_hash = $2 where id = $1', [sourceId, hash]);
        await client.query('commit');
      } catch (err) {
        await client.query('rollback');
        throw err;
      } finally {
        client.release();
      }
    }

    // A link somebody pasted is a candidate for a post. Deciding that is
    // propose_story's job, which arrives in Phase 4; until then this queues.
    if (job.payload.from_asset_id) {
      await enqueue({
        type: 'propose_story',
        payload: { source_id: sourceId, from_asset_id: job.payload.from_asset_id },
        dedupeKey: `propose_story:${sourceId}:${job.payload.from_asset_id}`,
      });
    }
  },
);

function chunkText(text: string): string[] {
  const chunks: string[] = [];
  for (let i = 0; i < text.length; i += CHUNK_CHARS) {
    chunks.push(text.slice(i, i + CHUNK_CHARS));
  }
  return chunks;
}
