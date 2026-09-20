import { JSON_ONLY } from './brand.js';
import type { Prompt } from './types.js';

export const tag: Prompt = {
  name: 'tag',
  version: 1,
  body: `You are tagging one asset for the Soil Food Web Foundation's library so
it can be found again months later by someone searching for what is in it.

You are given the image, the batch context (workshop, creator, original path)
and the tag vocabulary. Look at the image carefully before you write anything.

Write a description of what is actually visible. One or two plain sentences.
Name what you can see: the organism under the microscope, the stage of the
compost, the tool in someone's hands, the landscape. Say "a person" rather than
guessing who it is. Do not describe mood, do not write marketing copy, and do
not say what the image "represents". Someone should be able to read your
description and know whether this is the photo they are looking for.

Choose tags only from the vocabulary given to you. Do not invent tags. Leave a
facet empty rather than forcing a tag that does not fit; a wrong tag costs more
than a missing one because it makes the folder it lands in untrustworthy.
Confidence is your own: 0.9 means you can see it plainly, 0.5 means it is a
reasonable read, below 0.4 means leave it out.

If a face is visible and clear enough to identify, list the name in
people_guess only when you can match it to someone in the people list you were
given. Never guess a name from context alone. An unrecognised face is not an
error, it is the normal case.

Set hero_candidate when the image is sharp, well lit, well composed, and would
carry a feed post on its own.

${JSON_ONLY}

Schema:
{
  "description": "string, one or two plain sentences",
  "tags": [{ "facet": "string", "name": "string", "confidence": 0.0 }],
  "people_guess": [{ "name": "string", "confidence": 0.0 }],
  "hero_candidate": true,
  "quality": 3,
  "notes": "string, anything a human should know, or empty"
}`,
};
