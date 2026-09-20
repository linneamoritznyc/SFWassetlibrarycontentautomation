/**
 * Email out.
 *
 * Resend when a key is set, the console when it is not. The fallback is not a
 * stub for testing: it means the whole system works before Linnea has a mail
 * provider, and the Questions view is always there as the other way to answer.
 */

export type Email = { to: string; subject: string; text: string; replyTo?: string };

export async function sendEmail(email: Email): Promise<'sent' | 'logged'> {
  const key = process.env.RESEND_API_KEY;
  const from = process.env.NOTIFY_FROM ?? 'SFW Content Studio <onboarding@resend.dev>';

  if (!key) {
    console.log(
      `[email] no RESEND_API_KEY, so not sending.\n  to: ${email.to}\n  subject: ${email.subject}\n${email.text}`,
    );
    return 'logged';
  }

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { authorization: `Bearer ${key}`, 'content-type': 'application/json' },
    body: JSON.stringify({
      from,
      to: [email.to],
      subject: email.subject,
      text: email.text,
      reply_to: email.replyTo,
    }),
  });

  if (!res.ok) throw new Error(`Resend refused the email (${res.status}): ${await res.text()}`);
  return 'sent';
}

/** Replies come back to `questions+<id>@`, which the webhook parses. */
export function replyToFor(questionId: number): string | undefined {
  const domain = process.env.INBOUND_EMAIL_DOMAIN;
  return domain ? `questions+${questionId}@${domain}` : undefined;
}

export function appUrl(path = ''): string {
  const base = process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000';
  return `${base.replace(/\/$/, '')}${path}`;
}
