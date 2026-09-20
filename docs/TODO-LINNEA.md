# Things only you can do

External steps that need an account, a dashboard click, or an approval. Each one
has a mock or a stub in the code, so the build is never blocked waiting on it.

---

## 1. Create the Supabase project

**Why:** Phase 1 migrations need somewhere to run.

**Steps**

1. Go to https://supabase.com/dashboard and sign in.
2. Click **New project**. Organisation: your own. Name: anything; the name is
   only a label. Region: **Europe**, which is closest to you and to where the
   web app and the workers will run. R2 is region-free, so nothing else cares.
3. Set a database password and save it in your password manager. If you ever
   paste it into a connection string, percent-encode it: `@` becomes `%40`,
   `#` becomes `%23`, `/` becomes `%2F`.
4. On the **Security** block of the new-project form:
   - **Enable Data API** — leave **on**. The app reads data through Postgres
     directly, not through this API, so it is not doing any work for us, but
     it is the default and turning it off buys nothing.
   - **Automatically expose new tables** — turn it **off**. Migration
     `0009_rls.sql` revokes those grants anyway; off means there is nothing to
     revoke.
   - **Enable automatic RLS** — turn it **on**. The migrations already switch
     Row Level Security on for all 29 tables, so this changes nothing today. It
     is a safety net for a table someone adds by hand in the dashboard later.
5. Plan: **Free** is fine to start with. A free project pauses after a week
   with no traffic, and the cron hits the database every morning, so it should
   not pause. Move to **Pro** ($25/month) if it ever does, or when the database
   outgrows the 500 MB free limit.
6. Wait for the project to finish provisioning (about two minutes).
7. Left sidebar → **Project Settings** → **Data API**. Copy **Project URL** into
   `.env.local` as both `SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_URL`.
8. Same page → **API Keys**. Copy the **anon / public** key into
   `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Click **Reveal** on **service_role** and copy
   it into `SUPABASE_SERVICE_ROLE_KEY`. The service_role key bypasses every
   security rule, so it never goes in a browser and never in git.
9. Left sidebar → **Database** → **Extensions**. Search `vector`, toggle it on.
   Search `pgcrypto`, toggle it on. (Migration `0001` also creates them, but
   toggling them here first means a clearer error if the plan does not allow
   one.)
10. Left sidebar → **Project Settings** → **Database** → **Connection string**.
    There are two, and they are not interchangeable:
    - **Direct connection** (port 5432): use this one for `DATABASE_URL` when
      you run `pnpm db:setup`, which creates extensions and functions.
    - **Transaction pooler** (port 6543): use this one for `DATABASE_URL` on
      Vercel and on Railway. Serverless and a worker pool both open and close
      connections constantly, which is what the pooler is for.
    If the direct connection will not resolve from Vercel or Railway, that is
    IPv6: use the **session pooler** string instead.

**How the security model actually works**

The app never lets a browser talk to the database. Every read and write goes
through an API route on the server, which holds the service_role key.

- Row Level Security is **on and forced** for all 29 tables, with **zero
  policies** on any of them. On Supabase, `service_role` bypasses RLS; `anon`
  and `authenticated` do not. So a key that leaks into a browser can read
  nothing and write nothing.
- The grants are **revoked** as well, from `anon` and `authenticated`, on every
  table, sequence and function, plus the default privileges for anything added
  later. The answer is no twice.
- The queue functions (`claim_job`, `enqueue_job` and the rest) have their
  execute permission revoked from those two roles too.
- Signing in is Supabase magic link, and `middleware.ts` then checks the email
  against `APP_ALLOWLIST`. It fails closed: an empty allowlist lets nobody in.

That is all in `supabase/migrations/0009_rls.sql`, which is worth a read if you
want to see it rather than take my word for it.

**Mock in place:** the tests build their own throwaway database from
`TEST_DATABASE_URL`, so nothing in the repo needs your Supabase project to run.

---

## 2. Create the two Cloudflare R2 buckets

**Why:** all originals, thumbnails, proxies, clips and renders live here.

**Steps**

1. Go to https://dash.cloudflare.com and sign in.
2. Left sidebar → **R2 Object Storage**. If this is the first time, click
   **Purchase R2** (there is a free tier; you are only adding a payment method).
3. Click **Create bucket**. Name: `sfw-raw`. Location: **Automatic**. Default
   storage class: **Infrequent Access**. Create.
4. Click **Create bucket** again. Name: `sfw-media`. Location: **Automatic**.
   Default storage class: **Standard**. Create.
5. Open `sfw-media` → **Settings** → **CORS policy** → **Add CORS policy**.
   Paste:

   ```json
   [
     {
       "AllowedOrigins": ["http://localhost:3000", "https://YOUR-VERCEL-DOMAIN"],
       "AllowedMethods": ["GET", "PUT"],
       "AllowedHeaders": ["*"],
       "ExposeHeaders": ["ETag"],
       "MaxAgeSeconds": 3600
     }
   ]
   ```

   Repeat for `sfw-raw`. Replace `YOUR-VERCEL-DOMAIN` once Phase 8 deploys.
6. Back to **R2 Overview** → **API** → **Manage API tokens** → **Create API
   token**. Permissions: **Object Read & Write**. Scope: **Apply to specific
   buckets** → both buckets. TTL: forever. Create.
7. Copy **Access Key ID** → `R2_ACCESS_KEY_ID`, **Secret Access Key** →
   `R2_SECRET_ACCESS_KEY`. These are shown once.
8. The **Account ID** is in the right-hand column of the R2 overview page →
   `R2_ACCOUNT_ID`.

**Mock in place:** Phase 2 ships an on-disk storage driver so uploads work
locally without R2.

---

## 3. Anthropic and OpenAI API keys

**Steps**

1. https://console.anthropic.com → **API Keys** → **Create Key**. Name it
   `sfw-content-studio`. Copy into `ANTHROPIC_API_KEY`.
2. Set a spend limit: **Settings** → **Limits** → monthly cap $60. The spec
   estimates $20 to $40 a month.
3. https://platform.openai.com/api-keys → **Create new secret key**. Copy into
   `OPENAI_API_KEY`. This is Whisper and the embeddings only.
4. Set a spend limit there too: **Settings** → **Billing** → **Limits** → $20.

**Mock in place:** Phase 1 adds a fake AI client used by every test, so nothing
in CI ever calls a real API.

---

## 4. Canva Connect integration (Phase 7)

**Why:** `canva_push` and `canva_pull`. Autofill stays behind a feature flag
until Canva approves the integration, which takes them weeks.

**Steps**

1. https://www.canva.com/developers/ → sign in with your own Canva account.
2. **Your integrations** → **Create an integration** → **Public**.
3. Name: `SFW Content Studio`. Leave it in **Draft** mode; draft integrations
   work for your own account without review.
4. **Configuration** → **Scopes**. Tick: `asset:read`, `asset:write`,
   `design:content:read`, `design:content:write`, `design:meta:read`,
   `folder:read`, `folder:write`.
5. **Authentication** → **Add redirect URL**:
   `http://localhost:3000/api/canva/callback`, and later the Vercel one.
