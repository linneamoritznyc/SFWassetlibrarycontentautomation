# Security, in plain language

Written for Evan and anyone else who needs to know where SFW material goes and who
can see it. Kept up to date as the system changes. Last updated 25 Sep 2026.

---

## The short version

- The photos and videos live in a private Cloudflare storage account. Nobody can
  open a file without a link the app makes, and each link stops working after an
  hour.
- Only Linnea can log in. Three locks: a Vercel login, an email login link, and a
  list of allowed email addresses.
- The AI services see thumbnails, audio and text. They never receive the
  full-size originals, and they do not keep them.
- Nothing posts on its own. The app makes a download that a person uploads to
  Later by hand.
- No connection to SFW Google Drive, Google Chat or Monday.com.

---

## Where things live

| What | Where | Account |
| --- | --- | --- |
| Original photos and videos | Cloudflare R2, bucket `sfw-raw` | Linnea's Cloudflare account |
| Thumbnails, previews, cut clips | Cloudflare R2, bucket `sfw-media` | same |
| Descriptions, tags, transcripts, provenance, the job list | Supabase database (Ireland) | Linnea's Supabase org "SWF-org" |
| The web app you log into | Vercel (Dublin) | Linnea's Vercel account |
| Background workers that tag and cut | Railway | Linnea's Railway account |
| The code | GitHub, `linneamoritznyc/SFWassetlibrarycontentautomation` | Linnea's GitHub |

The code on GitHub contains no photos, videos, keys or passwords. A full check of
its history on 24 Sep 2026 found none.

---

## Who can get in

To reach the app a person must pass all three:

1. **Vercel Authentication.** The address only opens for people logged into
   Linnea's Vercel account.
2. **Email login link.** The app emails a one-time link. There is no password to
   guess or leak.
3. **Allowlist.** Even with a valid login, only the addresses in `APP_ALLOWLIST`
   get past the front door. Today: `linneamoritz1@gmail.com` and
   `linnea@soilfoodweb.com`. An empty list lets nobody in.

The database itself refuses every request from a browser. Only the app's server
and the workers can read it, using a connection string that lives in Vercel and
Railway settings.

---

## What the AI sees

| Service | Receives | Does not receive | Used for |
| --- | --- | --- | --- |
| Claude (Anthropic API) | An 800px thumbnail, the batch notes (workshop, photographer), transcripts, pasted text | Originals, the database | Descriptions, tags, clip suggestions |
| OpenAI Whisper | The audio track of a video | The picture | Transcripts |
| OpenAI embeddings | Short text: a description or a search phrase | Images, audio | Search by meaning |

Both providers say that data sent through their paid API is not used to train
their models. Each API key has a monthly spend cap.

Claude Code, the assistant that builds this, is a separate thing. It edits the
code. It is not part of the running system and holds none of its keys.

---

## Where the keys are

Every key lives in exactly the service settings that need it, and nowhere else:
not in the code, not on GitHub, not in chat.

| Key | Vercel | Railway | Unlocks |
| --- | :-: | :-: | --- |
| `DATABASE_URL` | yes | yes | The database. The most sensitive one. |
| `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` | yes | | The login screen only. Public by design; reads no data. |
| `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` | yes | yes | The two storage buckets and nothing else. |
| `ANTHROPIC_API_KEY` | | yes | Claude, capped per month. |
| `OPENAI_API_KEY` | yes | yes | Whisper and search, capped per month. |

The Supabase `service_role` key is not used by this app and is not copied
anywhere.

**If a key leaks:** delete it in the dashboard that issued it, make a new one,
paste the new one into Vercel and Railway. Nothing else needs to change.

---

## Provenance

Every photo and video carries where it came from: the batch it was uploaded in,
the photographer or creator, the original folder path, and a link back to the
original in Drive. The link is typed in by the person uploading. The app never
opens Drive itself.

---

## Open items

- **The repository is public.** It has no secrets, but `CLAUDE.md` holds the
  internal context pack (September results, brand direction). Decision pending:
  make the repository private, or remove that file from the history.
- Once email replies are switched on, the email webhook will need a way past the
  Vercel login (lock 1). To be decided then.
