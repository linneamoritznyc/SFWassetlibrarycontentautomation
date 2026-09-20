import type { HandlerMap } from '@sfw/queue';
import { renderReel } from './render_reel.js';

/** worker-render does one thing, and it needs a whole browser to do it. */
export const handlers: HandlerMap = { render_reel: renderReel };

export const AVAILABLE_TYPES = Object.keys(handlers);
