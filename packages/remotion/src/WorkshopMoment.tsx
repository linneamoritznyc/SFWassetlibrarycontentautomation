import { AbsoluteFill, OffthreadVideo, Sequence } from 'remotion';
import { base } from './components/Brand.js';
import { ClipLabel, EndCard, IntroCard } from './components/Cards.js';
import { END_SECONDS, FPS, INTRO_SECONDS, type WorkshopMomentProps } from './schema.js';

/**
 * Workshop moment: one thing someone said on real land, with who said it and
 * where.
 *
 * The hook is the speaker's own line, so the intro card holds it and the clip
 * then delivers it. Naming the speaker and the place is half of how this
 * clears the expertise bar.
 */
export function WorkshopMoment({
  hook,
  speaker,
  place,
  clips,
  endCard,
  ctaUrl,
}: WorkshopMomentProps) {
  let at = Math.round(INTRO_SECONDS * FPS);
  const attribution = [speaker, place].filter(Boolean).join(' · ');

  return (
    <AbsoluteFill style={base}>
      <Sequence durationInFrames={Math.round(INTRO_SECONDS * FPS)}>
        <IntroCard title={hook} subtitle={attribution || undefined} />
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
