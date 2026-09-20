/**
 * Smart folders are saved filters, not containers (PRD 5.1). One asset shows up
 * in every folder it matches. The sidebar groups them into four sections.
 */

export type AssetFilter = {
  type?: string[];
  status?: string[];
  /** Tags an asset must carry, as facet/name pairs. */
  tags?: { facet: string; name: string }[];
  /** No confirmed tags at all. */
  untagged?: boolean;
  /** Never used in a published post. */
  unused?: boolean;
  /** Free text over description, filename and notes. */
  q?: string;
};

export type SmartFolderSeed = {
  name: string;
  section: 'workshops' | 'asset_types' | 'views' | 'saved';
  filters: AssetFilter;
  position: number;
};

const WORKSHOPS = [
  'New Mexico compost workshop',
  'Wild Ken Hill',
  'Cyprus 2025',
  'India Accelerator Workshop 2026',
  'Life in the Soils seminar',
];

export const SMART_FOLDERS: SmartFolderSeed[] = [
  ...WORKSHOPS.map((name, i) => ({
    name,
    section: 'workshops' as const,
    filters: { tags: [{ facet: 'workshop', name }] },
    position: i,
  })),

  { name: 'Videos', section: 'asset_types', filters: { type: ['video'] }, position: 0 },
  { name: 'Photos', section: 'asset_types', filters: { type: ['photo'] }, position: 1 },
  { name: 'Graphics', section: 'asset_types', filters: { type: ['graphic'] }, position: 2 },
  { name: 'Clips', section: 'asset_types', filters: { type: ['clip'] }, position: 3 },
  { name: 'Documents', section: 'asset_types', filters: { type: ['doc'] }, position: 4 },
  { name: 'References', section: 'asset_types', filters: { type: ['reference'] }, position: 5 },

  { name: 'Inbox', section: 'views', filters: { status: ['inbox'] }, position: 0 },
  { name: 'Untagged', section: 'views', filters: { untagged: true }, position: 1 },
  { name: 'Unused', section: 'views', filters: { unused: true }, position: 2 },
  {
    name: 'Cleared to post',
    section: 'views',
    filters: { status: ['cleared'] },
    position: 3,
  },
  { name: 'Archived', section: 'views', filters: { status: ['archived'] }, position: 4 },
];
