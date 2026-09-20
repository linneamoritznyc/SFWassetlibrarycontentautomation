import {
  GetObjectCommand,
  PutObjectCommand,
  S3Client,
  HeadObjectCommand,
  ListObjectsV2Command,
  DeleteObjectCommand,
} from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import type { Readable } from 'node:stream';
import type { Bucket } from './keys.js';

/**
 * R2 speaks S3. The one thing that differs from AWS is the endpoint, and that
 * the region is always "auto".
 *
 * Buckets are private. Nothing is ever served from a public URL: the browser
 * gets a presigned GET that expires in an hour, and uploads go straight to R2
 * with a presigned PUT so a 4 GB video never passes through a Vercel function.
 */
export const PRESIGN_TTL_SECONDS = 3600;

let cached: S3Client | null = null;

export function r2(): S3Client {
  if (cached) return cached;

  const accountId = required('R2_ACCOUNT_ID');
  cached = new S3Client({
    region: 'auto',
    endpoint: `https://${accountId}.r2.cloudflarestorage.com`,
    credentials: {
      accessKeyId: required('R2_ACCESS_KEY_ID'),
      secretAccessKey: required('R2_SECRET_ACCESS_KEY'),
    },
  });
  return cached;
}

function required(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`${name} is not set. See .env.example and docs/TODO-LINNEA.md.`);
  return value;
}

export async function presignPut(
  bucket: Bucket,
  key: string,
  contentType: string,
): Promise<string> {
  return getSignedUrl(
    r2(),
    new PutObjectCommand({ Bucket: bucket, Key: key, ContentType: contentType }),
    {
      expiresIn: PRESIGN_TTL_SECONDS,
    },
  );
}

export async function presignGet(bucket: Bucket, key: string): Promise<string> {
  return getSignedUrl(r2(), new GetObjectCommand({ Bucket: bucket, Key: key }), {
    expiresIn: PRESIGN_TTL_SECONDS,
  });
}

export async function putObject(
  bucket: Bucket,
  key: string,
  body: Buffer | Uint8Array | string,
  contentType: string,
): Promise<void> {
  await r2().send(
    new PutObjectCommand({ Bucket: bucket, Key: key, Body: body, ContentType: contentType }),
  );
}

export async function getObject(bucket: Bucket, key: string): Promise<Buffer> {
  const res = await r2().send(new GetObjectCommand({ Bucket: bucket, Key: key }));
  const stream = res.Body as Readable;
  const chunks: Buffer[] = [];
  for await (const chunk of stream) chunks.push(Buffer.from(chunk));
  return Buffer.concat(chunks);
}

export async function objectExists(bucket: Bucket, key: string): Promise<boolean> {
  try {
    await r2().send(new HeadObjectCommand({ Bucket: bucket, Key: key }));
    return true;
  } catch {
    return false;
  }
}

export async function deleteObject(bucket: Bucket, key: string): Promise<void> {
  await r2().send(new DeleteObjectCommand({ Bucket: bucket, Key: key }));
}

export type R2Object = { key: string; size: number; lastModified?: Date };

/** Lists everything under a prefix, following continuation tokens. */
export async function listObjects(bucket: Bucket, prefix: string): Promise<R2Object[]> {
  const found: R2Object[] = [];
  let token: string | undefined;

  do {
    const res = await r2().send(
      new ListObjectsV2Command({ Bucket: bucket, Prefix: prefix, ContinuationToken: token }),
    );
    for (const item of res.Contents ?? []) {
      if (item.Key) {
        found.push({ key: item.Key, size: item.Size ?? 0, lastModified: item.LastModified });
      }
    }
    token = res.NextContinuationToken;
  } while (token);

  return found;
}
