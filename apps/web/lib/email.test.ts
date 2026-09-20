import { createHmac } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import { questionIdFrom, stripQuotedReply, verifySignature } from './email';

describe('finding which question a reply answers', () => {
  it('reads the id out of the reply-to address', () => {
    expect(questionIdFrom('questions+42@soilfoodweb.com')).toBe(42);
  });

  it('falls back to the subject line', () => {
    expect(questionIdFrom(undefined, 'Re: [#7] India workshop pricing')).toBe(7);
  });

  it('falls back to a marker in the body', () => {
    expect(questionIdFrom(null, null, 'Sure, it closes on the 21st.\n\nQuestion #103')).toBe(103);
  });

  it('returns null rather than guessing', () => {
    expect(questionIdFrom('stephanie@soilfoodweb.com', 'Re: hello', 'No idea')).toBeNull();
  });
});

describe('stripping the quoted original', () => {
  it('keeps only what was typed above a Gmail quote', () => {
    const reply = [
      'Enrollment closed on 21 September.',
      '',
      'On Fri, 20 Sep 2026 at 09:00, SFW Content Studio wrote:',
      '> Is the India workshop still open?',
    ].join('\n');

    expect(stripQuotedReply(reply)).toBe('Enrollment closed on 21 September.');
  });

  it('handles an Outlook original-message separator', () => {
    const reply = [
      'Loida runs it, with Gerald.',
      '',
      '-----Original Message-----',
      'From: SFW Content Studio',
    ].join('\n');

    expect(stripQuotedReply(reply)).toBe('Loida runs it, with Gerald.');
  });

  it('stops at a bare quote marker', () => {
    expect(stripQuotedReply('Yes.\n> the original question')).toBe('Yes.');
  });

  it('stops at a phone signature', () => {
    expect(stripQuotedReply('About 40 people.\n\nSent from my iPhone')).toBe('About 40 people.');
  });

  it('leaves an unquoted reply alone', () => {
    const plain = 'Two weeks, with a weekend break in the middle.';
    expect(stripQuotedReply(plain)).toBe(plain);
  });

  it('does not mistake a From: line in the first position for a quote', () => {
    // Some providers put headers at the top of the parsed text.
    expect(stripQuotedReply('From: Kavi\nIt is Isha Outreach.')).toContain('Isha Outreach');
  });
});

describe('webhook signatures', () => {
  const secret = 'shh';
  const body = '{"to":"questions+1@x"}';
  const good = createHmac('sha256', secret).update(body).digest('hex');

  it('accepts a correct signature', () => {
    expect(verifySignature(body, good, secret)).toBe(true);
  });

  it('rejects a wrong one', () => {
    expect(verifySignature(body, 'deadbeef', secret)).toBe(false);
  });

  it('rejects a tampered body', () => {
    expect(verifySignature('{"to":"questions+2@x"}', good, secret)).toBe(false);
  });

  it('does not throw on a signature of the wrong length', () => {
    expect(() => verifySignature(body, '', secret)).not.toThrow();
    expect(verifySignature(body, '', secret)).toBe(false);
  });
});
