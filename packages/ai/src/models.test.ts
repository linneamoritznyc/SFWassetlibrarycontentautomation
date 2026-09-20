import { describe, expect, it } from 'vitest';
import { PRICES, costUsd } from './models.js';

describe('cost', () => {
  it('prices a call in dollars per million tokens', () => {
    // Sonnet 4.6 at $3 in / $15 out.
    expect(costUsd('claude-sonnet-4-6', 1_000_000, 0)).toBeCloseTo(3);
    expect(costUsd('claude-sonnet-4-6', 0, 1_000_000)).toBeCloseTo(15);
    expect(costUsd('claude-sonnet-4-6', 500_000, 100_000)).toBeCloseTo(1.5 + 1.5);
  });

  it('prices a realistic tagging call at well under a cent', () => {
    expect(costUsd('claude-sonnet-4-6', 1500, 300)).toBeLessThan(0.01);
  });

  it('logs an unknown model at zero rather than guessing', () => {
    expect(costUsd('some-future-model', 1_000_000, 1_000_000)).toBe(0);
  });

  it('knows the models the app is configured to use', () => {
    for (const model of ['claude-sonnet-4-6', 'claude-haiku-4-5', 'claude-opus-5']) {
      expect(PRICES[model], `${model} needs a price`).toBeDefined();
    }
  });
});
