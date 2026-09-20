import { handler } from '@sfw/queue';
import { diffCaption } from '@sfw/shared';
import { db } from '../db.js';

/**
 * Records what a human changed about the AI's draft.
 *
 * This is the raw material of the whole self-improvement loop. The diff goes on
 * the human version rather than the AI one, so a version row answers "what did
 * this person change" without needing the row before it.
 */
export const logEdit = handler<{ post_id: string }>(async ({ job }) => {
  const pool = db();
  const postId = job.payload.post_id;

  const { rows } = await pool.query<{
    id: number;
    version: number;
    author: string;
    caption: string | null;
    hook: string | null;
    hashtags: string[];
  }>(
    `select id, version, author, caption, hook, hashtags
     from post_versions where post_id = $1 order by version desc limit 4`,
    [postId],
  );

  const human = rows.find((r) => r.author === 'human');
  if (!human) {
    console.log(`[log_edit] no human version of ${postId} yet`);
    return;
  }

  // The last AI version before this human one.
  const ai = rows.find((r) => r.author === 'ai' && r.version < human.version);
  if (!ai) {
    console.log(`[log_edit] ${postId} has no AI version to compare against`);
    return;
  }

  const captionDiff = diffCaption(ai.caption ?? '', human.caption ?? '');
  const hookDiff = diffCaption(ai.hook ?? '', human.hook ?? '');

  const added = human.hashtags.filter((h) => !ai.hashtags.includes(h));
  const dropped = ai.hashtags.filter((h) => !human.hashtags.includes(h));

  await pool.query(`update post_versions set diff = $2::jsonb where id = $1`, [
    human.id,
    JSON.stringify({
      compared_to_version: ai.version,
      caption: {
        ratio: captionDiff.ratio,
        added_words: captionDiff.addedWords,
        removed_words: captionDiff.removedWords,
        removed_sentences: captionDiff.removedSentences,
        added_sentences: captionDiff.addedSentences,
      },
      hook: {
        ratio: hookDiff.ratio,
        before: ai.hook,
        after: human.hook,
        changed: hookDiff.ratio > 0,
      },
      hashtags: { added, dropped },
    }),
  ]);

  console.log(
    `[log_edit] ${postId}: caption changed by ${Math.round(captionDiff.ratio * 100)}%` +
      (hookDiff.ratio > 0 ? ', hook rewritten' : ''),
  );
});
