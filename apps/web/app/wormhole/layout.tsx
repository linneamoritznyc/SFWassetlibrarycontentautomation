import type { Metadata } from 'next';
import { Fredoka, Montserrat } from 'next/font/google';
import type { ReactNode } from 'react';

export const metadata: Metadata = {
  title: 'Wormhole',
  description: 'Planned Soil Food Web posts, shown the way they will look.',
  robots: { index: false, follow: false },
};

// The fonts the finished tiles use (tools/wormhole-visuals), so a slide still
// waiting for its visual is set in the brand type, not the browser's default.
const heading = Fredoka({ subsets: ['latin'], weight: ['600'], variable: '--font-heading' });
const body = Montserrat({ subsets: ['latin'], weight: ['400', '600'], variable: '--font-body' });

export default function WormholeLayout({ children }: { children: ReactNode }) {
  return (
    <div className={`${heading.variable} ${body.variable}`}>
      <style>{`body{background:#fff;color:#111}`}</style>
      {children}
    </div>
  );
}
