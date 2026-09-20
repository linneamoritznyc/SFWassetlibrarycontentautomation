import type { HandlerMap } from '@sfw/queue';
import { embed } from './embed.js';
import { extractDoc } from './extract_doc.js';
import { findClips } from './find_clips.js';
import { ingest } from './ingest.js';
import { pasteIntake } from './paste_intake.js';
import { webFetch } from './web_fetch.js';

/** Everything worker-light can do today. Grows a phase at a time. */
export const handlers: HandlerMap = {
  ingest,
  embed,
  extract_doc: extractDoc,
  find_clips: findClips,
  paste_intake: pasteIntake,
  web_fetch: webFetch,
};

export const AVAILABLE_TYPES = Object.keys(handlers);
