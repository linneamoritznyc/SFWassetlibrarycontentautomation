import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';
import OpenAI from 'openai';
import { whisperModel } from './models.js';

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

export type TranscriptWord = { w: string; start: number; end: number; speaker: string | null };

export type Transcript = { language: string | null; text: string; words: TranscriptWord[] };

/** Whisper refuses anything larger than this, so audio is split before it gets here. */
export const WHISPER_MAX_BYTES = 25 * 1024 * 1024;

/**
 * Transcribes one audio file with word-level timestamps.
 *
 * `speaker` comes back null on every word: Whisper does not diarize, and
 * nothing in the OpenAI API does. The field exists because the schema and the
 * clip finder both use it, and real diarization is a Phase 8 item. Until then
 * the clip finder infers the speaker from what is being said.
 */
export async function transcribeFile(path: string, offsetS = 0): Promise<Transcript> {
  const { size } = await stat(path);
  if (size > WHISPER_MAX_BYTES) {
    throw new Error(
      `${path} is ${Math.round(size / 1e6)} MB, over Whisper's 25 MB limit. Split it first.`,
    );
  }

  const result = (await openai().audio.transcriptions.create({
    file: createReadStream(path),
    model: whisperModel(),
    response_format: 'verbose_json',
    timestamp_granularities: ['word', 'segment'],
  })) as unknown as {
    language?: string;
    text?: string;
    words?: { word: string; start: number; end: number }[];
  };

  return {
    language: result.language ?? null,
    text: result.text ?? '',
    words: (result.words ?? []).map((w) => ({
      w: w.word,
      start: w.start + offsetS,
      end: w.end + offsetS,
      speaker: null,
    })),
  };
}

/** Joins the pieces of a split file back into one transcript. */
export function mergeTranscripts(parts: Transcript[]): Transcript {
  return {
    language: parts.find((p) => p.language)?.language ?? null,
    text: parts
      .map((p) => p.text.trim())
      .filter(Boolean)
      .join(' '),
    words: parts.flatMap((p) => p.words).sort((a, b) => a.start - b.start),
  };
}
