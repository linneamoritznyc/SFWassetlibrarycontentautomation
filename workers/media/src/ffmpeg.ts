import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { brandFontsDir } from './fonts.js';

/**
 * A thin wrapper over the ffmpeg and ffprobe binaries.
 *
 * Deliberately not a library: ffmpeg's command line is the documented
 * interface, every recipe on the internet is in that form, and wrapping it in
 * a fluent API only makes it harder to work out what actually ran. Every
 * function here logs the exact arguments it used.
 */

export const FFMPEG = process.env.FFMPEG_PATH ?? 'ffmpeg';
export const FFPROBE = process.env.FFPROBE_PATH ?? 'ffprobe';

export class FfmpegError extends Error {
  constructor(
    message: string,
    readonly args: string[],
    readonly stderr: string,
  ) {
    super(message);
    this.name = 'FfmpegError';
  }
}

export async function run(bin: string, args: string[]): Promise<string> {
  const child = spawn(bin, args, { stdio: ['ignore', 'pipe', 'pipe'] });

  let stdout = '';
  let stderr = '';
  child.stdout.on('data', (chunk: Buffer) => {
    stdout += chunk.toString();
  });
  child.stderr.on('data', (chunk: Buffer) => {
    // ffmpeg writes progress here, so keep only the tail for error reporting.
    stderr = (stderr + chunk.toString()).slice(-8000);
  });

  const [code] = (await once(child, 'close')) as [number | null];

  if (code !== 0) {
    throw new FfmpegError(`${bin} exited ${code}`, args, stderr);
  }
  return stdout;
}

export type Probe = {
  durationS: number | null;
  width: number | null;
  height: number | null;
  hasAudio: boolean;
  videoCodec: string | null;
  audioCodec: string | null;
  fps: number | null;
};

export async function probe(path: string): Promise<Probe> {
  const raw = await run(FFPROBE, [
    '-v',
    'quiet',
    '-print_format',
    'json',
    '-show_format',
    '-show_streams',
    path,
  ]);

  const json = JSON.parse(raw) as {
    format?: { duration?: string };
    streams?: {
      codec_type?: string;
      codec_name?: string;
      width?: number;
      height?: number;
      r_frame_rate?: string;
    }[];
  };

  const video = json.streams?.find((s) => s.codec_type === 'video');
  const audio = json.streams?.find((s) => s.codec_type === 'audio');

  return {
    durationS: json.format?.duration ? Number(json.format.duration) : null,
    width: video?.width ?? null,
    height: video?.height ?? null,
    hasAudio: Boolean(audio),
    videoCodec: video?.codec_name ?? null,
    audioCodec: audio?.codec_name ?? null,
    fps: parseFps(video?.r_frame_rate),
  };
}

function parseFps(value: string | undefined): number | null {
  if (!value) return null;
  const [num, den] = value.split('/').map(Number);
  if (!num || !den) return null;
  return num / den;
}

/**
 * 720p H.264 for browser playback. The original stays untouched in sfw-raw;
 * this is what the library and the clips view actually play.
 *
 * `-movflags +faststart` moves the index to the front so the browser can start
 * playing before the whole file has arrived.
 */
export async function makeProxy(input: string, output: string): Promise<void> {
  await run(FFMPEG, [
    '-y',
    '-i',
    input,
    '-vf',
    // Never upscale, and keep dimensions even, which H.264 requires.
    "scale='min(1280,iw)':'min(720,ih)':force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2",
    '-c:v',
    'libx264',
    '-preset',
    'veryfast',
    '-crf',
    '23',
    '-pix_fmt',
    'yuv420p',
    '-c:a',
    'aac',
    '-b:a',
    '128k',
    '-movflags',
    '+faststart',
    output,
  ]);
}

/** Mono 64k AAC, which is all Whisper needs and keeps the upload small. */
export async function extractAudio(input: string, output: string): Promise<void> {
  await run(FFMPEG, [
    '-y',
    '-i',
    input,
    '-vn',
    '-ac',
    '1',
    '-ar',
    '16000',
    '-c:a',
    'aac',
    '-b:a',
    '64k',
    output,
  ]);
}

