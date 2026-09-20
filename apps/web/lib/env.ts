/**
 * Reads the environment once, with a clear error when something is missing.
 * Every message points at the file that explains how to get the value.
 */
function required(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`${name} is not set. See .env.example and docs/TODO-LINNEA.md.`);
  }
  return value;
}

export const env = {
  get supabaseUrl() {
    return required('NEXT_PUBLIC_SUPABASE_URL');
  },
  get supabaseAnonKey() {
    return required('NEXT_PUBLIC_SUPABASE_ANON_KEY');
  },
  get appUrl() {
    return process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000';
  },
};

/**
 * Who may sign in. Everything else is turned away at the door, before any
 * page or route runs.
 */
export function allowlist(): string[] {
  return (process.env.APP_ALLOWLIST ?? '')
    .split(',')
    .map((e) => e.trim().toLowerCase())
    .filter(Boolean);
}

export function isAllowed(email: string | null | undefined): boolean {
  if (!email) return false;
  const list = allowlist();
  // An empty allowlist means nobody, not everybody. Failing closed is the only
  // safe reading when the variable is missing in production.
  if (list.length === 0) return false;
  return list.includes(email.toLowerCase());
}
