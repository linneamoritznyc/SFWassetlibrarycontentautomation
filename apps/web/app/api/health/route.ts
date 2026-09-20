import { NextResponse } from 'next/server';

// Health check. Vercel and the uptime check poll this; worker heartbeat rows
// get folded in here in Phase 8.
export function GET() {
  return NextResponse.json({ ok: true, service: 'web', time: new Date().toISOString() });
}
