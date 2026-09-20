import OpenAI from 'openai';
import { EMBEDDING_DIMENSIONS, embeddingModel } from './models.js';

let client: OpenAI | null = null;

function openai(): OpenAI {
  if (!client) {
    if (!process.env.OPENAI_API_KEY) {
      throw new Error('OPENAI_API_KEY is not set. See docs/TODO-LINNEA.md.');
    }
    client = new OpenAI();
  }
  return client;
}

/**
 * Text embeddings for meaning search over assets, facts and news items.
 *
 * OpenAI rather than Anthropic, because Anthropic has no embedding endpoint and
 * the OpenAI key is already needed for Whisper. 1024 dimensions because the
 * spec fixes `vector(1024)` on three tables.
 */
export async function embed(texts: string[]): Promise<number[][]> {
  if (texts.length === 0) return [];

  const res = await openai().embeddings.create({
    model: embeddingModel(),
    input: texts.map((t) => t.slice(0, 8000)),
    dimensions: EMBEDDING_DIMENSIONS,
  });

  // The API returns them in order, but it also gives an index, so sort by it
  // rather than trusting the order.
  return res.data
    .slice()
    .sort((a, b) => a.index - b.index)
    .map((d) => d.embedding);
}

export async function embedOne(text: string): Promise<number[]> {
  const [vector] = await embed([text]);
  if (!vector) throw new Error('Embedding returned nothing.');
  return vector;
}

/** pgvector wants `[1,2,3]`, not a Postgres array literal. */
export function toVector(values: number[]): string {
  return `[${values.join(',')}]`;
}
