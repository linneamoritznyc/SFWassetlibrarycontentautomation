import Anthropic from '@anthropic-ai/sdk';
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';
import type { Pool } from '@sfw/db';
import type { z } from 'zod';
import { costUsd, defaultModel } from './models.js';
import { loadPrompt } from './prompts.js';

let client: Anthropic | null = null;

function anthropic(): Anthropic {
  if (!client) {
    if (!process.env.ANTHROPIC_API_KEY) {
      throw new Error('ANTHROPIC_API_KEY is not set. See docs/TODO-LINNEA.md.');
    }
    client = new Anthropic();
  }
  return client;
}

/** A thumbnail to show Claude. Originals stay in R2 (spec section 9). */
export type ImageInput = {
  /** image/jpeg, image/png, image/webp or image/gif. */
  mediaType: 'image/jpeg' | 'image/png' | 'image/webp' | 'image/gif';
  /** Raw bytes. Base64 encoding happens here. */
  data: Buffer;
  /** Shown to Claude just before the image so it knows what it is looking at. */
  label?: string;
};

export type CallOptions<T extends z.ZodType> = {
  pool: Pool;
  /** The prompt's name in the `prompts` table. Its active version is loaded. */
  prompt: string;
  /** The zod schema the reply is constrained to and validated against. */
  schema: T;
  /** The task, as text. The prompt body becomes the system prompt. */
  input: string;
  images?: ImageInput[];
  /** Overrides the default model for this call. */
  model?: string;
  maxTokens?: number;
  /** Logged against the job in `ai_calls`, so cost is attributable. */
  jobId?: string | null;
};

/**
 * One Claude call: load the active prompt, constrain the reply to the schema,
 * validate it, and log what it cost.
 *
 * The reply is constrained server-side by the output format rather than only
 * asked for in the prompt, so malformed JSON is close to impossible. The spec
 * still asks for one repair retry, and it is here: if validation fails anyway,
 * the call is made once more with the failure quoted back. A second failure
 * throws, which fails the job, which the queue retries with backoff.
 */
export async function callClaude<T extends z.ZodType>(
  options: CallOptions<T>,
): Promise<z.infer<T>> {
  const { pool, schema, input, images = [], jobId = null } = options;
  const model = options.model ?? defaultModel();
  const prompt = await loadPrompt(pool, options.prompt);

  const content: Anthropic.MessageParam['content'] = [];
  for (const image of images) {
    if (image.label) content.push({ type: 'text', text: image.label });
    content.push({
      type: 'image',
      source: { type: 'base64', media_type: image.mediaType, data: image.data.toString('base64') },
    });
  }
  content.push({ type: 'text', text: input });

  const messages: Anthropic.MessageParam[] = [{ role: 'user', content }];

  for (let attempt = 1; attempt <= 2; attempt += 1) {
    const started = Date.now();

    const response = await anthropic().messages.parse({
      model,
      max_tokens: options.maxTokens ?? 16000,
      system: prompt.body,
      messages,
      output_config: { format: zodOutputFormat(schema) },
    });

    await logCall(pool, {
      jobId,
      promptName: prompt.name,
      promptVersion: prompt.version,
      model,
      inputTokens: response.usage.input_tokens,
      outputTokens: response.usage.output_tokens,
      latencyMs: Date.now() - started,
    });

    // Claude declined. Retrying will not change that, so fail loudly.
    if (response.stop_reason === 'refusal') {
      throw new Error(
        `Claude declined the "${prompt.name}" call: ${response.stop_details?.explanation ?? 'no reason given'}`,
      );
    }

    const parsed = schema.safeParse(response.parsed_output);
    if (parsed.success) return parsed.data;

    if (attempt === 2) {
      throw new Error(
        `"${prompt.name}" v${prompt.version} returned output that does not match its schema, twice. ` +
          parsed.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; '),
      );
    }

    // The one repair retry the spec asks for: quote the failure back.
    messages.push({ role: 'assistant', content: JSON.stringify(response.parsed_output ?? {}) });
    messages.push({
      role: 'user',
      content:
        'That did not match the schema: ' +
        parsed.error.issues.map((i) => `${i.path.join('.')} ${i.message}`).join('; ') +
        '. Send the same answer again, corrected. Change nothing else.',
    });
  }

  // Unreachable: the loop either returns or throws.
  throw new Error('unreachable');
}

type CallLog = {
  jobId: string | null;
  promptName: string;
  promptVersion: number | null;
  model: string;
  inputTokens: number;
  outputTokens: number;
  latencyMs: number;
};

/**
 * Every AI call is logged, whether or not it validated. Cost the system paid is
 * cost the system paid, and a prompt that keeps failing validation should be
 * visible as money spent.
 */
export async function logCall(pool: Pool, call: CallLog): Promise<void> {
  await pool.query(
    `insert into ai_calls
       (job_id, prompt_name, prompt_version, model, input_tokens, output_tokens, cost_usd, latency_ms)
     values ($1, $2, $3, $4, $5, $6, $7, $8)`,
    [
      call.jobId,
      call.promptName,
      call.promptVersion,
      call.model,
      call.inputTokens,
      call.outputTokens,
      costUsd(call.model, call.inputTokens, call.outputTokens),
      call.latencyMs,
    ],
  );
}
