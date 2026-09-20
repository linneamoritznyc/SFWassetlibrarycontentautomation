import { JSON_ONLY } from './brand.js';
import type { Prompt } from './types.js';

export const pasteIntake: Prompt = {
  name: 'paste_intake',
  version: 1,
  body: `Someone pasted a screenshot into the Soil Food Web Foundation's content
studio. Read it and say what is in it.

It is usually a message from a colleague: a Google Chat message, an email, a
Slack thread, a social post, or an article. Often it is someone sharing a link
with a line like "More good news to share!".

The image is attached. Read the text in it literally, including the link
preview card at the bottom if there is one.

Pull out:

- Who sent it, exactly as the screenshot shows the name.
- When, exactly as shown. Do not convert it to a date.
- What they wrote, word for word, without their signature or the app's
  furniture.
- Every URL. Read them carefully from the image, character by character. A link
  that wraps across two lines is one URL: join it with no space and no hyphen. If
  you cannot read a URL with confidence, put it in unreadable_urls instead of
  guessing, because a wrong URL sends the next step to the wrong page.
- The link preview title and the source domain, if a preview card is shown.
- A plain description of any photograph in the screenshot.

Then one judgement that matters more than the rest.

is_sfw_material: is the imagery in this screenshot something the Foundation
could publish as its own? It is true only for the Foundation's own workshop
photos, microscopy, field photos, or a portrait supplied by the person in it.
It is false for a screenshot of a chat window, a stock photo, another
organisation's photography, and anything you are unsure about. Default to
false. The Foundation publishes real SFW images only, so a false here stops the
photo being used as a post visual, which is the right outcome almost every
time.

sensitive: true when the screenshot contains anything that should not travel,
such as a personal phone number, a home address, an unannounced decision, or
talk about a named person's employment. A human is told before it goes further.

${JSON_ONLY}

Schema:
{
  "kind": "chat | email | social | article | document | other",
  "sender": "string, or empty",
  "sent_at": "string as shown, or empty",
  "message_text": "string, word for word, or empty",
  "urls": ["string"],
  "unreadable_urls": ["string, your best partial read"],
  "link_preview_title": "string, or empty",
  "link_preview_source": "string, the domain, or empty",
  "image_description": "string, or empty",
  "is_sfw_material": false,
  "sensitive": false,
  "note": "string, anything a human should know, or empty"
}`,
};
