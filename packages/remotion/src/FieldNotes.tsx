import { AbsoluteFill, OffthreadVideo, Sequence } from 'remotion';
import { base } from './components/Brand.js';
import { ClipLabel, EndCard, IntroCard } from './components/Cards.js';
import { END_SECONDS, FPS, INTRO_SECONDS, type FieldNotesProps } from './schema.js';

/**
 * Field Notes: a practicum graduate's trial, including the parts that did not
 * work.
 *
 * The series convention from CLAUDE.md section 7 is the whole point of the
 * template: the eyebrow number, and a subtitle carrying the named person,
 * place and season. A Field Notes card without those is not a Field Notes card.
 */
export function FieldNotes({ eyebrow, title, subtitle, clips, endCard, ctaUrl }: FieldNotesProps) {
  let at = Math.round(INTRO_SECONDS * FPS);

  return (
    <AbsoluteFill style={base}>
      <Sequence durationInFrames={Math.round(INTRO_SECONDS * FPS)}>
        <IntroCard eyebrow={eyebrow} title={title} subtitle={subtitle} />
      </Sequence>

      {clips.map((clip, index) => {
        const frames = Math.round(clip.durationS * FPS);
        const from = at;
        at += frames;

        return (
          <Sequence key={index} from={from} durationInFrames={frames}>
            <AbsoluteFill>
              <OffthreadVideo
                src={clip.src}
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
              {clip.label && <ClipLabel text={clip.label} />}
            </AbsoluteFill>
          </Sequence>
        );
      })}

      <Sequence from={at} durationInFrames={Math.round(END_SECONDS * FPS)}>
        <EndCard text={endCard} ctaUrl={ctaUrl} />
      </Sequence>
    </AbsoluteFill>
  );
}
