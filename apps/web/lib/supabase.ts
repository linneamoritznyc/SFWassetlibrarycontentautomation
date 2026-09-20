import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';
import { env } from './env';

/**
 * Supabase is used for one thing: knowing who is signed in. Data goes through
 * Postgres directly (see lib/db.ts), because the library queries are joins,
 * facet counts and vector searches that the query builder would fight.
 *
 * This client holds the anon key, which is safe in a browser and, thanks to RLS
 * with no policies, can read nothing from the tables anyway.
 */
export async function supabaseServer() {
  const store = await cookies();

  return createServerClient(env.supabaseUrl, env.supabaseAnonKey, {
    cookies: {
      getAll() {
        return store.getAll();
      },
      setAll(toSet) {
        try {
          for (const { name, value, options } of toSet) {
            store.set(name, value, options);
          }
        } catch {
          // Called from a Server Component, where cookies are read-only. The
          // middleware refreshes the session, so this is safe to ignore.
        }
      },
    },
  });
}

export type SignedInUser = { id: string; email: string };

/** The signed-in user, or null. Does not check the allowlist. */
export async function currentUser(): Promise<SignedInUser | null> {
  const supabase = await supabaseServer();
  const { data } = await supabase.auth.getUser();
  if (!data.user?.email) return null;
  return { id: data.user.id, email: data.user.email };
}
