import type { Cadence } from '@sfw/shared';

export type Slot = {
  date: string;
  time: string;
  platform: 'instagram' | 'facebook' | 'linkedin' | 'youtube';
  format: 'feed' | 'carousel' | 'reel' | 'story' | 'linkedin' | 'short';
  /** Held back for a format or topic with under three data points. */
  exploration: boolean;
};

const DAY_NAMES = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'] as const;

/**
 * Turns the cadence into the week's actual slots.
 *
 * Mon/Wed/Fri feed posts, three or four Stories, two Shorts, one or two
 * LinkedIn. Feed posts take the morning window because that is when the
 * audience is there; Stories fill the days between.
 *
 * Pure, so the planner's arithmetic can be checked without a database. The
 * exploration share is applied by marking whole slots rather than by
 * post-processing, so the planner knows which slots it is allowed to
 * experiment in before it starts choosing.
 */
export function slotsForWeek(from: Date, cadence: Cadence): Slot[] {
  const slots: Slot[] = [];
  const morning = cadence.postingWindows[0]?.[0] ?? '08:00';
  const evening = cadence.postingWindows[1]?.[0] ?? '18:00';

  const days: { date: string; day: string }[] = [];
  for (let i = 0; i < 7; i += 1) {
    const date = new Date(from);
    date.setUTCDate(date.getUTCDate() + i);
    days.push({ date: date.toISOString().slice(0, 10), day: DAY_NAMES[date.getUTCDay()]! });
  }

  // Feed posts on the cadence days.
  for (const { date, day } of days) {
    if (cadence.feedDays.includes(day as Cadence['feedDays'][number])) {
      slots.push({
        date,
        time: morning,
        platform: 'instagram',
        format: 'feed',
        exploration: false,
      });
    }
  }

  // Stories: the top of the range, spread across the days without a feed post
  // first, then wrapping round.
  const storyCount = cadence.storiesPerWeek[1];
  const nonFeedDays = days.filter(
    (d) => !cadence.feedDays.includes(d.day as Cadence['feedDays'][number]),
  );
  const storyDays = nonFeedDays.length > 0 ? nonFeedDays : days;

  for (let i = 0; i < storyCount; i += 1) {
    const day = storyDays[i % storyDays.length]!;
    slots.push({
      date: day.date,
      time: evening,
      platform: 'instagram',
      format: 'story',
      exploration: false,
    });
  }

  // Shorts, spread across the week.
  for (let i = 0; i < cadence.shortsPerWeek; i += 1) {
    const day = days[Math.floor((i * days.length) / Math.max(cadence.shortsPerWeek, 1))]!;
    slots.push({
      date: day.date,
      time: evening,
      platform: 'youtube',
      format: 'short',
      exploration: false,
    });
  }

  // LinkedIn, at the low end of the range: it is the platform where posting
  // more of the wrong thing hurts most.
  for (let i = 0; i < cadence.linkedinPerWeek[0]; i += 1) {
    const day = days[(i * 3 + 1) % days.length]!;
    slots.push({
      date: day.date,
      time: morning,
      platform: 'linkedin',
      format: 'linkedin',
      exploration: false,
    });
  }

  slots.sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time));
  return markExploration(slots, cadence.explorationShare);
}

/**
 * Marks a share of the slots as exploration, spread evenly rather than
 * clustered, so a bad week of experiments cannot land on three consecutive
 * days.
 */
export function markExploration(slots: Slot[], share: number): Slot[] {
  const count = Math.round(slots.length * share);
  if (count <= 0) return slots;

  const step = slots.length / count;
  const marked = new Set<number>();
  for (let i = 0; i < count; i += 1) {
    marked.add(Math.min(slots.length - 1, Math.round(i * step + step / 2)));
  }

  return slots.map((slot, i) => (marked.has(i) ? { ...slot, exploration: true } : slot));
}

/**
 * relevance x freshness x material_strength x format_weight x pillar_balance,
 * the formula from backend spec section 6.
 */
export function scoreCandidate(parts: {
  relevance: number;
  /** Days since the material was created. */
  ageDays: number;
  /** How much material the story has: assets, clips, facts. */
  materialStrength: number;
  formatWeight: number;
  pillarBalance: number;
}): number {
  // Halves every three weeks, so a month-old story has to be twice as good.
  const freshness = 1 / (1 + parts.ageDays / 21);
  return (
    clamp(parts.relevance) *
    freshness *
    clamp(parts.materialStrength) *
    Math.max(parts.formatWeight, 0.01) *
    Math.max(parts.pillarBalance, 0.01)
  );
}

function clamp(value: number): number {
  return Math.min(Math.max(value, 0), 1);
}

/**
 * How far each pillar is from its share of the week. A pillar that has run
 * three times this week scores below one; a pillar that has not run scores
 * above one, so the planner pulls itself back into balance.
 */
export function pillarBalance(
  used: Record<string, number>,
  pillars: string[],
): Record<string, number> {
  const total = Object.values(used).reduce((a, b) => a + b, 0);
  const fairShare = total / pillars.length;

  const balance: Record<string, number> = {};
  for (const pillar of pillars) {
    const count = used[pillar] ?? 0;
    // +1 either side keeps this finite at the start of a week, when nothing
    // has run and every count is zero.
    balance[pillar] = (fairShare + 1) / (count + 1);
  }
  return balance;
}
