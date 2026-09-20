import { Composition, registerRoot } from 'remotion';
import { FieldNotes } from './FieldNotes.js';
import { WorkshopMoment } from './WorkshopMoment.js';
import { fieldNotesSchema, FPS, FRAME, totalFrames, workshopMomentSchema } from './schema.js';

/**
 * The compositions the renderer can be asked for.
 *
 * `calculateMetadata` works the length out from the clips it was given, so a
 * render is never padded with black or cut off: the job hands over clips and
 * the composition is exactly as long as they are, plus the two cards.
 */
export function RemotionRoot() {
  return (
    <>
      <Composition
        id="FieldNotes"
        component={FieldNotes}
        schema={fieldNotesSchema}
        fps={FPS}
        width={FRAME.width}
        height={FRAME.height}
        durationInFrames={Math.round(FPS * 30)}
        defaultProps={{
          eyebrow: 'Field Notes No. 01',
          title: 'Butternut squash on fallow clay',
          subtitle: 'Sandra Niggemeyer · Van, Texas · last season',
          clips: [],
          endCard:
            'Practicum graduates publish their trials, including the ones that did not work.',
          ctaUrl: 'soilfoodweb.com',
        }}
        calculateMetadata={({ props }) => ({ durationInFrames: totalFrames(props.clips) })}
      />

      <Composition
        id="WorkshopMoment"
        component={WorkshopMoment}
        schema={workshopMomentSchema}
        fps={FPS}
        width={FRAME.width}
        height={FRAME.height}
        durationInFrames={Math.round(FPS * 30)}
        defaultProps={{
          hook: 'The most is learned from failed piles',
          speaker: 'Loida Vasquez',
          place: 'Coimbatore, Tamil Nadu',
          clips: [],
          endCard: 'Learn in person at the next Accelerator Workshop.',
          ctaUrl: 'school.soilfoodweb.com',
        }}
        calculateMetadata={({ props }) => ({ durationInFrames: totalFrames(props.clips) })}
      />
    </>
  );
}

registerRoot(RemotionRoot);