6. Copy **Client ID** → `CANVA_CLIENT_ID` and **Client secret** →
   `CANVA_CLIENT_SECRET`. Set `CANVA_REDIRECT_URI` to the same URL as step 5.
7. Autofill needs `brandtemplate:content:read` plus a submitted review. Ask for
   it when you are ready; until then the flag stays off.

**Mock in place:** Phase 7 stubs both jobs behind `CANVA_ENABLED`.

---

## 5. Instagram Graph API (Phase 5, optional)

**Why:** `results_pull` reads insights. Without it, the CSV import from Later
covers the same ground by hand.

**Steps**

1. The @soilfoodwebschool account must be a **Business** account linked to a
   Facebook Page. Ask Stephanie, she owns the account.
2. https://developers.facebook.com → **My Apps** → **Create App** → type
   **Business**.
3. Add the **Instagram Graph API** product.
4. **Tools** → **Graph API Explorer**. Pick the app, permissions
   `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`.
   Generate a token.
5. Exchange it for a long-lived token (60 days) and put it in
   `IG_ACCESS_TOKEN`. The account id goes in `IG_BUSINESS_ACCOUNT_ID`.
6. Diary note: the token expires every 60 days and must be refreshed.

**Mock in place:** Phase 5 ships the Later CSV import screen first; the Graph
API path only runs when both variables are set.

---

## 6. Transactional email (Phase 4 and 5)

**Why:** the Monday review email and the question-routing emails people reply to.

**Steps**

1. https://resend.com → sign up → **API Keys** → **Create API Key**. Copy into
   `RESEND_API_KEY`.
2. **Domains** → **Add Domain** → `soilfoodweb.com`. This needs DNS records
   added, so it needs whoever runs the domain. Until then Resend's sandbox
   sender works for mail to your own address only.
3. **Webhooks** → **Add Webhook** → URL `https://YOUR-VERCEL-DOMAIN/api/webhooks/email`,
   event `email.received`. Copy the signing secret into `INBOUND_EMAIL_SECRET`.

**Mock in place:** Phase 4 writes emails to the console and to a table when no
key is set, and the Questions view lets you answer in the app instead.

---

## 7. Railway and Vercel (Phase 8)

Filled in when Phase 8 lands. Nothing to do yet.

---

## 8. Fill in the team's email addresses

