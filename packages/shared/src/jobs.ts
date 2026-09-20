/**
 * Every job type, and which worker claims it. A worker process is told what to
 * claim through WORKER_TYPES, so one image can run as several workers.
 */

export const JOB_TYPES = {
  light: [
    'ingest',
    'embed',
    'extract_doc',
    'find_clips',
    'brief',
    'gap_check',
    'save_fact',
    'web_refresh',
    'web_fetch',
    'paste_intake',
    'propose_story',
    'scout_fetch',
    'scout_rank',
    'plan_week',
    'write',
    'critique',
    'write_batch',
    'canva_push',
    'canva_pull',
    'export_bundle',
    'link_asset_usage',
    'results_pull',
    'log_edit',
    'log_rejection',
    'learn_weekly',
    'eval_nightly',
    'review_ready_notify',
    'questions_nudge',
  ],
  media: ['proxy', 'transcribe', 'cut_clip', 'build_post'],
  render: ['render_reel'],
} as const;

export type WorkerKind = keyof typeof JOB_TYPES;

export const ALL_JOB_TYPES: string[] = Object.values(JOB_TYPES).flat();

/** Clip ratios, in the order the Clips view offers them. */
export const CLIP_RATIOS = ['9x16', '4x5', '1x1', '16x9'] as const;

export type ClipRatio = (typeof CLIP_RATIOS)[number];
