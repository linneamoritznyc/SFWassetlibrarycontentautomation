/**
 * Gap fills and cleanup for October to December 2026 (26 Oct finishing pass).
 * Same shape and rules as CHANGES in wormhole-changes.ts.
 */
import type { Change } from './wormhole-changes';

export const GAP_CHANGES: Change[] = [
  {
    key: '2026-10-26 remove p07',
    post: 'p07',
    remove: true,
    reason: 'Removed (Linnea, 26 Oct): Dr. Caterina Capri no longer works with SFW.',
  },
  {
    key: '2026-10-26 remove p27',
    post: 'p27',
    remove: true,
    reason: 'Removed (26 Oct): duplicate of cr20261112 "Costa Rica: a day at the workshop".',
  },
];
