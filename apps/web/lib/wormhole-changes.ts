/**
 * Planned changes to posts, written in code and applied by Wormhole itself.
 *
 * Each change runs once: it goes through the normal edit path (savePost), and
 * its key is kept as the editor of that version ("Change: <key>"), which is how
 * Wormhole knows it already ran. The reason goes on top of the post's note.
 *
 * Add a change here, push, and the next time anyone opens Wormhole it is in.
 */
import { db } from './db';
import { savePost } from './wormhole';
import type { WormholePost } from './wormhole-types';

type Change = {
  key: string;
  post: string;
  set?: Partial<Pick<WormholePost, 'iso_date' | 'date_tbd' | 'slides'>>;
  /** A new post, inserted when no post has this id yet. */
  create?: Omit<WormholePost, 'id' | 'updated_by' | 'updated_at' | 'pinned'>;
  /** Plain text replacements in the caption: [from, to]. */
  caption?: [string, string][];
  reason: string;
};

const MENTORS = 'No staff or mentor posts have gone out yet; one a day from 21 Oct.';

export const CHANGES: Change[] = [
  {
    key: '2026-10-20 d25',
    post: 'd25',
    set: { iso_date: '2026-11-07', date_tbd: false },
    reason: 'Moved from 17 Oct to Sat 7 Nov (Linnea, 20 Oct): never posted, saved for later.',
  },
  {
    key: '2026-10-20 d26',
    post: 'd26',
    set: { date_tbd: true },
    reason:
      'Date TBD (Linnea, 20 Oct): Linnea dislikes the design, it needs a new visual. Was 18 Oct, never posted.',
  },
  {
    key: '2026-10-20 p05',
    post: 'p05',
    set: { iso_date: '2026-10-26', date_tbd: false },
    reason: 'Moved from 19 Oct to Mon 26 Oct (Linnea, 20 Oct): it was never posted on 19 Oct.',
  },
  {
    key: '2026-10-20 p07',
    post: 'p07',
    set: { date_tbd: true },
    reason: 'DO NOT POST: she no longer works with SFW (Linnea, 20 Oct). Was 21 Oct.',
  },
  {
    key: '2026-10-20 d05',
    post: 'd05',
    caption: [['with Dr. Elaine Ingham and Dr. Caterina Capri on', 'with Dr. Elaine Ingham on']],
    reason:
      'Removed Dr. Caterina Capri from the caption (Linnea, 20 Oct): she no longer works with SFW.',
  },
  {
    key: '2026-10-20 p02',
    post: 'p02',
    set: { iso_date: '2026-10-21', date_tbd: false },
    reason: `Moved from 17 Oct to Wed 21 Oct (Linnea, 20 Oct). ${MENTORS}`,
  },
  {
    key: '2026-10-20 p03',
    post: 'p03',
    set: { iso_date: '2026-10-22', date_tbd: false },
    reason: `Moved from 18 Oct to Thu 22 Oct (Linnea, 20 Oct). ${MENTORS}`,
  },
  {
    key: '2026-10-20 p04',
    post: 'p04',
    set: { iso_date: '2026-10-23', date_tbd: false },
    reason: `Moved from 19 Oct to Fri 23 Oct (Linnea, 20 Oct). ${MENTORS}`,
  },
  {
    key: '2026-10-20 p06',
    post: 'p06',
    set: { iso_date: '2026-10-24', date_tbd: false },
    reason: `Moved from 20 Oct to Sat 24 Oct (Linnea, 20 Oct). ${MENTORS}`,
  },
  {
    key: '2026-10-20 p09',
    post: 'p09',
    set: { iso_date: '2026-10-25', date_tbd: false },
    reason: `Moved from 22 Oct to Sun 25 Oct (Linnea, 20 Oct). ${MENTORS}`,
  },
  {
    key: '2026-10-20 p08 slides',
    post: 'p08',
    set: {
      slides: [
        {
          text: 'Happy World Earthworm Day! How do worms work their magic?',
          image: '/wormhole/tiles/p08-1.jpg',
        },
        {
          text: 'Anecic earthworms dig vertical burrows that can reach 1 to 2 meters deep to break up compaction.',
          image: '/wormhole/tiles/p08-2.jpg',
        },
        {
          text: 'They spread microbes around as they move by lining the walls with mucus and casts, rich in nutrients and microbes.',
          image: '/wormhole/tiles/p08-3.jpg',
        },
        {
          text: 'Their channels let rain soak in fast without causing the ground to go anaerobic.',
          image: '/wormhole/tiles/p08-4.jpg',
        },
        { text: 'How to care for them?', image: '/wormhole/tiles/p08-5.jpg' },
        {
          text: 'Digging cuts the burrows. No-dig keeps the plumbing intact.',
          image: '/wormhole/tiles/p08-6.jpg',
        },
        {
          text: "Add organic matter (or simply don't remove it).",
          image: '/wormhole/tiles/p08-7.jpg',
        },
      ],
    },
    reason:
      "New slides (Linnea, 20 Oct): the doc's own slide text in the earthworm-cover style. Deck: 21-10-2026-world-earthworm-day.pptx.",
  },
  {
    key: '2026-10-20 n20261023a',
    post: 'n20261023a',
    create: {
      iso_date: '2026-10-27',
      date_tbd: false,
      topic: 'Soil news: a mustard plant shares nutrients with an ancient soil fungus',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "A plant that biologists thought could never partner with fungi just traded food with one! 🌱\nResearchers at the University of Sheffield, led by Professor Katie Field, grew Arabidopsis, a small mustard plant and the most studied plant in biology, alongside an ancient soil fungus called a Mucoromycotina fine root endophyte. The mustard family lost the genes most plants use to welcome fungal partners millions of years ago, so everyone assumed it could not do this. The new study shows it can.\nThe fungus carried nitrogen and phosphorus from the soil into the plant's shoots, and in return it received more than 260% more of the plant's carbon. It did the plant no harm.\nCabbage, canola and mustard belong to the same family, and the team now wants to learn what this means for crops. For us it is one more reminder that the soil food web reaches further than the textbooks said.\nRead the study through the link in bio.\n#SoilFoodWeb #SoilBiology #SoilFungi #Mycorrhiza #LivingSoil #PlantScience",
      slides: [
        {
          text: 'A plant everyone said lives without fungi just proved them wrong. University of Sheffield, Current Biology, October 2026',
          image: '/wormhole/tiles/n20261023a-1.jpg',
        },
        {
          text: "The fungus carried nitrogen and phosphorus into the plant. It took more than 260% more of the plant's carbon in return.",
          image: '/wormhole/tiles/n20261023a-2.jpg',
        },
        {
          text: 'Mustards and their cabbage cousins were thought to skip this partnership. Next the team wants to know which crops do it too. Look closer, there is life.',
          image: '/wormhole/tiles/n20261023a-3.jpg',
        },
      ],
      cta: 'Read the study, link in bio',
      link: 'https://phys.org/news/2026-10-ancient-fungus-secret-major-food.html',
      sources: [
        'https://phys.org/news/2026-10-ancient-fungus-secret-major-food.html',
        'https://doi.org/10.1016/j.cub.2026.09.061',
      ],
      visual_note:
        'Collage carousel, 3 slides, one soil profile under all three. Deck: news-mustard-plant-fungus.pptx. LinkedIn: end with a question, e.g. "Which crops on your farm might have fungal partners nobody has looked for?"',
      note: "Found by Scout on 20 Oct 2026 (Phys.org, Agriculture feed). The study used Arabidopsis only; the crop link is the researchers' next question, so the caption does not claim it for crops.",
      status: 'draft',
    },
    reason:
      'Scout news draft, added 20 Oct for Tue 27 Oct (the first free day after the staff week).',
  },
  {
    key: '2026-10-20 n20261024a',
    post: 'n20261024a',
    create: {
      iso_date: '2026-10-28',
      date_tbd: false,
      topic: 'Soil news: restored land can look finished while its soil fungi lag behind',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Can a restored landscape look finished while the life in its soil is still catching up? 🌳\nA team at Flinders University in Australia, led by Professor Martin Breed, went back to replanted former farmland and sampled its soil fungi again six years later. What the fungi do in the soil kept recovering over those six years, while the fungal community as a whole changed very little.\nThe researchers point to the land's farming history and the high nutrient levels still in those soils as a likely brake. Trees and shrubs are the part of restoration we can see and count. The soil food web follows on its own timeline, and it deserves to be measured too.\nRead the study through the link in bio.\n#SoilFoodWeb #SoilFungi #EcologicalRestoration #LivingSoil #SoilHealth #SoilBiology",
      slides: [
        {
          text: 'Restored land can look finished while the fungi below are still catching up. Flinders University, Molecular Ecology, October 2026',
          image: '/wormhole/tiles/n20261024a-1.jpg',
        },
        {
          text: 'Over six years, what the fungi do in the soil kept recovering. The fungal community as a whole changed very little.',
          image: '/wormhole/tiles/n20261024a-2.jpg',
        },
        {
          text: 'The team points to the farming history: soils still rich in leftover nutrients. Trees are the part of restoration we can count. The soil food web takes longer.',
          image: '/wormhole/tiles/n20261024a-3.jpg',
        },
      ],
      cta: 'Read the study, link in bio',
      link: 'https://phys.org/news/2026-10-replanted-landscapes-soil-fungi-lag.html',
      sources: [
        'https://phys.org/news/2026-10-replanted-landscapes-soil-fungi-lag.html',
        'https://doi.org/10.1111/mec.70552',
      ],
      visual_note:
        'Collage carousel, 3 slides, fungal threads thinning from slide 1 to 3. Deck: news-restored-land-soil-fungi.pptx. LinkedIn: end with a question, e.g. "How do you measure whether a restoration is finished below ground?"',
      note: 'Found by Scout on 20 Oct 2026 (Phys.org, Agriculture feed).',
      status: 'draft',
    },
    reason: 'Scout news draft, added 20 Oct for Wed 28 Oct.',
  },
];

