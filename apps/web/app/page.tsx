export default function HomePage() {
  return (
    <main className="mx-auto max-w-3xl p-8">
      <h1 className="text-2xl font-semibold">SFW Content Studio</h1>
      <p className="mt-2 text-green-mid">
        Asset library and content machine for the Soil Food Web Foundation.
      </p>
      <ul className="mt-6 space-y-2">
        <li>
          <a className="underline" href="/library">
            Library
          </a>
          <span className="text-green-mid"> — Every asset, faceted and searchable.</span>
        </li>
        <li>
          <a className="underline" href="/inbox">
            Inbox
          </a>
          <span className="text-green-mid"> — Confirm AI tags, set quality, clear to post.</span>
        </li>
        <li>
          <a className="underline" href="/clips">
            Clips
          </a>
          <span className="text-green-mid">
            {' '}
            — Clip candidates from long video, Keep / Trim / Cut.
          </span>
        </li>
        <li>
          <a className="underline" href="/week">
            Week
          </a>
          <span className="text-green-mid">
            {' '}
            — This week's posts in real phone frames, for approval.
          </span>
        </li>
        <li>
          <a className="underline" href="/scout">
            Scout
          </a>
          <span className="text-green-mid"> — News cards from the soil source list.</span>
        </li>
        <li>
          <a className="underline" href="/learned">
            What it learned
          </a>
          <span className="text-green-mid"> — Rules, evidence, weight changes, eval history.</span>
        </li>
        <li>
          <a className="underline" href="/questions">
            Questions
          </a>
          <span className="text-green-mid"> — Open questions routed to named people.</span>
        </li>
        <li>
          <a className="underline" href="/errors">
            Errors
          </a>
          <span className="text-green-mid"> — Dead jobs, with retry.</span>
        </li>
        <li>
          <a className="underline" href="/settings">
            Settings
          </a>
          <span className="text-green-mid"> — Cadence, feeds, people, prompts, cost.</span>
        </li>
      </ul>
    </main>
  );
}
