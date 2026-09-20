import type { HandlerMap } from '@sfw/queue';
import { canvaPull } from './canva_pull.js';
import { canvaPush } from './canva_push.js';
import { critique } from './critique.js';
import { embed } from './embed.js';
import { exportBundle } from './export_bundle.js';
import { extractDoc } from './extract_doc.js';
import { findClips } from './find_clips.js';
import { evalNightly } from './eval_nightly.js';
import { gapCheck } from './gap_check.js';
import { ingest } from './ingest.js';
import { learnWeekly } from './learn_weekly.js';
import { linkAssetUsage } from './link_asset_usage.js';
import { logEdit } from './log_edit.js';
import { logRejection } from './log_rejection.js';
import { pasteIntake } from './paste_intake.js';
import { planWeek } from './plan_week.js';
import { proposeStory } from './propose_story.js';
import { questionsNudge } from './questions_nudge.js';
import { resultsPull } from './results_pull.js';
import { reviewReadyNotify } from './review_ready_notify.js';
import { saveFact } from './save_fact.js';
import { webFetch } from './web_fetch.js';
import { webRefresh } from './web_refresh.js';
import { write } from './write.js';
import { writeBatch } from './write_batch.js';

/** Everything worker-light can do today. Grows a phase at a time. */
export const handlers: HandlerMap = {
  // Material
  ingest,
  embed,
  extract_doc: extractDoc,
  // Paste and knowledge
  paste_intake: pasteIntake,
  web_fetch: webFetch,
  web_refresh: webRefresh,
  propose_story: proposeStory,
  gap_check: gapCheck,
  save_fact: saveFact,
  // Clips
  find_clips: findClips,
  // Writing
  write,
  write_batch: writeBatch,
  critique,
  // Canva
  canva_push: canvaPush,
  canva_pull: canvaPull,
  // Planning and distribution
  plan_week: planWeek,
  export_bundle: exportBundle,
  link_asset_usage: linkAssetUsage,
  // Learning
  log_edit: logEdit,
  log_rejection: logRejection,
  learn_weekly: learnWeekly,
  eval_nightly: evalNightly,
  // Results and notices
  results_pull: resultsPull,
  review_ready_notify: reviewReadyNotify,
  questions_nudge: questionsNudge,
};

export const AVAILABLE_TYPES = Object.keys(handlers);
