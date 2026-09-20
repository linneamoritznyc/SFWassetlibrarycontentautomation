# bulk-upload

Two steps for getting the ~7.34 TB raw footage drive into `sfw-raw` without
pushing it through the browser.

## 1. Copy the files with rclone

rclone talks S3 to R2 directly, resumes, and runs unattended.

```bash
# Install (macOS)
brew install rclone

# Configure a remote called r2
rclone config
#   n) New remote
#   name> r2
#   Storage> s3
#   provider> Cloudflare
#   access_key_id>      <R2_ACCESS_KEY_ID>
#   secret_access_key>  <R2_SECRET_ACCESS_KEY>
#   region> auto
#   endpoint> https://<R2_ACCOUNT_ID>.r2.cloudflarestorage.com

# Dry run first. Always.
rclone copy "/Volumes/SFW Footage" r2:sfw-raw/originals \
  --dry-run --progress --transfers 8

# Then for real. --checksum so a re-run skips what is already there.
rclone copy "/Volumes/SFW Footage" r2:sfw-raw/originals \
  --progress --transfers 8 --checksum --log-file rclone.log
```

An interrupted copy is safe to re-run: rclone skips files that already match.

## 2. Register what landed as assets

```bash
pnpm --filter @sfw/script-bulk-upload build
node scripts/bulk-upload/dist/index.js \
  --prefix originals/ \
  --creator "SFW" \
  --workshop "Wild Ken Hill 2025" \
  --drive-link "https://drive.google.com/..." \
  --dry-run
```

It lists every object under the prefix, creates one `assets` row per object with
the batch provenance filled in, and enqueues an `ingest` job for each. It is
idempotent: an object whose `r2_key` already has an asset row is skipped, so
re-running after an interrupted rclone copy adds only the new files.

Drop `--dry-run` to write.
