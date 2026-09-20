/**
 * Model ids and what they cost.
 *
 * The ids come from `.env.example` so a model swap is a config change, not a
 * code change. The defaults are the ones the build prompt asked for.
 *
 * Prices are US dollars per million tokens, from the Anthropic pricing table
 * (June 2026). They are used only to fill in `ai_calls.cost_usd`, which drives
 * the per-clip cost in the Clips header and the cost line in the Monday email.
 * If a price moves, change it here; nothing else reads it.
 */

export type ModelPrice = { input: number; output: number };

export const PRICES: Record<string, ModelPrice> = {
  'claude-opus-5': { input: 5, output: 25 },
  'claude-opus-4-8': { input: 5, output: 25 },
  'claude-sonnet-5': { input: 2, output: 10 },
  'claude-sonnet-4-6': { input: 3, output: 15 },
  'claude-haiku-4-5': { input: 1, output: 5 },
};

/** Tagging, clip finding, writing, critiquing, planning: most of the system. */
export function defaultModel(): string {
  return process.env.ANTHROPIC_MODEL_DEFAULT ?? 'claude-sonnet-4-6';
}

/** Scout ranking. High volume, low judgement. */
export function cheapModel(): string {
  return process.env.ANTHROPIC_MODEL_CHEAP ?? 'claude-haiku-4-5';
}

/** Articles, per the spec's "opus for articles". */
export function longformModel(): string {
  return process.env.ANTHROPIC_MODEL_LONGFORM ?? 'claude-opus-5';
}

export function costUsd(model: string, inputTokens: number, outputTokens: number): number {
  const price = PRICES[model];
  // An unknown model is logged at zero rather than guessed at. The token counts
  // are still recorded, so the cost can be worked out later.
  if (!price) return 0;
  return (inputTokens * price.input + outputTokens * price.output) / 1_000_000;
}

/** Embeddings. OpenAI, because Anthropic has no embedding endpoint. */
export function embeddingModel(): string {
  return process.env.OPENAI_EMBEDDING_MODEL ?? 'text-embedding-3-small';
}

/** The spec fixes vector(1024) on assets, facts and news_items. */
export const EMBEDDING_DIMENSIONS = 1024;

export function whisperModel(): string {
  return process.env.OPENAI_WHISPER_MODEL ?? 'whisper-1';
}
