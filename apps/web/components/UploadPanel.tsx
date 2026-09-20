'use client';

import { useCallback, useState } from 'react';
import { assetTypeFor, makeThumbnail } from '@/lib/thumbnail';

type Batch = { driveLink: string; originalPath: string; creator: string; workshop: string };

type Progress = {
  name: string;
  state: 'waiting' | 'thumbnail' | 'uploading' | 'done' | 'failed';
  note?: string;
};

/**
 * Batch upload.
 *
 * The provenance is entered once and inherited by every file in the batch,
 * which is the only way a few hundred photos ever get a Drive link on them.
 * Files go straight to R2 with a presigned PUT: nothing large passes through a
 * serverless function, and no key reaches the browser.
 */
export function UploadPanel({ onDone }: { onDone?: () => void }) {
  const [batch, setBatch] = useState<Batch>({
    driveLink: '',
    originalPath: '',
    creator: '',
    workshop: '',
  });
  const [progress, setProgress] = useState<Progress[]>([]);
  const [busy, setBusy] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [summary, setSummary] = useState('');

  const upload = useCallback(
    async (files: File[]) => {
      if (files.length === 0) return;
      setBusy(true);
      setSummary('');
      setProgress(files.map((f) => ({ name: f.name, state: 'waiting' })));

      const mark = (i: number, state: Progress['state'], note?: string) =>
        setProgress((prev) => prev.map((p, j) => (j === i ? { ...p, state, note } : p)));

      try {
        // 1. Ask for one presigned PUT per file.
        const res = await fetch('/api/upload-url', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({
            files: files.map((f) => ({
              filename: f.name,
              contentType: f.type || 'application/octet-stream',
              type: assetTypeFor(f),
            })),
          }),
        });

        if (!res.ok)
          throw new Error(((await res.json()) as { error?: string }).error ?? 'Upload refused');
        const { uploads } = (await res.json()) as {
          uploads: {
            assetId: string;
            filename: string;
            bucket: string;
            r2Key: string;
            thumbKey: string;
            putUrl: string;
            thumbPutUrl: string;
          }[];
        };

        // 2. Thumbnail, EXIF, then the two uploads, one file at a time so a
        //    hundred photos do not open a hundred connections at once.
        const created: Record<string, unknown>[] = [];

        for (const [i, file] of files.entries()) {
          const slot = uploads[i];
          if (!slot) continue;

          try {
            mark(i, 'thumbnail');
            const measured = await makeThumbnail(file);
            const exif = await readExif(file);

            mark(i, 'uploading');
            await put(slot.putUrl, file, file.type || 'application/octet-stream');

            if (measured.blob) {
              await put(slot.thumbPutUrl, measured.blob, 'image/jpeg');
            }

            created.push({
              assetId: slot.assetId,
              type: assetTypeFor(file),
              filename: slot.filename,
              bucket: slot.bucket,
              r2Key: slot.r2Key,
              thumbKey: measured.blob ? slot.thumbKey : null,
              width: measured.width,
              height: measured.height,
              durationS: measured.durationS,
              takenAt: exif.takenAt,
              camera: exif.camera,
              gpsLat: exif.lat,
              gpsLng: exif.lng,
            });

            mark(i, 'done');
          } catch (err) {
            mark(i, 'failed', err instanceof Error ? err.message : 'failed');
          }
        }

        if (created.length === 0) {
          setSummary('Nothing uploaded.');
          return;
        }

        // 3. Register them, which enqueues one ingest per asset.
        const register = await fetch('/api/assets', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ batch, assets: created }),
        });

        const body = (await register.json()) as { created?: number; error?: string };
        setSummary(
          register.ok
            ? `${body.created} asset(s) uploaded. Tagging has been queued.`
            : (body.error ?? 'Could not register the uploads.'),
        );
        if (register.ok) onDone?.();
      } catch (err) {
        setSummary(err instanceof Error ? err.message : 'Upload failed.');
      } finally {
        setBusy(false);
      }
    },
    [batch, onDone],
  );

  return (
    <section className="rounded border border-green-mid/30 bg-white p-4">
      <h2 className="text-sm font-semibold">Upload a batch</h2>
      <p className="mt-1 text-xs text-green-mid">
        Entered once, copied onto every file in this batch.
      </p>

      <div className="mt-3 grid gap-2 sm:grid-cols-2">
        <Field
          label="Workshop"
          value={batch.workshop}
          onChange={(v) => setBatch({ ...batch, workshop: v })}
          placeholder="Wild Ken Hill"
        />
        <Field
          label="Creator"
          value={batch.creator}
          onChange={(v) => setBatch({ ...batch, creator: v })}
          placeholder="Who shot it"
        />
        <Field
          label="Drive link"
          value={batch.driveLink}
          onChange={(v) => setBatch({ ...batch, driveLink: v })}
          placeholder="https://drive.google.com/..."
        />
        <Field
          label="Original path"
          value={batch.originalPath}
          onChange={(v) => setBatch({ ...batch, originalPath: v })}
          placeholder="/Footage/2025/Cyprus"
        />
      </div>

      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          void upload(Array.from(e.dataTransfer.files));
        }}
        className={`mt-3 rounded border-2 border-dashed p-6 text-center text-sm ${
          dragging ? 'border-green-deep bg-green-bright/10' : 'border-green-mid/30'
        }`}
      >
        <p>Drop files here</p>
        <p className="mt-1 text-xs text-green-mid">Photos, video, graphics, PDFs. Or</p>
        <input
          type="file"
          multiple
          disabled={busy}
          className="mt-2 text-xs"
          onChange={(e) => void upload(Array.from(e.target.files ?? []))}
        />
      </div>

      {progress.length > 0 && (
        <ul className="mt-3 max-h-40 space-y-0.5 overflow-y-auto text-xs">
          {progress.map((p) => (
            <li key={p.name} className="flex gap-2">
              <span className="flex-1 truncate">{p.name}</span>
              <span className={p.state === 'failed' ? 'text-gold' : 'text-green-mid'}>
                {p.note ?? p.state}
              </span>
            </li>
          ))}
        </ul>
      )}

      {summary && <p className="mt-2 text-xs font-medium">{summary}</p>}
    </section>
  );
}

