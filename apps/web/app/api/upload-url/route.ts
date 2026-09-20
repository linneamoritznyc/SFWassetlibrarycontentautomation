import { randomUUID } from 'node:crypto';
import { NextResponse, type NextRequest } from 'next/server';
import { bucketForType, keys, presignPut, safeFilename } from '@sfw/storage';
import { fail, route } from '@/lib/http';

/**
 * Hands back presigned PUTs so the browser uploads straight to R2. A 4 GB
 * workshop video never passes through a serverless function, and no key ever
 * reaches the browser: a presigned URL is a one-hour permission to write to
 * exactly one object key.
 *
 * The asset id is minted here so the upload and the later `POST /api/assets`
 * agree on where the file went.
 */
export const POST = route(async (request: NextRequest) => {
  const body = (await request.json()) as {
    files?: { filename: string; contentType: string; type: string }[];
  };

  const files = body.files ?? [];
  if (files.length === 0) return fail('No files given');
  if (files.length > 200) return fail('Too many files in one go. Try 200 at a time.');

  const uploads = await Promise.all(
    files.map(async (file) => {
      const assetId = randomUUID();
      const bucket = bucketForType(file.type);
      const filename = safeFilename(file.filename);
      const r2Key =
        file.type === 'doc' ? keys.doc(assetId, filename) : keys.original(assetId, filename);

      return {
        assetId,
        filename,
        bucket,
        r2Key,
        thumbKey: keys.thumb(assetId),
        putUrl: await presignPut(bucket, r2Key, file.contentType || 'application/octet-stream'),
        thumbPutUrl: await presignPut('sfw-media', keys.thumb(assetId), 'image/jpeg'),
      };
    }),
  );

  return NextResponse.json({ uploads });
});
