/* eslint-disable @typescript-eslint/no-explicit-any -- the Apps Script file is untyped */
// Runs the Google Apps Script's pure parts in node: what the script writes
// into the doc must read back as the same post, or the sync would ping-pong.
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join } from 'node:path';
import { runInNewContext } from 'node:vm';
import { describe, expect, it } from 'vitest';
import { dayLabel } from '../components/wormhole/util';

const root = join(__dirname, '..', '..', '..');
const mod = { exports: {} as Record<string, any> };
runInNewContext(readFileSync(join(root, 'integrations/google-doc/Code.gs'), 'utf8'), {
  module: mod,
});
const gs = mod.exports;

const { toRow } = createRequire(__filename)(join(root, 'scripts/wormhole-seed-rows.mjs')) as {
  toRow: (p: unknown) => any;
};

function apiPost(row: any) {
  return { ...row, date_tbd: false, slides: row.slides.map((s: { text: string }) => s.text) };
}

function asDoc(post: any) {
  return gs.renderBlock(post).map((p: any, index: number) => ({
    index,
    heading: p.heading,
    text: p.tag ? `${p.text} [wh:${p.tag}]` : p.text,
  }));
}

describe('Google Doc script', () => {
  it('writes the date the way Wormhole does', () => {
    for (const iso of ['2026-10-01', '2026-10-22', '2026-11-13', '2027-01-04']) {
      expect(gs.dayLabel(iso)).toBe(dayLabel(iso));
      expect(gs.isoFromLabel(gs.dayLabel(iso), iso)).toBe(iso);
    }
  });

  it('reads loose dates', () => {
    expect(gs.isoFromLabel('Tuesday, October 6th', '2026-10-01')).toBe('2026-10-06');
    expect(gs.isoFromLabel('Thursday Oct 15', '2026-10-01')).toBe('2026-10-15');
    expect(gs.isoFromLabel('Wednesday, January 6', '2026-12-20')).toBe('2027-01-06');
    expect(gs.isoFromLabel('Day and Date', '2026-10-01')).toBe(null);
  });

  it('reads back every seeded post unchanged', async () => {
    const { default: posts } = await import('../../../supabase/seed/wormhole-posts.json');
    for (const p of posts as unknown[]) {
      const post = apiPost(toRow(p));
      const [block] = gs.splitBlocks(asDoc(post));
      expect(block.id).toBe(post.id);
      expect(gs.sameFields_(block.fields, gs.fromApi_(post))).toBe(true);
    }
  });

  it('keeps Date TBD, multi-line slides and links', () => {
    const post = {
      id: 'd99',
      iso_date: '2026-10-31',
      date_tbd: true,
      topic: 'Story with a poll',
      cta: 'Vote',
      slides: ['Frame one', 'Poll\nOption 1: Epigeic\nOption 2: Anecic'],
      link: 'https://example.org\nYouTube: https://youtube.com/@x',
      sources: ['A: https://doi.org/1', 'B'],
      visual_note: 'Story, 2 frames.\nThree collage worms.',
      caption: 'First line.\n\nSecond paragraph.\n#SoilFoodWeb',
    };
    const [block] = gs.splitBlocks(asDoc(post));
    expect(block.fields.date).toBe('Date TBD');
    expect(block.fields.slides).toEqual(post.slides);
    expect(block.fields.link).toBe(post.link);
    expect(block.fields.caption).toBe(post.caption);
    expect(gs.toApi_({ date: 'Date TBD' }, post)).toEqual({ date_tbd: true });
    expect(gs.toApi_({ date: 'Friday, October 30' }, post)).toEqual({
      iso_date: '2026-10-30',
      date_tbd: false,
    });
  });

  it("writes Stephanie's template exactly", () => {
    const post = {
      id: 'p06',
      iso_date: '2026-10-28',
      date_tbd: false,
      status: 'scheduled',
      topic: 'Meet our mentors',
      cta: 'Learn more',
      slides: ['Slide one'],
      link: 'https://soilfoodweb.com',
      sources: [],
      visual_note: '',
      caption: 'Hello.',
      thumb: '/wormhole/tiles/p06-1.jpg',
    };
    expect(gs.renderBlock(post).map((p: any) => [p.heading, p.text])).toEqual([
      ['H2', '✔️ Wednesday, October 28'],
      ['P', 'Meet our mentors'],
      ['H3', 'CTA (Optional):'],
      ['P', 'Words: Learn more'],
      ['P', 'Link: https://soilfoodweb.com'],
      ['H3', 'Visual Asset (Image Thumbnail for preview and Link to Canva Project):'],
      ['P', ''],
      ['P', 'Slide 1: Slide one'],
      ['H3', 'Caption/Body Copy:'],
      ['P', 'Hello.'],
    ]);
    expect(gs.renderBlock({ ...post, status: 'draft' })[0].text).toBe('*Wednesday, October 28');
    const [block] = gs.splitBlocks(asDoc(post));
    expect(block.fields.date).toBe('Wednesday, October 28');
    expect(block.fields.cta).toBe('Learn more');
    expect(block.fields.slides).toEqual(['Slide one']);
  });

  it('treats a block with no tag as a new post', () => {
    const [block] = gs.splitBlocks([
      { index: 0, heading: 'H2', text: 'Friday, October 30' },
      { index: 1, heading: 'H3', text: 'A new idea' },
      { index: 2, heading: 'H3', text: 'CTA (Optional):' },
      { index: 3, heading: 'P', text: 'Words:' },
    ]);
    expect(block.id).toBe(null);
    expect(block.fields.topic).toBe('A new idea');
  });
});
