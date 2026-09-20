/** What the API returns to the browser. Kept here so components share it. */

export type Tag = {
  name: string;
  facet: string;
  source: 'ai' | 'human';
  confirmed: boolean;
  confidence: number | null;
};

export type Asset = {
  id: string;
  type: string;
  filename: string;
  thumbUrl: string | null;
  fileUrl?: string;
  width: number | null;
  height: number | null;
  duration_s: number | null;
  clip_start_s: number | null;
  clip_end_s: number | null;
  status: string;
  quality: number | null;
  hero_candidate: boolean;
  description: string | null;
  notes: string | null;
  drive_link: string | null;
  original_path: string | null;
  creator: string | null;
  credit_line: string | null;
  taken_at: string | null;
  camera: string | null;
  release_status: string;
  created_at: string;
  workshop: string | null;
  tags: Tag[];
  people: { name: string; confirmed: boolean }[];
  used_in: number;
};

export type Facet = { facet: string; name: string; count: number };

export type SmartFolder = {
  id: number;
  name: string;
  section: 'workshops' | 'asset_types' | 'views' | 'saved';
  filters: Record<string, unknown>;
  position: number;
};

export type LibraryResponse = { assets: Asset[]; total: number; facets: Facet[] };

export const STATUS_LABELS: Record<string, string> = {
  inbox: 'Inbox',
  tagged: 'Tagged',
  cleared: 'Cleared to post',
  used: 'Used',
  archived: 'Archived',
};

export const SECTION_LABELS: Record<SmartFolder['section'], string> = {
  workshops: 'Workshops',
  asset_types: 'Asset types',
  views: 'Views',
  saved: 'Saved',
};
