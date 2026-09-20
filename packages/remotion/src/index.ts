/**
 * What the render worker imports. The templates themselves are only ever
 * loaded by Remotion's bundler, through `src/Root.tsx`.
 */
export {
  fieldNotesSchema,
  workshopMomentSchema,
  clipSchema,
  totalFrames,
  FPS,
  FRAME,
  INTRO_SECONDS,
  END_SECONDS,
  type FieldNotesProps,
  type WorkshopMomentProps,
} from './schema.js';

/** The composition ids registered in Root.tsx. */
export const TEMPLATES = ['FieldNotes', 'WorkshopMoment'] as const;

export type Template = (typeof TEMPLATES)[number];

export function isTemplate(value: string): value is Template {
  return (TEMPLATES as readonly string[]).includes(value);
}

/** Where the bundler should start. Resolved from this package's root. */
export const ENTRY_POINT = 'src/Root.tsx';
