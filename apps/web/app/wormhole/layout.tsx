import type { Metadata } from 'next';
import type { ReactNode } from 'react';

export const metadata: Metadata = {
  title: 'Wormhole',
  description: 'Planned Soil Food Web posts, shown the way they will look.',
  robots: { index: false, follow: false },
};

export default function WormholeLayout({ children }: { children: ReactNode }) {
  return (
    <>
      <style>{`body{background:#fff;color:#111}`}</style>
      {children}
    </>
  );
}
