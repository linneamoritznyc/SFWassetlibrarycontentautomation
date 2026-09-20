# Things only you can do

External steps that need an account, a dashboard click, or an approval. Each one
has a mock or a stub in the code, so the build is never blocked waiting on it.

---

## 1. Create the Supabase project

**Why:** Phase 1 migrations need somewhere to run.

**Steps**

1. Go to https://supabase.com/dashboard and sign in.
2. Click **New project**. Organisation: your own. Name: `sfw-content-studio`.
   Region: **Europe (Frankfurt)** (closest to you; R2 is region-free).
3. Set a database password and save it in your password manager.
4. Plan: **Pro** ($25/month). The free tier pauses after a week of no traffic,
   which would stop the cron jobs.
5. Wait for the project to finish provisioning (about two minutes).
6. Left sidebar → **Project Settings** → **Data API**. Copy **Project URL** into
   `.env.local` as both `SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_URL`.
7. Same page → **API Keys**. Copy the **anon / public** key into
   `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Click **Reveal** on **service_role** and copy
   it into `SUPABASE_SERVICE_ROLE_KEY`. The service_role key bypasses every
   security rule, so it never goes in a browser and never in git.
8. Left sidebar → **Database** → **Extensions**. Search `vector`, toggle it on.
   Search `pgcrypto`, toggle it on.

**Mock in place:** none yet. Phase 1 adds a local Postgres fallback for tests.

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
