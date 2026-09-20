# supabase

- `migrations/` — ordered SQL. Every table in backend spec section 4, plus
  `claim_job`, `complete_job`, `fail_job` and the triggers from section 5. Row
  Level Security is on for every table and only the service role gets through.
- `seed/` — tag vocabulary, smart folders, people, question routing, cadence
  config, the starting prompts, and the eval test cases.

Apply with the Supabase CLI: `supabase db push`, or paste into the SQL editor.
