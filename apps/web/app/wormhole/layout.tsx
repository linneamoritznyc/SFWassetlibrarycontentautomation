import type { Metadata } from 'next';
import { Montserrat, Source_Sans_3 } from 'next/font/google';
import type { ReactNode } from 'react';

export const metadata: Metadata = {
  title: 'Wormhole',
  description: 'Planned Soil Food Web posts, shown the way they will look.',
  robots: { index: false, follow: false },
};

// The brand fonts (2026 Brand Style Guide, docs/brand.md), so a slide still
// waiting for its visual is set in the brand type, not the browser's default.
const heading = Montserrat({ subsets: ['latin'], weight: ['600'], variable: '--font-heading' });
const body = Source_Sans_3({ subsets: ['latin'], weight: ['400', '600'], variable: '--font-body' });

export default function WormholeLayout({ children }: { children: ReactNode }) {
  return (
    <div className={`${heading.variable} ${body.variable}`}>
      <style>{`body{background:#fff;color:#111}`}</style>
      {children}
    </div>
  );
}
