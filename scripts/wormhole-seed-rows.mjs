// Turns one planning-doc post into a Wormhole row.
export function toRow(p) {
  const slides = [];
  for (const w of p.words ?? []) {
    for (const part of String(w).split(/\n(?=Slide\s*\d+\s*:)/i)) {
      const text = part.replace(/^Slide\s*\d+\s*:\s*/i, '').trim();
      if (text) slides.push({ text, image: null });
    }
  }
  const note = String(p.status ?? '');
  const status = /approved by stephanie/i.test(note) ? 'approved' : 'draft';
  return {
    id: p.id, iso_date: p.iso, topic: p.topic ?? '', platform: p.platform ?? '',
    caption: p.caption ?? '', slides, cta: p.cta ?? '', link: p.link ?? '',
    sources: p.sources ?? [], visual_note: p.visual ?? '', note, status,
  };
}
