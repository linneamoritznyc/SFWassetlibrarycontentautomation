import { COLOURS, FONTS } from '@sfw/brand';
import type { CSSProperties, ReactNode } from 'react';

/**
 * The bits of the brand that every template shares.
 *
 * Greens and cream, cream used as a shape rather than a background, one shadow
 * value. The wordmark stands in for the real logo file, which is not in the
 * repository: see docs/TODO-LINNEA.md.
 */

export const fontStack = [FONTS.caption, ...FONTS.captionFallbacks].join(', ');

export const base: CSSProperties = {
  fontFamily: fontStack,
  color: COLOURS.cream,
  backgroundColor: COLOURS.greenDeep,
};

export function Wordmark({ style }: { style?: CSSProperties }) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 16,
        fontWeight: 700,
        fontSize: 34,
        letterSpacing: 1,
        color: COLOURS.cream,
        ...style,
      }}
    >
      <span
        style={{
          width: 44,
          height: 44,
          borderRadius: 22,
          border: `4px solid ${COLOURS.greenBright}`,
          display: 'block',
        }}
      />
      SOIL FOOD WEB
    </div>
  );
}

/** The cream shape the eyebrow and titles sit on. */
export function CreamBlock({ children, style }: { children: ReactNode; style?: CSSProperties }) {
  return (
    <div
      style={{
        backgroundColor: COLOURS.cream,
        color: COLOURS.greenDeep,
        padding: '18px 34px',
        boxShadow: '0 2px 8px rgba(29, 59, 42, 0.12)',
        ...style,
      }}
    >
      {children}
    </div>
  );
}

export function Eyebrow({ children }: { children: ReactNode }) {
  return (
    <div
      style={{
        fontSize: 30,
        fontWeight: 700,
        letterSpacing: 6,
        textTransform: 'uppercase',
        color: COLOURS.greenBright,
      }}
    >
      {children}
    </div>
  );
}