const editorOf = (c: Change) => `Change: ${c.key}`;
let done = false;

/** Applies every change that has not run yet. Cheap after the first call. */
export async function applyChanges(): Promise<void> {
  if (done) return;
  const { rows } = await db().query<{ editor: string }>(
    `select distinct editor from wormhole_versions where editor like 'Change: %'`,
  );
  const ran = new Set(rows.map((r) => r.editor));
  for (const c of CHANGES) {
    if (ran.has(editorOf(c))) continue;
    const { rows: found } = await db().query<{ caption: string; note: string }>(
      `select caption, note from wormhole_posts where id = $1`,
      [c.post],
    );
    const current = found[0];
    if (!current) {
      if (c.create) {
        const p = c.create;
        await db().query(
          `insert into wormhole_posts (id, iso_date, date_tbd, topic, platform, caption, slides, cta, link,
             sources, visual_note, note, status, created_by, updated_by)
           values ($1,$2,$3,$4,$5,$6,$7::jsonb,$8,$9,$10::jsonb,$11,$12,$13,$14,$14)
           on conflict (id) do nothing`,
          [
            c.post,
            p.iso_date,
            p.date_tbd,
            p.topic,
            p.platform,
            p.caption,
            JSON.stringify(p.slides),
            p.cta,
            p.link,
            JSON.stringify(p.sources),
            p.visual_note,
            `${c.reason}\n${p.note}`,
            p.status,
            editorOf(c),
          ],
        );
        await db().query(
          `insert into wormhole_versions (post_id, data, editor) values ($1, $2, $3)`,
          [c.post, JSON.stringify(p), editorOf(c)],
        );
      }
      continue;
    }
    let caption = current.caption;
    for (const [from, to] of c.caption ?? []) caption = caption.split(from).join(to);
    const note = current.note ? `${c.reason}\n${current.note}` : c.reason;
    await savePost(c.post, { ...c.set, ...(c.caption ? { caption } : {}), note }, editorOf(c));
  }
  done = true;
}
