import type { HandlerMap } from '@sfw/queue';
import { buildPost } from './build_post.js';
import { cutClip } from './cut_clip.js';
import { proxy } from './proxy.js';
import { transcribe } from './transcribe.js';

/** Everything worker-media can do today. */
export const handlers: HandlerMap = {
  proxy,
  transcribe,
  cut_clip: cutClip,
  build_post: buildPost,
};

export const AVAILABLE_TYPES = Object.keys(handlers);
