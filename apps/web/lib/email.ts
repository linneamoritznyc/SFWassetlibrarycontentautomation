import { createHmac, timingSafeEqual } from 'node:crypto';

/**
 * Parsing a reply to a question email.
 *
 * Kept out of the route file both because Next only allows certain exports
 * there, and because this is the part worth testing: getting it wrong means
 * storing a mail client's quoted copy of the question back as its own answer.
 */

export function verifySignature(body: string, signature: string, secret: string): boolean {
  const expected = createHmac('sha256', secret).update(body).digest('hex');
  const a = Buffer.from(expected);
  const b = Buffer.from(signature);
  // Length first: timingSafeEqual throws when the lengths differ.
  return a.length === b.length && timingSafeEqual(a, b);
}

/** `questions+42@…` in the To, `[#42]` in the subject, or a marker in the body. */
export function questionIdFrom(...fields: (string | undefined | null)[]): number | null {
  for (const field of fields) {
    if (!field) continue;
    const match =
      /questions\+(\d+)@/.exec(field) ?? /\[#(\d+)\]/.exec(field) ?? /question #(\d+)/i.exec(field);
    if (match?.[1]) return Number(match[1]);
  }
  return null;
}

/**
 * Everything above the first quoted line.
 *
 * Mail clients quote the original underneath the reply. Without this, answering
 * "It closes on the 21st" would store the answer plus the whole question plus
 * whatever else was in the thread, and the fact extractor would treat the
 * question as a statement.
 */
export function stripQuotedReply(text: string): string {
  const out: string[] = [];

  for (const line of text.split('\n')) {
    const trimmed = line.trim();
    if (trimmed.startsWith('>')) break;
    if (/^On .+ wrote:$/.test(trimmed)) break;
    if (/^-{2,}\s*Original Message/i.test(trimmed)) break;
    if (/^_{5,}$/.test(trimmed)) break;
    if (/^From:\s/.test(trimmed) && out.length > 0) break;
    // Outlook and Gmail both use this before the quoted block.
    if (/^Sent from my /i.test(trimmed)) break;
    out.push(line);
  }

  return out.join('\n').trim();
}
