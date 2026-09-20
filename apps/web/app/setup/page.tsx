export default function SetupPage() {
  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="text-2xl font-semibold">Not configured yet</h1>
      <p className="mt-3">
        This app needs a Supabase project, two Cloudflare R2 buckets and a couple of API keys before
        it can do anything. None of that can be done from here.
      </p>
      <p className="mt-3">
        The click-by-click steps are in <code>docs/TODO-LINNEA.md</code> in the repository. Once the
        values are in <code>.env.local</code>, restart the app and this page goes away.
      </p>
      <ul className="mt-4 list-disc space-y-1 pl-5 text-sm text-green-mid">
        <li>
          <code>NEXT_PUBLIC_SUPABASE_URL</code> and <code>NEXT_PUBLIC_SUPABASE_ANON_KEY</code>
        </li>
        <li>
          <code>APP_ALLOWLIST</code>, or nobody can sign in
        </li>
        <li>
          <code>DATABASE_URL</code>, then <code>pnpm db:setup</code>
        </li>
        <li>the four R2 variables, and the Anthropic and OpenAI keys</li>
      </ul>
    </main>
  );
}
