import type { HandlerMap } from '@sfw/queue';
import { critique } from './critique.js';
import { embed } from './embed.js';
import { extractDoc } from './extract_doc.js';
import { findClips } from './find_clips.js';
import { gapCheck } from './gap_check.js';
import { ingest } from './ingest.js';
import { pasteIntake } from './paste_intake.js';
import { proposeStory } from './propose_story.js';
import { saveFact } from './save_fact.js';
import { webFetch } from './web_fetch.js';
import { webRefresh } from './web_refresh.js';
import { write } from './write.js';

/** Everything worker-light can do today. Grows a phase at a time. */
export const handlers: HandlerMap = {
  ingest,
  embed,
  extract_doc: extractDoc,
  paste_intake: pasteIntake,
  web_fetch: webFetch,
  web_refresh: webRefresh,
  find_clips: findClips,
  propose_story: proposeStory,
  gap_check: gapCheck,
  save_fact: saveFact,
  write,
  critique,
};

export const AVAILABLE_TYPES = Object.keys(handlers);
