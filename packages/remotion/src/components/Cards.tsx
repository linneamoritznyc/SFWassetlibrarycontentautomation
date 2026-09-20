import { COLOURS } from '@sfw/brand';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { base, CreamBlock, Eyebrow, Wordmark } from './Brand.js';

/**
 * The cards either side of the clips.
 *
 * The movement is deliberately small: a slow rise and a fade. Wonder grounded
 * in rigor, per CLAUDE.md section 4, does not mean things flying around.
 */

export function IntroCard({
  eyebrow,
  title,
  subtitle,
}: {
  eyebrow?: string;
  title: string;
  subtitle?: string;
}) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const rise = spring({
    frame,
    fps,
    config: { damping: 200 },
    durationInFrames: Math.round(fps * 0.8),
  });
  const fadeOut = interpolate(frame, [fps * 2, fps * 2.5], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        ...base,
        justifyContent: 'center',
        padding: 96,
        opacity: fadeOut,
      }}
    >
      <div style={{ transform: `translateY(${interpolate(rise, [0, 1], [40, 0])}px)` }}>
        {eyebrow && <Eyebrow>{eyebrow}</Eyebrow>}

        <CreamBlock style={{ marginTop: 28, display: 'inline-block' }}>
          <h1 style={{ margin: 0, fontSize: 84, lineHeight: 1.05, fontWeight: 700 }}>{title}</h1>
        </CreamBlock>

        {subtitle && (
          <p style={{ marginTop: 32, fontSize: 40, lineHeight: 1.3, color: COLOURS.cream }}>
            {subtitle}
          </p>
        )}
      </div>

      <Wordmark style={{ position: 'absolute', bottom: 96, left: 96 }} />
    </AbsoluteFill>
  );
}

export function EndCard({ text, ctaUrl }: { text: string; ctaUrl: string }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fadeIn = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        ...base,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 96,
        opacity: fadeIn,
      }}
    >
      <p
        style={{
          fontSize: 60,
          lineHeight: 1.25,
          textAlign: 'center',
          fontWeight: 600,
          margin: 0,
        }}
      >
        {text}
      </p>

      <p style={{ marginTop: 40, fontSize: 34, color: COLOURS.greenBright }}>{ctaUrl}</p>

      <Wordmark style={{ marginTop: 72 }} />
    </AbsoluteFill>
  );
}

/** The line that sits over a clip, when it has one. */
export function ClipLabel({ text }: { text: string }) {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const rise = interpolate(frame, [0, fps * 0.3], [24, 0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'flex-start', padding: 80 }}>
      <CreamBlock style={{ alignSelf: 'flex-start', transform: `translateY(${rise}px)` }}>
        <span style={{ fontSize: 40, fontWeight: 700, lineHeight: 1.2 }}>{text}</span>
      </CreamBlock>
      {/* Keeps the label clear of the burned-in captions at the bottom. */}
      <div style={{ height: height * 0.2 }} />
    </AbsoluteFill>
  );
}
