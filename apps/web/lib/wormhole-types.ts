// Shared by the server routes and the browser. No server imports here.
export type Slide = { text: string; image: string | null };

export type WormholeStatus = 'draft' | 'copy_approved' | 'approved' | 'scheduled';

export const STATUSES: { value: WormholeStatus; label: string }[] = [
  { value: 'draft', label: 'Draft' },
  { value: 'copy_approved', label: 'Copy approved (Allison)' },
  { value: 'approved', label: 'Approved (Stephanie)' },
  { value: 'scheduled', label: 'Scheduled' },
];

export type WormholePost = {
  id: string;
  iso_date: string;
  topic: string;
  platform: string;
  caption: string;
  slides: Slide[];
  cta: string;
  link: string;
  sources: string[];
  visual_note: string;
  note: string;
  status: WormholeStatus;
  updated_by: string;
  updated_at: string;
};

export const EDITABLE = [
  'iso_date',
  'topic',
  'platform',
  'caption',
  'slides',
  'cta',
  'link',
  'sources',
  'visual_note',
  'status',
] as const;