function Field({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}) {
  return (
    <label className="block text-xs">
      <span className="text-green-mid">{label}</span>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="mt-0.5 w-full rounded border border-green-mid/40 px-2 py-1 text-sm"
      />
    </label>
  );
}

async function put(url: string, body: Blob, contentType: string): Promise<void> {
  const res = await fetch(url, { method: 'PUT', body, headers: { 'content-type': contentType } });
  if (!res.ok) throw new Error(`R2 refused the upload (${res.status})`);
}

type Exif = {
  takenAt: string | null;
  camera: string | null;
  lat: number | null;
  lng: number | null;
};

async function readExif(file: File): Promise<Exif> {
  if (!file.type.startsWith('image/')) return { takenAt: null, camera: null, lat: null, lng: null };

  try {
    // Loaded on demand: exifr is not small and most batches are one shape.
    const exifr = (await import('exifr')).default;
    const data = (await exifr.parse(file, {
      pick: ['DateTimeOriginal', 'CreateDate', 'Make', 'Model', 'latitude', 'longitude'],
    })) as Record<string, unknown> | undefined;

    if (!data) return { takenAt: null, camera: null, lat: null, lng: null };

    const taken = (data.DateTimeOriginal ?? data.CreateDate) as Date | undefined;
    const make = typeof data.Make === 'string' ? data.Make.trim() : '';
    const model = typeof data.Model === 'string' ? data.Model.trim() : '';

    return {
      takenAt: taken instanceof Date ? taken.toISOString() : null,
      camera: [make, model].filter(Boolean).join(' ') || null,
      lat: typeof data.latitude === 'number' ? data.latitude : null,
      lng: typeof data.longitude === 'number' ? data.longitude : null,
    };
  } catch {
    // No EXIF, or a file that is not really a JPEG. Not worth failing over.
    return { takenAt: null, camera: null, lat: null, lng: null };
  }
}