/**
 * Splits audio into chunks no longer than `seconds`.
 *
 * Whisper rejects anything over 25 MB, and an hour of workshop audio is well
 * past that. Splitting on time rather than size keeps the arithmetic for
 * shifting the word timestamps back trivial.
 */
export async function splitAudio(
  input: string,
  outputPattern: string,
  seconds: number,
): Promise<void> {
  await run(FFMPEG, [
    '-y',
    '-i',
    input,
    '-f',
    'segment',
    '-segment_time',
    String(seconds),
    '-c',
    'copy',
    '-reset_timestamps',
    '1',
    outputPattern,
  ]);
}

export type CutOptions = {
  input: string;
  output: string;
  startS: number;
  durationS: number;
  width: number;
  height: number;
  /** Path to an .ass file to burn in. Omit for no captions. */
  assPath?: string | null;
  hasAudio: boolean;
  /** Integrated loudness target, LUFS. */
  loudness?: { integrated: number; truePeak: number; range: number };
  /**
   * An ffmpeg expression for the crop's left edge, in the scaled frame's
   * coordinates. Omit for a centre crop.
   */
  cropX?: string | null;
  /** The frame the crop expression was computed against, so it can be scaled. */
  sourceWidth?: number | null;
};

/**
 * ffmpeg's filter syntax needs colons and backslashes escaped inside a value,
 * which Windows paths and absolute paths both hit.
 */
function filterValue(path: string): string {
  return `'${path.replace(/\\/g, '/').replace(/:/g, '\\:')}'`;
}

/**
 * The `ass` filter that burns a caption file in, with libass told where the
 * brand font is. `fontsdir` is searched before the system's fontconfig, so
 * the captions come out in Montserrat wherever the worker runs, and fall back
 * to whatever fontconfig has if the directory is missing.
 */
export function assFilter(assPath: string, fontsDir: string = brandFontsDir()): string {
  return `ass=${filterValue(assPath)}:fontsdir=${filterValue(fontsDir)}`;
}

/**
 * Cuts one clip out of the original and reframes it.
 *
 * `-ss` before `-i` seeks by keyframe, which is fast on a multi-gigabyte file,
 * and because the video is re-encoded anyway the cut still lands on the exact
 * frame asked for. Doing it the other way round would decode from the start of
 * the file every time.
 *
 * Reframing is a centre crop: scale until the frame is covered, then take the
 * middle. Speaker-tracking comes in Phase 8 and replaces only the crop
 * coordinates.
 */
export async function cutClip(options: CutOptions): Promise<void> {
  const { width, height } = options;

  const filters = [
    // Cover the target frame, then take a slice of it.
    `scale=${width}:${height}:force_original_aspect_ratio=increase`,
  ];

  if (options.cropX) {
    // The track was measured on the original frame; the crop happens after
    // the scale, so the expression is scaled with it. `iw` is the scaled
    // width, and min/max keep it inside the frame whatever the track says.
    const ratio = options.sourceWidth ? `*(iw/${options.sourceWidth})` : '';
    filters.push(
      `crop=${width}:${height}:x='max(0,min(iw-${width},(${options.cropX})${ratio}))':y=0`,
    );
  } else {
    filters.push(`crop=${width}:${height}`);
  }

  filters.push('setsar=1');

  if (options.assPath) filters.push(assFilter(options.assPath));

  const args = [
    '-y',
    '-ss',
    options.startS.toFixed(3),
    '-i',
    options.input,
    '-t',
    options.durationS.toFixed(3),
    '-vf',
    filters.join(','),
    '-c:v',
    'libx264',
    '-preset',
    'medium',
    '-crf',
    '20',
    '-pix_fmt',
    'yuv420p',
    '-movflags',
    '+faststart',
  ];

  if (options.hasAudio) {
    const l = options.loudness ?? { integrated: -14, truePeak: -1.5, range: 11 };
    args.push(
      '-af',
      `loudnorm=I=${l.integrated}:TP=${l.truePeak}:LRA=${l.range}`,
      '-c:a',
      'aac',
      '-b:a',
      '128k',
      '-ar',
      '48000',
    );
  } else {
    args.push('-an');
  }

  args.push(options.output);
  await run(FFMPEG, args);
}
