import { CAPTION_STYLE, FONTS } from '@sfw/brand';

export type Word = { w: string; start: number; end: number; speaker?: string | null };

/**
 * Burned-in captions in the SFW style: Montserrat 600, two lines at most, the
 * word being spoken picked out in the bright green.
 *
 * Built as ASS rather than SRT because SRT cannot colour part of a line. One
 * dialogue event is emitted per word, each showing the same one or two lines
 * with a different word highlighted, which is what produces the word-by-word
 * effect without any animation.
 */

/** ASS wants &HBBGGRR, the reverse of CSS, and with no alpha for a solid colour. */
function assColour(hex: string): string {
  const clean = hex.replace('#', '');
  const r = clean.slice(0, 2);
  const g = clean.slice(2, 4);
  const b = clean.slice(4, 6);
  return `&H00${b}${g}${r}`.toUpperCase();
}

function assTime(seconds: number): string {
  const clamped = Math.max(0, seconds);
  const h = Math.floor(clamped / 3600);
  const m = Math.floor((clamped % 3600) / 60);
  const s = Math.floor(clamped % 60);
  const cs = Math.round((clamped % 1) * 100);
  return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs).padStart(2, '0')}`;
}

/** ASS treats braces and backslashes as markup. */
function escapeAss(text: string): string {
  return text.replace(/\\/g, '\\\\').replace(/\{/g, '\\{').replace(/\}/g, '\\}');
}

/** `lines` holds indices into `words`, so rendering never has to re-derive which token is which. */
type Window = { words: Word[]; lines: number[][] };

/**
 * Groups words into what fits on screen at once: at most two lines, at most
 * roughly `charsPerLine` characters each. A window also ends at a long pause,
 * because holding a half-sentence on screen through silence looks broken.
 */
export function windowWords(words: Word[], style = CAPTION_STYLE): Window[] {
  const windows: Window[] = [];
  let lines: number[][] = [[]];
  let current: Word[] = [];

  const lineLength = (line: number[]) => line.reduce((n, i) => n + current[i]!.w.length + 1, -1);

  const flush = () => {
    if (current.length > 0) windows.push({ words: current, lines });
    current = [];
    lines = [[]];
  };

  for (const [i, word] of words.entries()) {
    const previous = words[i - 1];
    // A pause of more than a second means a new thought.
    if (previous && word.start - previous.end > 1) flush();

    let line = lines[lines.length - 1]!;

    if (line.length > 0 && lineLength(line) + 1 + word.w.length > style.charsPerLine) {
      if (lines.length >= style.maxLines) {
        flush();
        line = lines[lines.length - 1]!;
      } else {
        lines.push([]);
        line = lines[lines.length - 1]!;
      }
    }

    current.push(word);
    line.push(current.length - 1);
  }

  flush();
  return windows;
}

export function buildAss(
  words: Word[],
  frame: { width: number; height: number },
  style = CAPTION_STYLE,
): string {
  // Sizes in the tokens are for a 1080-wide frame.
  const scale = frame.width / 1080;
  const fontSize = Math.round(style.fontSize * scale);
  const marginV = Math.round(frame.height * style.marginBottomRatio);

  const header = [
    '[Script Info]',
    'ScriptType: v4.00+',
    `PlayResX: ${frame.width}`,
    `PlayResY: ${frame.height}`,
    'WrapStyle: 2',
    'ScaledBorderAndShadow: yes',
    '',
    '[V4+ Styles]',
    'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,' +
      ' BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,' +
      ' BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
    [
      'Style: SFW',
      FONTS.caption,
      String(fontSize),
      assColour(style.text),
      assColour(style.highlight),
      assColour(style.outline),
      assColour(style.outline),
      // Bold on: Montserrat 600 is the nearest the renderer can pick.
      '1',
      '0',
      '0',
      '0',
      '100',
      '100',
      '0',
      '0',
      '1',
      String(Math.round(style.outlineWidth * scale)),
      String(Math.round(style.shadowDepth * scale)),
      // 2 = bottom centre.
      '2',
      String(Math.round(frame.width * 0.06)),
      String(Math.round(frame.width * 0.06)),
      String(marginV),
      '1',
    ].join(','),
    '',
    '[Events]',
    'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
  ];

  const highlight = assColour(style.highlight);
  const normal = assColour(style.text);
  const events: string[] = [];

  for (const window of windowWords(words, style)) {
    for (const [index, word] of window.words.entries()) {
      // The same window, drawn again with the next word picked out.
      const rendered = window.lines
        .map((line) =>
          line
            .map((wordIndex) => {
              const text = escapeAss(window.words[wordIndex]!.w);
              return wordIndex === index ? `{\\c${highlight}}${text}{\\c${normal}}` : text;
            })
            .join(' '),
        )
        .join('\\N');

      const next = window.words[index + 1];
      // Hold each word until the next one starts, so there is never a gap.
      const end = next ? Math.max(word.end, next.start) : word.end + 0.3;

      events.push(`Dialogue: 0,${assTime(word.start)},${assTime(end)},SFW,,0,0,0,,${rendered}`);
    }
  }

  return [...header, ...events].join('\n');
}

/** The .srt the spec stores next to every clip, for anything that wants plain captions. */
export function buildSrt(words: Word[], style = CAPTION_STYLE): string {
  const blocks: string[] = [];

  for (const [i, window] of windowWords(words, style).entries()) {
    const first = window.words[0];
    const last = window.words[window.words.length - 1];
    if (!first || !last) continue;

    blocks.push(
      String(i + 1),
      `${srtTime(first.start)} --> ${srtTime(last.end)}`,
      window.lines.map((line) => line.map((i) => window.words[i]!.w).join(' ')).join('\n'),
      '',
    );
  }

  return blocks.join('\n');
}

function srtTime(seconds: number): string {
  const clamped = Math.max(0, seconds);
  const h = Math.floor(clamped / 3600);
  const m = Math.floor((clamped % 3600) / 60);
  const s = Math.floor(clamped % 60);
  const ms = Math.round((clamped % 1) * 1000);
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
}

/** Shifts word times so a clip's captions start at zero. */
export function shiftWords(words: Word[], by: number): Word[] {
  return words.map((w) => ({ ...w, start: w.start - by, end: w.end - by }));
}

/** The words that fall inside a clip, clipped at its edges. */
export function wordsBetween(words: Word[], start: number, end: number): Word[] {
  return words
    .filter((w) => w.end > start && w.start < end)
    .map((w) => ({ ...w, start: Math.max(w.start, start), end: Math.min(w.end, end) }));
}
