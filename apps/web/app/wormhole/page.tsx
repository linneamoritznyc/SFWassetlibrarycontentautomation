import { cookies } from 'next/headers';
import { Wormhole } from '@/components/wormhole/Wormhole';
import { NAME_COOKIE, cleanName } from '@/lib/wormhole-auth';

export const dynamic = 'force-dynamic';

export default function WormholePage() {
  const editor = cleanName(cookies().get(NAME_COOKIE)?.value);
  return <Wormhole editor={editor} />;
}