**Why:** `gap_check` turns an unknown into a one-line question and emails it to
the right person. Right now every person is seeded with their name, role and
topics, but no address, because none of the source documents contains one and
guessing would mean mailing a stranger.

**Steps**

1. Open the app, Settings, People (Phase 8), or ask me to do it.
2. Add an address for at least these four, who are the routing targets:
   Stephanie McDaniel (programs), Carla Portugal (mentors and graduates),
   Kavi Reddy (India and partners), Loida Vasquez (workshops).
3. Until then, questions are created and shown in the Questions view but not
   emailed. Nothing is lost, you just have to look.

**Mock in place:** questions appear in the app and can be answered there.

---

## 9. Paste the two real captions into the test set

**Why:** the eval test set has the Pratik vermicompost post and the Sandra
Niggemeyer Field Notes post as its two "good" cases, and every prompt change is
measured against them. The versions in the repo are rebuilt from the details in
CLAUDE.md, not the real posts, which are not in any document you sent.

**Steps**

1. Open Instagram, @soilfoodwebschool, find the 16 September Pratik vermicompost
   post and the Sandra Niggemeyer Field Notes carousel.
2. Copy each caption in full, including hashtags.
3. Paste them to me, or edit
   `packages/shared/src/test-cases.ts` and replace the `caption` on the two
   entries whose names start `good:`.
4. Re-run `pnpm db:seed`.

**Mock in place:** reconstructed captions that carry the same concrete detail.

---

## 10. Check the captions are in Montserrat, not DejaVu

**Why:** burned-in captions are meant to be Montserrat 600 (CLAUDE.md section
5). It is not in the Debian archive, so the `workers/media` image downloads it
from Google Fonts at build time. If that download fails the image still builds
and falls back to DejaVu Sans Bold. The clips are legible either way, but off
brand.

**Steps**

1. After the first deploy, cut one clip and look at it.
2. If the caption is not Montserrat, open the Railway build log for
   `worker-media` and search for "Montserrat unavailable at build time".
3. If it is there, the simplest fix is to commit the font file: download
   Montserrat from https://fonts.google.com/specimen/Montserrat, put
   `Montserrat-SemiBold.ttf` in `packages/brand/fonts/`, and tell me. It is
   Open Font Licensed, so it can live in the repository.

**Mock in place:** the fallback chain, which produces legible captions in
DejaVu Sans Bold.

---

## 11. Generate the token encryption key

**Why:** Canva's access and refresh tokens are encrypted before they touch the
database (backend spec section 9). Without the key, connecting Canva fails with
a message saying so.

**Steps**

1. Run this and paste the result into `TOKEN_ENC_KEY` in `.env.local`:

   ```bash
   node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
   ```

2. Keep a copy somewhere safe. Changing it makes the stored tokens
   unreadable, and you would have to reconnect Canva.

**Mock in place:** none. Canva simply stays disconnected until this is set.

---

## 12. Check the Remotion licence

**Why:** the Reel templates are built with Remotion, which is free for
individuals and small companies but needs a paid company licence above a
certain size. The PRD flags it as an open question.

**Steps**

1. Read https://www.remotion.dev/docs/licensing
2. Count the Foundation's employees against their threshold.
3. If a licence is needed, it is bought per seat per month and the licence key
   goes in the Remotion config.

If the answer is no, the alternative is building Reels in Canva instead, which
the Canva integration already covers for still posts. Tell me and I will move
the two templates over.

**Mock in place:** none. The templates work; this is a legal question, not a
technical one.

---

## 13. Check the scout's feed list

**Why:** the twenty-seven feeds are seeded from the UN bodies, the research
networks and the regional programmes the Foundation asked for, but the sandbox
this was built in could not reach the open internet, so **none** of the URLs was
confirmed to still work. They are the best known URL for each organisation, not
tested ones.

**Steps**

1. Run `pnpm feeds:check` from your laptop. It tests every feed, prints a table
   by region, and lists the failing URLs at the end. It touches no database and
   needs no API key.
2. Fix any failures in `packages/shared/src/feeds.ts`, then `pnpm db:seed`.
   A site's feed is usually at `/feed`, `/rss`, `/rss.xml` or `/feed/`.
   If an organisation has no feed at all, set `kind: 'page'` and the scout reads
   the page as a source instead of trying to parse it.
3. Once it is running, Settings shows the same thing live: the Feeds panel puts
   any failing feed at the top with the actual error and the date it last
   worked. A feed that fails five mornings in a row switches itself off.

Worth adding if you have them: the journals you already follow, and any
newsletter with an RSS mirror. Non-English is welcome, the scout summarises
everything in English and keeps the original on the card.

**Mock in place:** a failing feed is recorded and skipped, so one dead URL out
of twenty-seven never stops the other twenty-six.
