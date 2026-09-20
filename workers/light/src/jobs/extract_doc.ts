import { createHash } from 'node:crypto';
import { callClaude, embed as embedTexts, extractFactsSchema, toVector } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { getObject, type Bucket } from '@sfw/storage';
import { extractText, getDocumentProxy } from 'unpdf';
import { db } from '../db.js';

/** Roughly 12k characters a chunk, so a long report is a handful of calls. */
const CHUNK_CHARS = 12_000;

/**
 * Turns a PDF into sourced facts.
 *
 * The document becomes one `sources` row, its text is chunked, and Claude
 * pulls atomic facts out of each chunk with a page reference. Facts it flags as
 * contradicting something else in the same chunk land as `conflict` for the
 * weekly review rather than being silently picked between.
 *
 * Idempotent through the content hash: a document whose text has not changed
 * is skipped rather than re-extracted, so the same facts are not created twice.
 */
export const extractDoc = handler<{ asset_id: string; force?: boolean }>(async ({ job }) => {
  const pool = db();
  const assetId = job.payload.asset_id;

  const { rows } = await pool.query<{
    id: string;
    filename: string;
    bucket: Bucket;
    r2_key: string;
  }>('select id, filename, bucket, r2_key from assets where id = $1 and type = $2', [
    assetId,
    'doc',
  ]);

  const asset = rows[0];
  if (!asset) throw new Error(`No document asset ${assetId}`);

  const file = await getObject(asset.bucket, asset.r2_key);
  const pdf = await getDocumentProxy(new Uint8Array(file));
  const { text: pages } = await extractText(pdf, { mergePages: false });

  const fullText = pages.join('\n\n').trim();
  if (!fullText) throw new Error(`No text in ${asset.filename}. A scan needs OCR first.`);

  const hash = createHash('sha256').update(fullText).digest('hex');

  const source = await pool.query<{ id: number; content_hash: string | null }>(
    `insert into sources (kind, ref, title, fetched_at, content_hash)
     values ('doc', $1, $2, now(), $3)
     on conflict (kind, ref) do update set title = excluded.title, fetched_at = now()
     returning id, content_hash`,
    [assetId, asset.filename, hash],
  );

  const sourceId = source.rows[0]!.id;
  const previousHash = source.rows[0]!.content_hash;

  if (previousHash === hash && !job.payload.force) {
    console.log(`[extract_doc] ${asset.filename} unchanged, nothing to re-extract`);
    return;
  }

  const chunks = chunkPages(pages);
  const extracted: {
    text: string;
    subject: string;
    predicate: string;
    object: string;
    page: string;
    confidence: number;
    conflict: boolean;
  }[] = [];

  for (const chunk of chunks) {
    const result = await callClaude({
      pool,
      jobId: job.id,
      prompt: 'extract_facts',
      schema: extractFactsSchema,
      input: [
        `Document: ${asset.filename}`,
        `Pages ${chunk.firstPage} to ${chunk.lastPage}.`,
        '',
        chunk.text,
      ].join('\n'),
    });
    extracted.push(...result.facts);
  }

  if (extracted.length === 0) {
    await pool.query('update sources set content_hash = $2 where id = $1', [sourceId, hash]);
    return;
  }

  const vectors = await embedTexts(extracted.map((f) => f.text));

  const client = await pool.connect();
  try {
    await client.query('begin');

    // Re-extraction supersedes the previous pass over the same document.
    await client.query(
      `update facts set status = 'retired', valid_to = now()
       where source_id = $1 and status <> 'retired'`,
      [sourceId],
    );

    for (const [i, fact] of extracted.entries()) {
      if (fact.confidence < 0.5) continue;
      await client.query(
        `insert into facts
           (subject, predicate, object, text, source_id, confidence, status, embedding)
         values ($1, $2, $3, $4, $5, $6, $7, $8::vector)`,
        [
          fact.subject,
          fact.predicate,
          fact.object,
          `${fact.text} (${asset.filename}, ${fact.page})`,
          sourceId,
          fact.confidence,
          fact.conflict ? 'conflict' : 'active',
          toVector(vectors[i]!),
        ],
      );
    }

    await client.query('update sources set content_hash = $2 where id = $1', [sourceId, hash]);
    await client.query(`update assets set status = 'tagged' where id = $1 and status = 'inbox'`, [
      assetId,
    ]);

    await client.query('commit');
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }
});

type Chunk = { text: string; firstPage: number; lastPage: number };

/** Splits on page boundaries, so a fact can always cite a real page. */
function chunkPages(pages: string[]): Chunk[] {
  const chunks: Chunk[] = [];
  let current = '';
  let firstPage = 1;

  for (const [index, page] of pages.entries()) {
    const pageNumber = index + 1;
    const block = `[page ${pageNumber}]\n${page}\n\n`;

    if (current && current.length + block.length > CHUNK_CHARS) {
      chunks.push({ text: current.trim(), firstPage, lastPage: pageNumber - 1 });
      current = '';
      firstPage = pageNumber;
    }
    current += block;
  }

  if (current.trim()) {
    chunks.push({ text: current.trim(), firstPage, lastPage: pages.length });
  }
  return chunks;
}
