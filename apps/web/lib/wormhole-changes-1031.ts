/**
 * 31 Oct 2026 (Linnea): remove every Instagram Story ("all the IG stories are damn ugly"),
 * and the two placeholder posts she approved for deletion.
 */
import type { Change } from './wormhole-changes';

const STORIES = [
  'st20261026', 'st20261029', 'st20261102', 'st20261103', 'st20261104', 'st20261112',
  'st20261116', 'st20261123', 'st20261201', 'k20261205', 'j20270110b', 'st20270111',
  'j20270118', 'j20270130b', 'd15',
];

export const OCT31_CHANGES: Change[] = [
  ...STORIES.map((post) => ({
    key: `2026-10-31 remove story ${post}`,
    post,
    remove: true as const,
    reason: 'Removed (Linnea, 31 Oct): all old Instagram Stories are off brand.',
  })),
  {
    key: '2026-10-31 remove pl20261107',
    post: 'pl20261107',
    remove: true,
    reason: 'Removed (Linnea, 31 Oct): Field Notes #1 was still a placeholder.',
  },
  {
    key: '2026-10-31 remove pl20261125',
    post: 'pl20261125',
    remove: true,
    reason: 'Removed (Linnea, 31 Oct): mentor spotlight placeholder, repeats the mentor series.',
  },
];
