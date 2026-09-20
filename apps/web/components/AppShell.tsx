'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import type { ReactNode } from 'react';

const NAV = [
  { href: '/library', label: 'Library' },
  { href: '/inbox', label: 'Inbox' },
  { href: '/clips', label: 'Clips' },
  { href: '/week', label: 'Week' },
  { href: '/questions', label: 'Questions' },
  { href: '/scout', label: 'Scout' },
  { href: '/learned', label: 'Learned' },
  { href: '/errors', label: 'Errors' },
  { href: '/settings', label: 'Settings' },
];

const BARE = ['/login', '/setup', '/auth'];

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  if (BARE.some((p) => pathname.startsWith(p))) return <>{children}</>;

  return (
    <div className="min-h-screen">
      <header className="border-b border-green-mid/20 bg-white">
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 px-4 py-2">
          <Link href="/library" className="text-sm font-semibold">
            SFW Content Studio
          </Link>
          <nav className="flex flex-wrap gap-1 text-sm">
            {NAV.map((item) => {
              const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`rounded px-2 py-1 ${
                    active ? 'bg-green-deep text-cream' : 'hover:bg-green-bright/15'
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
          <form action="/auth/signout" method="post" className="ml-auto">
            <button type="submit" className="text-xs text-green-mid underline">
              Sign out
            </button>
          </form>
        </div>
      </header>
      {children}
    </div>
  );
}
