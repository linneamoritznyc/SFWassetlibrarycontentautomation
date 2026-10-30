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
import { GAP_CHANGES } from './wormhole-changes-gaps';
import { JAN_CHANGES } from './wormhole-changes-jan';
import { OCT27_CHANGES } from './wormhole-changes-1027';

export type Change = {
  key: string;
  post: string;
  set?: Partial<
    Pick<
      WormholePost,
      'iso_date' | 'date_tbd' | 'topic' | 'slides' | 'link' | 'sources' | 'visual_note'
    >
  >;
  /** A new post, inserted when no post has this id yet. */
  create?: Omit<WormholePost, 'id' | 'updated_by' | 'updated_at' | 'pinned'>;
  /** Plain text replacements in the caption: [from, to]. */
  caption?: [string, string][];
  /** Replace the whole caption. */
  captionText?: string;
  /** Delete the post (its versions go with it). */
  remove?: true;
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
  {
    key: '2026-10-21 p02 slides',
    post: 'p02',
    set: {
      slides: [
        { text: 'Meet our mentors Casey Williams', image: '/wormhole/tiles/p02-1.jpg' },
        {
          text: 'Casey learns from his students as much as he teaches them. A bacterial-feeding nematode at 40x, photographed by Casey.',
          image: '/wormhole/tiles/p02-2.jpg',
        },
        {
          text: 'His advice: put your hands in the soil. We learn best by doing. Thank you, Casey!',
          image: '/wormhole/tiles/p02-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21) , each mentor in their own style. Deck: 21-10-2026-meet-casey-williams.pptx.',
  },
  {
    key: '2026-10-21 p03 slides',
    post: 'p03',
    set: {
      slides: [
        { text: 'Meet our mentors Nick Padwick', image: '/wormhole/tiles/p03-1.jpg' },
        {
          text: 'More than 40 years farming at scale, in the UK, Italy, Spain and Argentina.',
          image: '/wormhole/tiles/p03-2.jpg',
        },
        {
          text: 'Today he makes around 750 tons of compost a year in Norfolk. Thank you, Nick, for showing our students what this looks like at scale.',
          image: '/wormhole/tiles/p03-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21) , each mentor in their own style. Deck: 22-10-2026-meet-nick-padwick.pptx.',
  },
  {
    key: '2026-10-21 p04 slides',
    post: 'p04',
    set: {
      slides: [
        {
          text: 'Meet our mentors Wes Sander Microscopy mentor',
          image: '/wormhole/tiles/p04-1.jpg',
        },
        {
          text: 'His favourite organism: the Arcella amoeba. “You can almost see inside it. So cool.”',
          image: '/wormhole/tiles/p04-2.jpg',
        },
        {
          text: "“It depends,” as Dr. Elaine loved to say. Wes's advice: success hinges on reading the signs. Thank you, Wes!",
          image: '/wormhole/tiles/p04-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21) , each mentor in their own style. Deck: 23-10-2026-meet-wes-sander.pptx.',
  },
  {
    key: '2026-10-21 p06 slides',
    post: 'p06',
    set: {
      slides: [
        { text: 'Meet our mentors Gerald Ramirez', image: '/wormhole/tiles/p06-1.jpg' },
        {
          text: 'Gerald teaches students to make compost extracts and teas. Costa Rica, March 2025.',
          image: '/wormhole/tiles/p06-2.jpg',
        },
        {
          text: 'They carry living biology from the compost out onto the fields. Thank you, Gerald!',
          image: '/wormhole/tiles/p06-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21) , each mentor in their own style. Deck: 24-10-2026-meet-gerald-ramirez.pptx.',
  },
  {
    key: '2026-10-21 p09 slides',
    post: 'p09',
    set: {
      slides: [
        { text: 'Meet our mentors Dora Tkalec', image: '/wormhole/tiles/p09-1.jpg' },
        {
          text: 'Her favourite microbe: the naked amoeba. A slimy splotch that changes shape, and still every species keeps its own.',
          image: '/wormhole/tiles/p09-2.jpg',
        },
        {
          text: 'She has seen BioComplete™ compost extract help plants resist disease. Thank you, Dora!',
          image: '/wormhole/tiles/p09-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21) , each mentor in their own style. Deck: 25-10-2026-meet-dora-tkalec.pptx.',
  },
  {
    key: '2026-10-21-varied p02 slides',
    post: 'p02',
    set: {
      slides: [
        { text: 'Meet our mentors Casey Williams', image: '/wormhole/tiles/p02-1.jpg' },
        {
          text: '“I am deeply grateful that I get to learn from my students as well as teach them.” A bacterial-feeding nematode at 40x, photographed by Casey.',
          image: '/wormhole/tiles/p02-2.jpg',
        },
        {
          text: 'His advice: put your hands in the soil. We learn best by doing. Thank you, Casey!',
          image: '/wormhole/tiles/p02-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21-varied) , each mentor in their own style. Deck: 21-10-2026-meet-casey-williams.pptx.',
  },
  {
    key: '2026-10-21-varied p03 slides',
    post: 'p03',
    set: {
      slides: [
        {
          text: 'Meet our mentors Nick Padwick Norfolk, England',
          image: '/wormhole/tiles/p03-1.jpg',
        },
        {
          text: 'More than 40 years farming at scale, in the UK, Italy, Spain and Argentina.',
          image: '/wormhole/tiles/p03-2.jpg',
        },
        {
          text: 'Today he makes around 750 tons of compost a year. Thank you, Nick, for showing our students what this looks like at scale.',
          image: '/wormhole/tiles/p03-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21-varied) , each mentor in their own style. Deck: 22-10-2026-meet-nick-padwick.pptx.',
  },
  {
    key: '2026-10-21-varied p04 slides',
    post: 'p04',
    set: {
      slides: [
        {
          text: 'Meet our mentors Wes Sander Microscopy mentor',
          image: '/wormhole/tiles/p04-1.jpg',
        },
        {
          text: "His favourite organism: the Arcella amoeba. “There's just something about that large test that you can almost see inside of, with the amoeba squished up against the wall. So cool.” Arcella at 40x, photographed by student Mark Horton.",
          image: '/wormhole/tiles/p04-2.jpg',
        },
        {
          text: "“It depends,” as Dr. Elaine loved to say. Wes's advice: success hinges on reading the signs. Thank you, Wes!",
          image: '/wormhole/tiles/p04-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21-varied) , each mentor in their own style. Deck: 23-10-2026-meet-wes-sander.pptx.',
  },
  {
    key: '2026-10-21-varied p06 slides',
    post: 'p06',
    set: {
      slides: [
        { text: 'Meet our mentors Gerald Ramirez', image: '/wormhole/tiles/p06-1.jpg' },
        {
          text: 'Gerald teaches students to make compost extracts and teas. Costa Rica, March 2025',
          image: '/wormhole/tiles/p06-2.jpg',
        },
        {
          text: 'They carry living biology from the compost out onto the fields. Thank you, Gerald!',
          image: '/wormhole/tiles/p06-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21-varied) , each mentor in their own style. Deck: 24-10-2026-meet-gerald-ramirez.pptx.',
  },
  {
    key: '2026-10-21-varied p09 slides',
    post: 'p09',
    set: {
      slides: [
        { text: 'Meet our mentors Dora Tkalec', image: '/wormhole/tiles/p09-1.jpg' },
        {
          text: 'Her favourite microbe: the naked amoeba. “A slimy splotch that changes shape, and every species keeps its own.”',
          image: '/wormhole/tiles/p09-2.jpg',
        },
        {
          text: '“I have seen plants treated with BioComplete™ compost extract being more resistant to bacterial disease.” Thank you, Dora!',
          image: '/wormhole/tiles/p09-3.jpg',
        },
      ],
    },
    reason:
      'New slides (2026-10-21-varied) , each mentor in their own style. Deck: 25-10-2026-meet-dora-tkalec.pptx.',
  },
  {
    key: '2026-10-23 plan pl20261102',
    post: 'pl20261102',
    create: {
      iso_date: '2026-11-02',
      date_tbd: false,
      topic: 'Read the drop: meet the nematodes by their mouthparts',
      platform: 'Instagram Reel',
      caption:
        'Every nematode tells you what it eats. Look at the mouth. 🔬\nBacterial feeders have an open, tube-shaped mouth. Fungal feeders carry a thin stylet, a hollow spear, to pierce fungal hyphae. Root feeders have a heavier stylet for plant roots, and predators have teeth or a wide mouth for eating other nematodes. The balance between these groups tells a consultant whether nutrients are cycling or roots are under attack.\n💾 Save this for your next slide.\n#Nematodes #Microscopy #SoilBiology #SoilFoodWeb',
      slides: [
        { text: 'Bacterial feeder: open, tube-shaped mouth', image: null },
        { text: 'Fungal feeder: a thin stylet to pierce hyphae', image: null },
        { text: 'Root feeder: a heavy stylet to pierce roots', image: null },
        { text: 'Predator: teeth or a wide mouth', image: null },
        { text: 'Read the mouth, know the job.', image: null },
      ],
      cta: 'Save this for your next slide',
      link: '',
      sources: [
        'https://scholar.google.com/scholar?q=Yeates+1993+Feeding+habits+in+soil+nematode+families+and+genera',
      ],
      visual_note:
        'Reel, 15 to 20 seconds, one label as each nematode appears. Footage: repo microscopy of nematodes. Cover: four nematode heads side by side.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261107',
    post: 'pl20261107',
    create: {
      iso_date: '2026-11-07',
      date_tbd: false,
      topic: 'Field Notes #1',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "[PLACEHOLDER] Open with the result number, then the question, method and the honest surprise, in the graduate's words.\n#FieldNotes #SoilFoodWeb #SoilScience",
      slides: [
        { text: 'Trial name, place and season.', image: null },
        { text: 'The question they tested.', image: null },
        { text: 'The method in 3 lines.', image: null },
        { text: 'The result, one big number.', image: null },
        { text: "What surprised them, including what didn't work.", image: null },
        { text: 'Who ran it.', image: null },
      ],
      cta: 'Save this trial',
      link: 'Collab with the graduate.',
      sources: [
        'https://docs.google.com/spreadsheets/d/10UHLwzJLBQAsmJqmg4hiCQRjBKXPAx7UnOudU-Vsg5U/edit',
      ],
      visual_note:
        "Carousel, 6 slides, field notebook style. Graduate trial still to pick from the impact sheet. Use the graduate's own trial photos.",
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261114',
    post: 'pl20261114',
    create: {
      iso_date: '2026-11-14',
      date_tbd: false,
      topic: 'Do this weekend: make leaf mold',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Before you bag your leaves, try this. 🍂\nLeaf mold is compost made almost entirely by fungi. Pack damp leaves into a wire cage or a bag with holes and leave them. Fungi break down the lignin slowly, and in one to two years you get a dark, crumbly, fungal-rich material that's perfect as mulch or in potting mixes.\n💾 Save this for raking day.\n#LeafMold #Compost #FallGarden #SoilFoodWeb",
      slides: [
        { text: 'Your fallen leaves can become fungal compost.', image: null },
        { text: 'Pack wet leaves into a wire cage or a bag with holes.', image: null },
        { text: 'Keep them damp. Fungi do the work, slowly.', image: null },
        { text: 'In 1 to 2 years you get dark, crumbly leaf mold.', image: null },
        { text: 'Use it as mulch or mix it into potting soil.', image: null },
      ],
      cta: 'Save this for raking day',
      link: '',
      sources: ['https://www.rhs.org.uk/soil-composts-mulches/leafmould'],
      visual_note:
        'Carousel, 5 step slides. Wire cage full of leaves, fungal threads in the leaves, a hand holding dark leaf mold. Verify the RHS link.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261115',
    post: 'pl20261115',
    create: {
      iso_date: '2026-11-15',
      date_tbd: false,
      topic: 'A world without worms already exists',
      platform: 'Instagram Reel',
      caption:
        "A world without earthworms already exists, and you can walk through it. 🌲\nAfter the last Ice Age, glaciers scraped the earthworms out of large parts of northern North America. The forests that grew back evolved without them, on a thick layer of slowly decaying leaf litter full of fungi. Today, earthworms introduced through fishing bait, gardens and soil movement are eating through that litter layer, and the forest floor is changing with it.\nIt's a good reminder for everyone who works with soil: an organism's value depends on the system it lives in.\n📤 Send this to the gardener who thinks worms are always good news.\n#Earthworms #SoilEcology #ForestSoil #SoilFoodWeb",
      slides: [
        { text: 'Imagine a world without earthworms.', image: null },
        { text: 'It already exists.', image: null },
        {
          text: 'Many northern North American forests evolved without them after the last Ice Age.',
          image: null,
        },
        {
          text: 'Introduced worms now eat through the leaf litter those forests depend on.',
          image: null,
        },
        { text: 'Even a good organism can be the wrong one in the wrong place.', image: null },
      ],
      cta: 'Send this to the gardener who thinks worms are always good news',
      link: '',
      sources: [
        "https://scholar.google.com/scholar?q=Hendrix+2008+Pandora's+box+contained+bait+introduced+earthworms",
      ],
      visual_note:
        'Reel, 20 to 30 seconds. Northern forest floor footage, an earthworm crossing a thick leaf litter layer. Idea: Stina (SLU).',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261116',
    post: 'pl20261116',
    create: {
      iso_date: '2026-11-16',
      date_tbd: false,
      topic: 'Myth vs mechanism: the "wood wide web" is overstated',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'The "wood wide web" is one of the most shared ideas in soil science, and the evidence is weaker than the story. 🌳\nMycorrhizal fungi do connect the roots of neighboring trees. But a 2023 review in Nature Ecology and Evolution found that field evidence for trees sending meaningful resources to each other through those networks is thin, and that popular claims had outrun the data. What is solid: each tree trades sugars with its fungal partners for nutrients and water. That\'s remarkable on its own.\n📤 Send this to the friend who loved that tree documentary.\n#Mycorrhiza #ForestScience #MythVsMechanism #SoilFoodWeb',
      slides: [
        {
          text: 'Myth: "Mother trees feed their seedlings through a fungal internet."',
          image: null,
        },
        {
          text: 'Mycorrhizal fungi do connect the roots of different trees. That part is real.',
          image: null,
        },
        {
          text: 'But field evidence that trees send meaningful resources to each other through them is thin.',
          image: null,
        },
        {
          text: 'A 2023 review found positive citation bias: papers cited the dramatic claims more than the data supported.',
          image: null,
        },
        {
          text: 'What is solid: mycorrhizal fungi trade nutrients and water for plant sugars, one plant at a time.',
          image: null,
        },
        { text: 'Real science is exciting enough. Source on the slide.', image: null },
      ],
      cta: 'Send this to the friend who loved that tree documentary',
      link: '',
      sources: [
        'https://scholar.google.com/scholar?q=Karst+2023+Positive+citation+bias+overinterpreted+results+common+mycorrhizal+networks+forests',
      ],
      visual_note:
        'Carousel, 6 slides. Two tree root systems with fungal threads between them, a single root tip wrapped in hyphae.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261121',
    post: 'pl20261121',
    create: {
      iso_date: '2026-11-21',
      date_tbd: false,
      topic: 'Do this weekend: cover bare beds before winter',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Bare soil in winter is soil you're losing. 🌧️\nRaindrops hit exposed soil hard enough to break its aggregates apart, and the finest, richest particles wash away. A layer of leaves, straw, woodchips or a winter cover crop takes the hit instead, and the soil life underneath keeps working all season.\n💾 Save this for your fall cleanup.\n#SoilCover #FallGarden #SoilHealth #SoilFoodWeb",
      slides: [
        { text: "Bare soil in winter is soil you're losing.", image: null },
        {
          text: 'Rain hits bare soil hard, breaks aggregates apart and washes the fine particles away.',
          image: null,
        },
        { text: 'Cover it: leaf mulch, straw, woodchips or a winter cover crop.', image: null },
        {
          text: 'Soil life keeps working under the cover, and your beds are ready in spring.',
          image: null,
        },
      ],
      cta: 'Save this for your fall cleanup',
      link: '',
      sources: [
        'https://www.nrcs.usda.gov/conservation-basics/natural-resource-concerns/soil/soil-health',
      ],
      visual_note:
        'Carousel, 4 slides. Raindrop hitting dry soil, a row of four covers (leaves, straw, woodchips, cover crop), a mulched bed. Verify the NRCS link.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261123',
    post: 'pl20261123',
    create: {
      iso_date: '2026-11-23',
      date_tbd: false,
      topic: 'Two levels: soil aggregates, explained twice',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Two levels, one idea. Swipe until it gets too nerdy for you. 🤓\nLevel 1: healthy soil forms crumbs, and those crumbs are held together by roots, fungi and bacteria. Level 2: microaggregates are bound by persistent organic compounds, while macroaggregates are held by roots and fungal hyphae, so they fall apart when tillage cuts those networks.\n💾 Save this for the day level 2 clicks.\n#SoilStructure #SoilScience #TwoLevels #SoilFoodWeb',
      slides: [
        {
          text: 'Soil aggregates, explained twice. Level 1 for new gardeners, level 2 for consultants.',
          image: null,
        },
        {
          text: 'Level 1: Healthy soil clumps into crumbs. Those crumbs are aggregates.',
          image: null,
        },
        { text: 'Level 1: Roots, fungi and bacteria glue them together.', image: null },
        { text: 'Level 1: Crumbs leave spaces for air, water and roots.', image: null },
        {
          text: 'Level 2: Microaggregates are bound by persistent organic compounds and bacterial glues.',
          image: null,
        },
        {
          text: 'Level 2: Macroaggregates are held by roots and fungal hyphae, so they break down when tillage cuts those networks.',
          image: null,
        },
        { text: 'Source: Tisdall and Oades, 1982.', image: null },
      ],
      cta: 'Save this for the day level 2 clicks',
      link: '',
      sources: [
        'https://scholar.google.com/scholar?q=Tisdall+Oades+1982+Organic+matter+and+water-stable+aggregates+in+soils',
      ],
      visual_note:
        'Carousel, 7 slides. A soil crumb held by roots and fungal threads, a magnified macroaggregate made of microaggregates. Idea: Stina (SLU), Two levels series.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261125',
    post: 'pl20261125',
    create: {
      iso_date: '2026-11-25',
      date_tbd: false,
      topic: 'Mentor spotlight',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        '[PLACEHOLDER] Meet [Name]: where they are, what they teach, and their best advice in their own words. Thank you, [Name]!\n#SoilFoodWeb #Mentors #SoilScience',
      slides: [
        { text: 'Meet our mentors. [Name], [role].', image: null },
        { text: '[Their one line of advice, in their words.]', image: null },
      ],
      cta: '',
      link: 'Tag the mentor [VERIFY handle].',
      sources: ['https://soilfoodweb.com'],
      visual_note: "Next mentor from Stephanie's list. Their website headshot.",
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261126',
    post: 'pl20261126',
    create: {
      iso_date: '2026-11-26',
      date_tbd: false,
      topic: 'Thanksgiving: thank the soil life that grew your dinner',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Before the first bite, thank the soil life that grew your dinner. 🥧\nEvery dish on the table started with microbes: fungi and bacteria cycling nutrients for the potatoes, rhizobia in bean roots turning air into nitrogen, and mycorrhizal fungi helping pumpkin vines reach water and phosphorus. Happy Thanksgiving from all of us at the Soil Food Web School. 💚\n#Thanksgiving #SoilLife #Gratitude #SoilFoodWeb',
      slides: [
        { text: 'This Thanksgiving, thank the soil life that grew your dinner.', image: null },
        { text: 'The potatoes: fungi and bacteria cycled the nutrients.', image: null },
        { text: 'The green beans: rhizobia in the roots turned air into nitrogen.', image: null },
        {
          text: 'The pumpkin pie: mycorrhizal fungi helped the vines find water and phosphorus.',
          image: null,
        },
        { text: 'Happy Thanksgiving from all of us. 💚', image: null },
      ],
      cta: "Tag who's cooking this year",
      link: '',
      sources: [
        'https://scholar.google.com/scholar?q=Brundrett+Tedersoo+2018+Evolutionary+history+of+mycorrhizal+symbioses+and+global+host+plant+diversity',
      ],
      visual_note:
        'Carousel, 5 slides. A potato plant with tubers, a green bean plant with pink root nodules, a pumpkin on its vine with fungal threads at the roots.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261127',
    post: 'pl20261127',
    create: {
      iso_date: '2026-11-27',
      date_tbd: false,
      topic: 'Fun Soil News: November 2026',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Five pieces of good soil news from around the world this month. 🌍\n[One line per story, with the country and the source.]\n📤 Send this to a friend who needs good news.\n#FunSoilNews #SoilHealth #GoodNews #SoilFoodWeb',
      slides: [
        { text: 'Fun Soil News: November 2026.', image: null },
        { text: 'Story 1. Country in big type, one sentence, source.', image: null },
        { text: 'Story 2. Country in big type, one sentence, source.', image: null },
        { text: 'Story 3. Country in big type, one sentence, source.', image: null },
        { text: 'Story 4. Country in big type, one sentence, source.', image: null },
        { text: 'Story 5. Country in big type, one sentence, source.', image: null },
      ],
      cta: 'Send this to a friend who needs good news',
      link: '',
      sources: [],
      visual_note:
        'Same format as Fun Soil News October. Stories from the news scout, verify every item.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261130',
    post: 'pl20261130',
    create: {
      iso_date: '2026-11-30',
      date_tbd: false,
      topic: 'Read the drop: ciliates, the anaerobic warning sign',
      platform: 'Instagram Reel',
      caption:
        'When you see lots of these, your compost has run out of air. 🔬\nCiliates are protozoa covered in fine hair-like cilia, and they thrive when oxygen drops and anaerobic bacteria take over. A few are normal. A slide full of them in compost or compost tea is a warning: turn the pile, add structure or aerate the brew before it goes on your plants.\n📤 Send this to someone making compost tea.\n#Ciliates #Microscopy #Compost #SoilFoodWeb',
      slides: [
        { text: 'This is a ciliate.', image: null },
        { text: 'Hair-like cilia cover its body.', image: null },
        { text: 'Lots of them in compost or tea?', image: null },
        { text: 'Oxygen has run low. Fix it before you apply.', image: null },
      ],
      cta: 'Send this to someone making compost tea',
      link: '',
      sources: ['https://scholar.google.com/scholar?q=Ingham+Soil+Biology+Primer+USDA+NRCS'],
      visual_note: 'Reel, 15 seconds. Repo microscopy of a ciliate.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261205',
    post: 'pl20261205',
    create: {
      iso_date: '2026-12-05',
      date_tbd: false,
      topic: 'World Soil Day: a year of living soil',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Happy World Soil Day! 🌍\nThis year our graduates brought soil back to life on coffee farms in Guinea, pastures in Tennessee, olive groves in Turkey, a farm school in Brazil and community plots in Kenya. Every one of them started by learning what lives in a single drop of soil. Thank you for protecting the ground we all stand on. 💚\n#WorldSoilDay #SoilHealth #LivingSoil #SoilFoodWeb',
      slides: [
        { text: "Happy World Soil Day. Here's a year of living soil.", image: null },
        { text: 'Boubacar, Guinea. Coffee grown in a syntropic agroforest.', image: null },
        { text: 'Christina, Tennessee. From advertising to a soil business.', image: null },
        { text: 'Ibrahim, Turkey. More than 80 growers going regenerative.', image: null },
        { text: 'Arthur, Brazil. A prize-winning farm school.', image: null },
        { text: 'Joseph, Kenya. Teaching his whole community.', image: null },
        { text: 'Thank you for protecting the ground we all stand on.', image: null },
      ],
      cta: "Share how you'll celebrate World Soil Day",
      link: '',
      sources: [
        'https://www.fao.org/world-soil-day/en',
        'https://docs.google.com/spreadsheets/d/10UHLwzJLBQAsmJqmg4hiCQRjBKXPAx7UnOudU-Vsg5U/edit',
      ],
      visual_note:
        "Carousel, 7 slides. Reuse each graduate's photo from their own post. Add this year's FAO theme.",
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261206',
    post: 'pl20261206',
    create: {
      iso_date: '2026-12-06',
      date_tbd: false,
      topic: 'Field Notes #2',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        '[PLACEHOLDER] Open with the result number, then the question, method and the honest surprise.\n#FieldNotes #SoilFoodWeb #SoilScience',
      slides: [
        { text: 'Trial name, place and season.', image: null },
        { text: 'The question they tested.', image: null },
        { text: 'The method in 3 lines.', image: null },
        { text: 'The result, one big number.', image: null },
        { text: "What surprised them, including what didn't work.", image: null },
        { text: 'Who ran it.', image: null },
      ],
      cta: 'Save this trial',
      link: 'Collab with the graduate.',
      sources: [
        'https://docs.google.com/spreadsheets/d/10UHLwzJLBQAsmJqmg4hiCQRjBKXPAx7UnOudU-Vsg5U/edit',
      ],
      visual_note: 'Same layout as Field Notes #1. Graduate trial still to pick.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261207',
    post: 'pl20261207',
    create: {
      iso_date: '2026-12-07',
      date_tbd: false,
      topic: 'Myth vs mechanism: organic matter and water',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        '"1% more organic matter holds 20,000 more gallons per acre." You\'ve heard it. The data says the effect is much smaller. 💧\nA 2018 review in the European Journal of Soil Science pooled results from dozens of studies and found that raising soil organic carbon by 1% increased available water only slightly on average, more in sandy soils and less in clays. Where living soil really changes water is infiltration: stable aggregates and biopores let rain soak in instead of running off.\n📤 Send this to the consultant who quotes the 20,000 gallons.\n#SoilWater #MythVsMechanism #SoilScience #SoilFoodWeb',
      slides: [
        {
          text: 'Myth: "Add 1% organic matter and your soil holds 20,000 more gallons of water per acre."',
          image: null,
        },
        { text: 'A 2018 review of about 60 studies tested that claim.', image: null },
        {
          text: 'A 1% rise in soil organic carbon raised available water only slightly, on average about 1 mm per 10 cm of soil.',
          image: null,
        },
        { text: 'The effect was larger in sandy soils and smaller in clays.', image: null },
        {
          text: 'Where biology really helps water: aggregates and pores that let rain soak in instead of running off.',
          image: null,
        },
        { text: 'Honest numbers build trust. Source on the slide.', image: null },
      ],
      cta: 'Send this to the consultant who quotes the 20,000 gallons',
      link: '',
      sources: [
        'https://scholar.google.com/scholar?q=Minasny+McBratney+2018+Limited+effect+of+organic+matter+on+soil+available+water+capacity',
      ],
      visual_note: 'Carousel, 6 slides. Claimed vs measured bar. Wes to confirm the numbers.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261209',
    post: 'pl20261209',
    create: {
      iso_date: '2026-12-09',
      date_tbd: false,
      topic: 'Free webinar this month',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        '[PLACEHOLDER] One line on what people will learn, who\'s teaching, the date and time, and "Free. Link in bio."\n#SoilFoodWeb #FreeWebinar #SoilEducation',
      slides: [
        { text: 'FREE WEBINAR', image: null },
        { text: '[Webinar title]', image: null },
        { text: '[Date and time, three time zones]', image: null },
        { text: '[Host name]', image: null },
        { text: 'Free. Link in bio.', image: null },
      ],
      cta: 'Sign up, link in bio',
      link: '[PLACEHOLDER] Webinar signup link',
      sources: [],
      visual_note: 'Single image. Host headshot or a microscope.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261211',
    post: 'pl20261211',
    create: {
      iso_date: '2026-12-11',
      date_tbd: false,
      topic: 'International Mountain Day: mountain soils',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'On a mountain, soil is precious. 🏔️\nCold temperatures and steep slopes slow soil formation, so mountain soils are often thin and young. Strip away the roots and plant cover, and a single heavy storm can wash away soil that took centuries to build. Terraces, permanent cover and living roots are what hold mountain farms together.\n📤 Send this to your hiking friend.\n#InternationalMountainDay #SoilErosion #SoilHealth #SoilFoodWeb',
      slides: [
        { text: 'Mountain soils are thin, young and fragile.', image: null },
        { text: 'Cold and steep slopes slow soil formation.', image: null },
        {
          text: 'Without roots and cover, one heavy storm can wash away centuries of soil.',
          image: null,
        },
        { text: 'Terraces, cover and living roots hold mountain farms together.', image: null },
      ],
      cta: 'Send this to your hiking friend',
      link: '',
      sources: [
        'https://www.fao.org/international-mountain-day/en',
        "https://scholar.google.com/scholar?q=FAO+ITPS+2015+Status+of+the+World's+Soil+Resources",
      ],
      visual_note:
        'Carousel, 4 slides. Mountain cross-section with a thin soil layer and roots. Real photo of farming terraces.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261212',
    post: 'pl20261212',
    create: {
      iso_date: '2026-12-12',
      date_tbd: false,
      topic: 'Do this weekend: winter care for your worm bin',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Your worms feel the cold too. 🥶🪱\nRed wigglers slow down below about 10°C and die if their bin freezes. Move the bin somewhere sheltered, add extra shredded cardboard as insulation, feed a little less, and keep the bedding damp like a wrung-out sponge. They'll be ready to work hard again in spring.\n💾 Save this before the first frost.\n#WormBin #Vermicompost #WinterGarden #SoilFoodWeb",
      slides: [
        { text: 'Your worms get cold too.', image: null },
        {
          text: 'Red wigglers slow down below about 10°C and die if the bin freezes.',
          image: null,
        },
        { text: 'Move the bin to a shed, garage or basement.', image: null },
        { text: 'Add extra shredded cardboard as insulation, and feed less.', image: null },
        { text: 'Keep the bedding damp, like a wrung-out sponge.', image: null },
      ],
      cta: 'Save this before the first frost',
      link: '',
      sources: [
        'https://scholar.google.com/scholar?q=Cornell+Waste+Management+Institute+composting+with+worms+red+wigglers+temperature',
      ],
      visual_note:
        'Carousel, 5 slides. A red wiggler in a tiny scarf, a worm bin in a shed, a hand squeezing a damp sponge. Wes to verify the 10°C figure.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261214',
    post: 'pl20261214',
    create: {
      iso_date: '2026-12-14',
      date_tbd: false,
      topic: "Soil in numbers: a third of the world's soils are degraded",
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "One third of the world's soils are degraded. 🌍\nThe FAO's global soil assessment found about 33% of soils moderately to highly degraded, through erosion, carbon loss, salinization, compaction, acidification and pollution. New soil forms slowly, so protecting and restoring the soil we have is the work that matters.\n📤 Send this to someone who works in food.\n#SoilInNumbers #SoilDegradation #SoilHealth #SoilFoodWeb",
      slides: [
        { text: "33% of the world's soils are moderately to highly degraded.", image: null },
        {
          text: 'The causes: erosion, loss of organic carbon, salinization, compaction, acidification and pollution.',
          image: null,
        },
        { text: 'Forming a few centimeters of new soil can take centuries.', image: null },
        { text: 'Restoring soil biology is one of the fastest ways to rebuild it.', image: null },
      ],
      cta: 'Send this to someone who works in food',
      link: '',
      sources: [
        "https://scholar.google.com/scholar?q=FAO+ITPS+2015+Status+of+the+World's+Soil+Resources",
      ],
      visual_note:
        'Carousel, 4 slides, same format as the nematode Soil in numbers post. Pie chart with one third shaded.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261218',
    post: 'pl20261218',
    create: {
      iso_date: '2026-12-18',
      date_tbd: false,
      topic: 'Fun Soil News: December 2026',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Five pieces of good soil news to end the year. 🌍\n[One line per story, with the country and the source.]\n📤 Send this to a friend who needs good news.\n#FunSoilNews #SoilHealth #GoodNews #SoilFoodWeb',
      slides: [
        { text: 'Fun Soil News: December 2026.', image: null },
        { text: 'Story 1. Country in big type, one sentence, source.', image: null },
        { text: 'Story 2. Country in big type, one sentence, source.', image: null },
        { text: 'Story 3. Country in big type, one sentence, source.', image: null },
        { text: 'Story 4. Country in big type, one sentence, source.', image: null },
        { text: 'Story 5. Country in big type, one sentence, source.', image: null },
      ],
      cta: 'Send this to a friend who needs good news',
      link: '',
      sources: [],
      visual_note: 'Same format as Fun Soil News October. Verify every item.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261219',
    post: 'pl20261219',
    create: {
      iso_date: '2026-12-19',
      date_tbd: false,
      topic: 'Do this weekend: the jar test',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "All you need to know your soil texture is a jar. 🫙\nFill a jar a third of the way with soil, add water and a pinch of dish soap, and shake hard. Sand drops out in about a minute, silt over a few hours, and clay can take a day or more. Mark each layer and you'll know what you're working with, and how your soil biology can help it.\n💾 Save this for a rainy afternoon.\n#SoilTexture #JarTest #GardenScience #SoilFoodWeb",
      slides: [
        { text: 'What is your soil made of? Find out with a jar.', image: null },
        {
          text: 'Fill a jar one third with soil, top up with water and a pinch of dish soap. Shake hard.',
          image: null,
        },
        { text: 'Sand settles in about a minute. Mark the line.', image: null },
        {
          text: 'Silt settles over a few hours. Mark it. Clay can take a day or more.',
          image: null,
        },
        { text: 'Compare the layers to find your texture.', image: null },
      ],
      cta: 'Save this for a rainy afternoon',
      link: '',
      sources: ['https://scholar.google.com/scholar?q=USDA+NRCS+soil+texture+jar+test'],
      visual_note:
        'Carousel, 5 slides. A glass jar with sand, silt and clay layers and water on top, with labelled arrows. Fits the watercolor jar style.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261221',
    post: 'pl20261221',
    create: {
      iso_date: '2026-12-21',
      date_tbd: false,
      topic: 'Read the drop: fungal hyphae or debris?',
      platform: 'Instagram Reel',
      caption:
        'Is it a fungal hypha or just a scrap of plant debris? 🔬\nReal hyphae keep the same width along their whole length, with parallel walls, and they often branch. Debris has irregular edges and changes width. And if the thread is much thinner, you may be looking at actinomycetes, filamentous bacteria. Getting this right is the difference between a fungal and a bacterial compost reading.\n💾 Save this for your next slide.\n#FungalHyphae #Microscopy #Compost #SoilFoodWeb',
      slides: [
        { text: 'Fungal hypha: same width along its whole length.', image: null },
        { text: 'Parallel walls, often branching.', image: null },
        { text: 'Debris: irregular edges, changing width.', image: null },
        { text: 'Actinomycetes: much thinner threads.', image: null },
      ],
      cta: 'Save this for your next slide',
      link: '',
      sources: ['https://scholar.google.com/scholar?q=Ingham+Soil+Biology+Primer+USDA+NRCS'],
      visual_note: 'Reel, 15 to 20 seconds. Repo microscopy of hyphae and debris side by side.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261223',
    post: 'pl20261223',
    create: {
      iso_date: '2026-12-23',
      date_tbd: false,
      topic: 'Partner share',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        '[PLACEHOLDER] One line on who the partner is and why we love their work.\n#SoilFoodWeb #Partners',
      slides: [
        { text: 'FROM OUR PARTNERS', image: null },
        { text: '[Partner name]', image: null },
        { text: '[One line on their work]', image: null },
      ],
      cta: 'Follow our partner',
      link: 'Tag the partner.',
      sources: [],
      visual_note: "Single image. The partner's own post. Partner to pick with Stephanie.",
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261225',
    post: 'pl20261225',
    create: {
      iso_date: '2026-12-25',
      date_tbd: false,
      topic: 'Holiday card: tardigrades in Santa hats',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Happy holidays from all of us, and from the tardigrades. 🎄\nThank you for a year of looking closer at the life in our soils. See you in 2027. 💚\n#HappyHolidays #Tardigrades #SoilFoodWeb',
      slides: [
        { text: 'Happy holidays', image: null },
        { text: 'from all of us at the Soil Food Web School.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'Single image. Two chubby tardigrades in little red Santa hats with green leaves around them, on cream.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261228',
    post: 'pl20261228',
    create: {
      iso_date: '2026-12-28',
      date_tbd: false,
      topic: "Myth vs mechanism: humus isn't what you learned",
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "The humus you learned about in school may not exist the way it was taught. 🧪\nFor a century, soil science described humic substances as large, unique molecules. A 2015 Nature paper argued that much of that picture came from the harsh chemical extraction used to study them. The current view is a continuum: organic matter keeps being broken down by microbes, and carbon lasts when it's protected inside aggregates or bound to minerals.\n📤 Send this to the soil scientist in your life.\n#SoilOrganicMatter #SoilScience #MythVsMechanism #SoilFoodWeb",
      slides: [
        { text: 'Myth: "Humus is a special, stable substance in soil."', image: null },
        {
          text: 'For a century, textbooks described humic substances as large, unique molecules.',
          image: null,
        },
        {
          text: 'Modern imaging found little of that in intact soil. Much of it came from the harsh extraction method.',
          image: null,
        },
        {
          text: 'The current view: organic matter is a continuum of compounds being broken down by microbes.',
          image: null,
        },
        {
          text: "Carbon stays in soil mainly when it's protected in aggregates or bound to minerals.",
          image: null,
        },
        { text: 'Microbes are part of the answer. Source on the slide.', image: null },
      ],
      cta: 'Send this to the soil scientist in your life',
      link: '',
      sources: [
        'https://scholar.google.com/scholar?q=Lehmann+Kleber+2015+The+contentious+nature+of+soil+organic+matter',
      ],
      visual_note:
        'Carousel, 6 slides. A leaf breaking down into smaller and smaller fragments, a soil crumb, fungal hyphae.',
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 plan pl20261230',
    post: 'pl20261230',
    create: {
      iso_date: '2026-12-30',
      date_tbd: false,
      topic: 'Soil Regenerators in the wild: tree crop farmer, Sumatra',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'They farmed the way their parents did. Then they looked under a microscope. 🌳\nIn the Simalungun Regency of Sumatra, Indonesia, [Name] started out farming organically. At the Soil Food Web School, they learned to make regenerative compost and check it under a microscope, then mapped their fields and planted companion plants and ground cover to feed the soil life their trees depend on. Today they teach other tree crop farmers across Sumatra. 💚\n🤝 Tag a farmer who should hear this.\n#SoilRegeneratorsInTheWild #Indonesia #Agroforestry #SoilFoodWeb',
      slides: [
        {
          text: 'Soil Regenerators in the wild. [Name], Simalungun Regency, Sumatra, Indonesia',
          image: null,
        },
        {
          text: 'Farming the way their parents did. Then they looked under a microscope.',
          image: null,
        },
        { text: 'Regenerative compost, checked under the microscope.', image: null },
        { text: 'Fields mapped, companion plants and ground cover planted.', image: null },
        {
          text: '"It has enriched the people, plants and animals in the Simalungun regency where I call home."',
          image: null,
        },
      ],
      cta: 'Tag a farmer who should hear this',
      link: 'Collab with the farmer [VERIFY name and handle].',
      sources: [
        'https://docs.google.com/spreadsheets/d/10UHLwzJLBQAsmJqmg4hiCQRjBKXPAx7UnOudU-Vsg5U/edit',
      ],
      visual_note: "Carousel, 5 slides. The farmer's own photos. Name and handle still to verify.",
      note: 'From the November/December plan doc (30 Sep). Visual still to make.',
      status: 'draft',
    },
    reason:
      'Added from the November/December plan doc (Linnea, 23 Oct). Caption and slide text drafted; visual still to make.',
  },
  {
    key: '2026-10-23 costa rica cr20261102',
    post: 'cr20261102',
    create: {
      iso_date: '2026-11-02',
      date_tbd: false,
      topic: 'Collaboration post with Armonía: we are going back',
      platform: 'Instagram collab, Facebook',
      caption:
        'We are going back to Armonía! 🌿\nFor the fourth time, Armonía Agricultura Orgánica near San José will host our Accelerator Workshop. Armonía is a campus built around health and learning, with primary and secondary schools and an organic farm that feeds visitors at its own restaurant. Our students build their compost piles where children grow up knowing where food comes from.\nThank you, Armonía, for having us again. 💚\nAccelerator Workshop, 18 to 29 January 2027. Register now, link in bio.\n#SoilFoodWeb #CostaRica #Compost #Workshop #LivingSoil',
      slides: [
        {
          text: 'We are going back to Armonía.',
          image: '/wormhole/tiles/cr20261102-v1-1.jpg',
        },
        {
          text: 'Our fifth Costa Rica workshop, and our fourth at Armonía Agricultura Orgánica.',
          image: '/wormhole/tiles/cr20261102-v1-2.jpg',
        },
        {
          text: 'An organic farm on a school campus, with primary and secondary schools and its own restaurant.',
          image: '/wormhole/tiles/cr20261102-v1-3.jpg',
        },
        {
          text: 'You learn compost where children grow up knowing where food comes from.',
          image: '/wormhole/tiles/cr20261102-v1-4.jpg',
        },
        {
          text: 'Accelerator Workshop, 18 to 29 January 2027.',
          image: '/wormhole/tiles/cr20261102-v1-5.jpg',
        },
      ],
      cta: 'Register, link in bio',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'October 2025 newsletter: https://soilfoodweb.com/october-2025-newsletter/',
        'Workshop Handbook, March 2025: https://soilfoodweb.com/wp-content/uploads/2024/11/WORKSHOP-HANDBOOK-MARCH-2025.pdf',
        'SFW workshops page: https://new.soilfoodweb.com/workshops/',
        'Idea: Allison',
      ],
      visual_note:
        'Carousel, real photos from past Costa Rica workshops. Deck: /wormhole/decks/02-11-2026-armonia-collab.pptx. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica cr20261103',
    post: 'cr20261103',
    create: {
      iso_date: '2026-11-03',
      date_tbd: false,
      topic: 'Costa Rica Accelerator Workshop: early bird ends tomorrow',
      platform: 'Instagram, Facebook',
      caption:
        'The early bird for our Costa Rica workshop ends tomorrow. 🌿\nFor ten days at Armonía Agricultura Orgánica near San José, you build compost piles with your team, make extracts and teas, and check everything under the microscope with mentors beside you. What takes 18 to 24 months alone, you do here in two weeks.\n18 to 29 January 2027. The early bird discount ends 4 November.\nRegister now, link in bio.\n#SoilFoodWeb #CostaRica #Compost #Workshop #LivingSoil',
      slides: [
        {
          text: 'The early bird ends tomorrow.',
          image: '/wormhole/tiles/cr20261103-v1-1.jpg',
        },
        {
          text: 'Accelerator Workshop, Costa Rica, 18 to 29 January 2027.',
          image: '/wormhole/tiles/cr20261103-v1-2.jpg',
        },
        {
          text: 'A year of hands-on experience in 10 days.',
          image: '/wormhole/tiles/cr20261103-v1-3.jpg',
        },
        {
          text: 'Week one compost, week two liquid amendments, the microscope every day.',
          image: '/wormhole/tiles/cr20261103-v1-4.jpg',
        },
      ],
      cta: 'Register, link in bio',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Carousel, real photos from past Costa Rica workshops. Deck: /wormhole/decks/03-11-2026-costa-rica-early-bird.pptx. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica cr20261112',
    post: 'cr20261112',
    create: {
      iso_date: '2026-11-12',
      date_tbd: false,
      topic: 'Costa Rica: a day at the workshop',
      platform: 'Instagram, Facebook',
      caption:
        "Morning: build the pile. Midday: lunch together. Afternoon: the microscope. ☀️\nThat's a day at our Costa Rica workshop. Next one: 18 to 29 January 2027. Register now, link in bio.\n#SoilFoodWeb #CostaRica #Workshop",
      slides: [
        {
          text: 'A day at the Costa Rica workshop.',
          image: '/wormhole/tiles/cr20261112-v1-1.jpg',
        },
        {
          text: 'Morning: build the pile.',
          image: '/wormhole/tiles/cr20261112-v1-2.jpg',
        },
        {
          text: 'Midday: lunch together.',
          image: '/wormhole/tiles/cr20261112-v1-3.jpg',
        },
        {
          text: 'Afternoon: the microscope.',
          image: '/wormhole/tiles/cr20261112-v1-4.jpg',
        },
        {
          text: '18 to 29 January 2027.',
          image: '/wormhole/tiles/cr20261112-v1-5.jpg',
        },
      ],
      cta: 'Register, link in bio',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Carousel, real photos from past Costa Rica workshops. Deck: /wormhole/decks/12-11-2026-costa-rica-a-day.pptx. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica cr20261116',
    post: 'cr20261116',
    create: {
      iso_date: '2026-11-16',
      date_tbd: false,
      topic: 'Costa Rica: some piles are built to fail',
      platform: 'Instagram, Facebook',
      caption:
        'At our Costa Rica workshop, some compost piles are built to fail. On purpose. 🔥\nStudents build several piles at the same time. Some are designed to succeed and some are designed to go wrong, so you learn to read a failing pile and rescue it, with a mentor beside you. As Loida Vasquez says, the most is learned from failed piles.\nAccelerator Workshop, 18 to 29 January 2027. Register now, link in bio.\n#SoilFoodWeb #CostaRica #Compost #Workshop',
      slides: [
        {
          text: 'Some piles are built to fail.',
          image: '/wormhole/tiles/cr20261116-v1-1.jpg',
        },
        {
          text: 'On purpose.',
          image: '/wormhole/tiles/cr20261116-v1-2.jpg',
        },
        {
          text: 'Students build several piles at once, some designed to go wrong.',
          image: '/wormhole/tiles/cr20261116-v1-3.jpg',
        },
        {
          text: 'Then they diagnose them and turn them around.',
          image: '/wormhole/tiles/cr20261116-v1-4.jpg',
        },
        {
          text: '"The most is learned from failed piles." Loida Vasquez',
          image: '/wormhole/tiles/cr20261116-v1-5.jpg',
        },
        {
          text: 'Costa Rica, 18 to 29 January 2027.',
          image: '/wormhole/tiles/cr20261116-v1-6.jpg',
        },
      ],
      cta: 'Register, link in bio',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Workshop Handbook, March 2025: https://soilfoodweb.com/wp-content/uploads/2024/11/WORKSHOP-HANDBOOK-MARCH-2025.pdf',
        'Workshop Handbook, June 2025: https://www.soilfoodweb.com/wp-content/uploads/2025/02/WORKSHOP-HANDBOOK-JUNE-2025.pdf',
        "Loida's line: SFW context pack (CLAUDE.md) [CONFIRM wording with Loida]",
      ],
      visual_note:
        'Carousel, real photos from past Costa Rica workshops. Deck: /wormhole/decks/16-11-2026-costa-rica-built-to-fail.pptx. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica cr20261123',
    post: 'cr20261123',
    create: {
      iso_date: '2026-11-23',
      date_tbd: false,
      topic: 'Costa Rica: why we teach here',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'The country that regrew its forests is a good place to learn to regrow soil. 🌳\nCosta Rica\'s forest cover fell to 21 to 25% in the 1980s and climbed back to 53% by 2016. Its farms are under heavy chemical pressure, with some of the highest fertilizer and pesticide use per hectare in the world. Our Costa Rica students learn to make living compost and liquid amendments from local materials, and to check them under a microscope.\nAccelerator Workshop, 18 to 29 January 2027. Register now, link in bio.\n#SoilFoodWeb #CostaRica #LivingSoil #Workshop\nLinkedIn version: end with "What would it take for farms in your region to rely less on bought-in inputs?"',
      slides: [
        {
          text: 'Costa Rica brought its forests back.',
          image: '/wormhole/tiles/cr20261123-v1-1.jpg',
        },
        {
          text: 'Forest cover went from 21 to 25% in the 1980s to 53% by 2016.',
          image: '/wormhole/tiles/cr20261123-v1-2.jpg',
        },
        {
          text: 'Its farms carry some of the heaviest chemical loads in the world.',
          image: '/wormhole/tiles/cr20261123-v1-3.jpg',
        },
        {
          text: 'Our students learn to build living soil from local materials, and take it home.',
          image: '/wormhole/tiles/cr20261123-v1-4.jpg',
        },
        {
          text: 'Costa Rica, 18 to 29 January 2027.',
          image: '/wormhole/tiles/cr20261123-v1-5.jpg',
        },
      ],
      cta: 'Register, link in bio',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Inter Press Service, 2016: https://www.ipsnews.net/?p=146239',
        'Semanario Universidad, 2023 (FAO pesticide data): https://semanariouniversidad.com/pais/costa-rica-es-el-pais-que-utiliza-mas-plaguicidas-en-todo-el-mundo-segun-estadisticas-de-la-fao/',
        'World Bank, fertilizer use: https://data.worldbank.org/indicator/AG.CON.FERT.ZS?locations=CR',
      ],
      visual_note:
        'Carousel, real photos from past Costa Rica workshops. Deck: /wormhole/decks/23-11-2026-costa-rica-why-here.pptx. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261026',
    post: 'st20261026',
    create: {
      iso_date: '2026-10-26',
      date_tbd: false,
      topic: 'Costa Rica stories · Announcement',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Link sticker on frame 1. Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 1 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261026-v1-1.jpg',
        },
        {
          text: 'Story frame 2 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261026-v1-2.jpg',
        },
        {
          text: 'Story frame 3 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261026-v1-3.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 1, 2, 3 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261029',
    post: 'st20261029',
    create: {
      iso_date: '2026-10-29',
      date_tbd: false,
      topic: 'Costa Rica stories · The two weeks',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Poll sticker on frame 5: "Would you rescue a failing pile?" Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 4 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261029-v1-1.jpg',
        },
        {
          text: 'Story frame 5 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261029-v1-2.jpg',
        },
        {
          text: 'Story frame 7 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261029-v1-3.jpg',
        },
        {
          text: 'Story frame 8 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261029-v1-4.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 4, 5, 7, 8 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261102',
    post: 'st20261102',
    create: {
      iso_date: '2026-11-02',
      date_tbd: false,
      topic: "Costa Rica stories · What's included and who can join",
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Also reshare the Armonía collab post. Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 10 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261102-v1-1.jpg',
        },
        {
          text: 'Story frame 11 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261102-v1-2.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 10, 11 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261103',
    post: 'st20261103',
    create: {
      iso_date: '2026-11-03',
      date_tbd: false,
      topic: 'Costa Rica stories · Early bird ends tomorrow',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Countdown sticker to 4 November. Also reshare the feed post. Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 12 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261103-v1-1.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 12 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261104',
    post: 'st20261104',
    create: {
      iso_date: '2026-11-04',
      date_tbd: false,
      topic: 'Costa Rica stories · Early bird ends today',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Same frame, text sticker "Ends today". Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 12 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261104-v1-1.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 12 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261112',
    post: 'st20261112',
    create: {
      iso_date: '2026-11-12',
      date_tbd: false,
      topic: 'Costa Rica stories · The weekend and a student voice',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Also reshare the "day at the workshop" post. Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 6 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261112-v1-1.jpg',
        },
        {
          text: 'Story frame 9 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261112-v1-2.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 6, 9 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261116',
    post: 'st20261116',
    create: {
      iso_date: '2026-11-16',
      date_tbd: false,
      topic: 'Costa Rica stories · Built to fail',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Also reshare the feed post. Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 5 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261116-v1-1.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 5 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261123',
    post: 'st20261123',
    create: {
      iso_date: '2026-11-23',
      date_tbd: false,
      topic: 'Costa Rica stories · Where we learn',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Also reshare the "why we teach here" post. Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 3 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261123-v1-1.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 3 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20261201',
    post: 'st20261201',
    create: {
      iso_date: '2026-12-01',
      date_tbd: false,
      topic: 'Costa Rica stories · Registration still open',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Before refunds stop on 7 December. Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 10 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261201-v1-1.jpg',
        },
        {
          text: 'Story frame 11 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261201-v1-2.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 10, 11 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 costa rica st20270111',
    post: 'st20270111',
    create: {
      iso_date: '2027-01-11',
      date_tbd: false,
      topic: 'Costa Rica stories · Countdown week',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Countdown sticker to 18 January. Link sticker: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      slides: [
        {
          text: 'Story frame 13 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20270111-v1-1.jpg',
        },
      ],
      cta: 'Register, link sticker',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'Costa Rica 2027 sales page: https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'Frames 13 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027.pptx. Post around 8:00am Pacific. No prices.',
      note: 'Costa Rica 2027 promo, from the November planning doc (Linnea, 23 Oct). Visual made in Claude, editable deck in /wormhole/decks.',
      status: 'draft',
    },
    reason: 'Added the Costa Rica 2027 feed post or story with its visuals (Linnea, 23 Oct).',
  },
  {
    key: '2026-10-23 p18 slides v2',
    post: 'p18',
    set: {
      slides: [{ text: 'Vampire amoeba.', image: '/wormhole/tiles/p18-v2-1.jpg' }],
    },
    reason:
      'New cover (23 Oct): clouds drifting across the moon, headline moved up so it no longer covers the amoeba. The amoeba is a naked amoeba from our microscopy, not a vampyrellid: swap in a real vampyrellid image before posting.',
  },
  {
    key: '2026-10-23 p18 slides v3',
    post: 'p18',
    set: {
      slides: [{ text: 'Vampire amoeba.', image: '/wormhole/tiles/p18-v3-1.jpg' }],
    },
    reason:
      'New cover (23 Oct): real vampire amoeba photos. The moon is Vampyrella lateritia with its radiating threads; the lens shows one draining an algal cell. Source: Hess, Sausen & Melkonian (2012), Shedding light on vampires, PLoS ONE 7: e31165, Fig. 2 A and H, CC BY 4.0, credited on the slide.',
  },
  {
    key: '2026-10-23 p15 hold',
    post: 'p15',
    set: { date_tbd: true },
    reason: "Hold (Linnea, 23 Oct): we haven't emailed Jason Gearheart yet. Was Wed 28 Oct.",
  },
  {
    key: '2026-10-23 p14 slides v1',
    post: 'p14',
    set: {
      slides: [
        { text: "We're going back to Costa Rica.", image: '/wormhole/tiles/p14-v1-1.jpg' },
        {
          text: 'Ten days of compost piles, extracts and the microscope.',
          image: '/wormhole/tiles/p14-v1-2.jpg',
        },
        {
          text: 'Where we learn: Armonía Agricultura Orgánica, 11 km north of San José.',
          image: '/wormhole/tiles/p14-v1-3.jpg',
        },
        {
          text: 'The early bird ends 4 November. 18 to 29 January 2027. Register, link in bio.',
          image: '/wormhole/tiles/p14-v1-4.jpg',
        },
      ],
    },
    caption: [
      [
        'Ready to take what you learned online into your hands? 🌿',
        "We're going back to Costa Rica! 🌺",
      ],
      [
        'runs January 18 to 25, 2027. Join the interest list at the link in bio.',
        'runs January 18 to 29, 2027. The early bird ends November 4. Register now, link in bio.',
      ],
    ],
    reason:
      'New slides (Linnea, 23 Oct) in the Costa Rica look: real workshop photos, flat colour, flower cutouts. Deck: /wormhole/decks/26-10-2026-costa-rica-going-back.pptx. Dates fixed to 18 to 29 January, CTA is Register.',
  },
  {
    key: '2026-10-23 p16 slides v1',
    post: 'p16',
    set: {
      slides: [
        { text: 'Every event in one place.', image: '/wormhole/tiles/p16-v1-1.jpg' },
        {
          text: "What you'll find: free webinars, in-person workshops, course start dates.",
          image: '/wormhole/tiles/p16-v1-2.jpg',
        },
        {
          text: 'soilfoodweb.com/events [VERIFY URL]. Link in bio.',
          image: '/wormhole/tiles/p16-v1-3.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct) in the Costa Rica look: real workshop photos, flat colour, flower cutouts. Deck: /wormhole/decks/29-10-2026-every-event.pptx.',
  },
  {
    key: '2026-10-23 p17 slides v1',
    post: 'p17',
    set: {
      slides: [
        { text: 'Fun Soil News, October 2026.', image: '/wormhole/tiles/p17-v1-1.jpg' },
        {
          text: 'Australia: six years after replanting, the fungi in restored farmland were still recovering. Flinders University News, 20 Oct 2026 [VERIFY]',
          image: '/wormhole/tiles/p17-v1-2.jpg',
        },
        {
          text: 'Forests: climate warming can slow how tree roots feed soil microbes. Phys.org, Oct 2026 [VERIFY]',
          image: '/wormhole/tiles/p17-v1-3.jpg',
        },
        {
          text: 'Biochar: "bomb carbon" in wood shavings measures how long biochar stays in soil. Phys.org, Oct 2026 [VERIFY]',
          image: '/wormhole/tiles/p17-v1-4.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct) in the Costa Rica look: real workshop photos, flat colour, flower cutouts. Deck: /wormhole/decks/30-10-2026-fun-soil-news-october.pptx.',
  },
  {
    key: '2026-10-23 p19 slides v1',
    post: 'p19',
    set: {
      slides: [
        {
          text: 'Last call for the early bird: Foundation Courses and the Compost Intensive.',
          image: '/wormhole/tiles/p19-v1-1.jpg',
        },
        {
          text: 'Foundation Courses: online, at your own pace.',
          image: '/wormhole/tiles/p19-v1-2.jpg',
        },
        {
          text: 'Compost Intensive: open to anyone, starts 18 January. Early bird for both ends 1 November.',
          image: '/wormhole/tiles/p19-v1-3.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct) in the Costa Rica look: real workshop photos, flat colour, flower cutouts. Deck: /wormhole/decks/01-11-2026-early-bird-last-call.pptx.',
  },
  {
    key: '2026-10-23 p18 slides v4',
    post: 'p18',
    set: {
      slides: [{ text: 'Vampire amoeba.', image: '/wormhole/tiles/p18-v4-1.jpg' }],
    },
    reason:
      'New cover (23 Oct): a plain drawn moon with clouds; the vampire amoebae are below it in two lenses: Vampyrella lateritia with its radiating threads, and one draining an algal cell. Source: Hess, Sausen & Melkonian (2012), Shedding light on vampires, PLoS ONE 7: e31165, Fig. 2 A and H, CC BY 4.0, credited on the slide.',
  },
  {
    key: '2026-10-23 sh-w1-01',
    post: 'sh-w1-01',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Can Soil Heal Itself After a Fire?',
      platform: 'Instagram Reels, YouTube Shorts',
      caption: '',
      slides: [
        { text: 'Can Soil Heal Itself After a Fire?', image: '/wormhole/tiles/sh-w1-01-v1-1.jpg' },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'Reel and Short cover, 1080 x 1920, from branch covers/shorts-webinar-1 (covers/shorts/webinar-1/01-can-soil-heal-itself-after-a-fire.png). Clip: Ivan, Webinar 1 "Wildfire Recovery & Bioremediation with Soil Biology".',
      note: 'Short 1 of 4 from Webinar 1. Caption and date still to write.',
      status: 'draft',
    },
    reason: 'Added 23 Oct: Webinar 1 Short 1 of 4, cover only, no date yet.',
  },
  {
    key: '2026-10-23 sh-w1-02',
    post: 'sh-w1-02',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Why Weeds Are Good After a Fire?',
      platform: 'Instagram Reels, YouTube Shorts',
      caption: '',
      slides: [
        { text: 'Why Weeds Are Good After a Fire?', image: '/wormhole/tiles/sh-w1-02-v1-1.jpg' },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'Reel and Short cover, 1080 x 1920, from branch covers/shorts-webinar-1 (covers/shorts/webinar-1/02-why-weeds-are-good-after-a-fire.png). Clip: Ivan, Webinar 1 "Wildfire Recovery & Bioremediation with Soil Biology".',
      note: 'Short 2 of 4 from Webinar 1. Caption and date still to write.',
      status: 'draft',
    },
    reason: 'Added 23 Oct: Webinar 1 Short 2 of 4, cover only, no date yet.',
  },
  {
    key: '2026-10-23 sh-w1-03',
    post: 'sh-w1-03',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'How Our Garden Survived a Wildfire',
      platform: 'Instagram Reels, YouTube Shorts',
      caption: '',
      slides: [
        { text: 'How Our Garden Survived a Wildfire', image: '/wormhole/tiles/sh-w1-03-v1-1.jpg' },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'Reel and Short cover, 1080 x 1920, from branch covers/shorts-webinar-1 (covers/shorts/webinar-1/03-how-our-garden-survived-a-wildfire.png). Clip: Ivan, Webinar 1 "Wildfire Recovery & Bioremediation with Soil Biology".',
      note: 'Short 3 of 4 from Webinar 1. Caption and date still to write.',
      status: 'draft',
    },
    reason: 'Added 23 Oct: Webinar 1 Short 3 of 4, cover only, no date yet.',
  },
  {
    key: '2026-10-23 sh-w1-04',
    post: 'sh-w1-04',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Where Do Heavy Metals Go?',
      platform: 'Instagram Reels, YouTube Shorts',
      caption: '',
      slides: [{ text: 'Where Do Heavy Metals Go?', image: '/wormhole/tiles/sh-w1-04-v1-1.jpg' }],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'Reel and Short cover, 1080 x 1920, from branch covers/shorts-webinar-1 (covers/shorts/webinar-1/04-where-do-heavy-metals-go.png). Clip: Ivan, Webinar 1 "Wildfire Recovery & Bioremediation with Soil Biology".',
      note: 'Short 4 of 4 from Webinar 1. Caption and date still to write.',
      status: 'draft',
    },
    reason: 'Added 23 Oct: Webinar 1 Short 4 of 4, cover only, no date yet.',
  },
  {
    key: '2026-10-23 pl20261116 slides v1',
    post: 'pl20261116',
    set: {
      slides: [
        {
          text: 'Myth: "Mother trees feed their seedlings through a fungal internet."',
          image: '/wormhole/tiles/pl20261116-v1-1.jpg',
        },
        {
          text: 'Mycorrhizal fungi do connect the roots of different trees. That part is real.',
          image: '/wormhole/tiles/pl20261116-v1-2.jpg',
        },
        {
          text: 'But field evidence that trees send meaningful resources to each other through them is thin.',
          image: '/wormhole/tiles/pl20261116-v1-3.jpg',
        },
        {
          text: 'A 2023 review found positive citation bias: papers cited the dramatic claims more than the data supported.',
          image: '/wormhole/tiles/pl20261116-v1-4.jpg',
        },
        {
          text: 'What is solid: mycorrhizal fungi trade nutrients and water for plant sugars, one plant at a time.',
          image: '/wormhole/tiles/pl20261116-v1-5.jpg',
        },
        {
          text: 'Real science is exciting enough. Source on the slide.',
          image: '/wormhole/tiles/pl20261116-v1-6.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/16-11-2026-myth-wood-wide-web-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261123 slides v1',
    post: 'pl20261123',
    set: {
      slides: [
        {
          text: 'Soil aggregates, explained twice. Level 1 for new gardeners, level 2 for consultants.',
          image: '/wormhole/tiles/pl20261123-v1-1.jpg',
        },
        {
          text: 'Level 1: Healthy soil clumps into crumbs. Those crumbs are aggregates.',
          image: '/wormhole/tiles/pl20261123-v1-2.jpg',
        },
        {
          text: 'Level 1: Roots, fungi and bacteria glue them together.',
          image: '/wormhole/tiles/pl20261123-v1-3.jpg',
        },
        {
          text: 'Level 1: Crumbs leave spaces for air, water and roots.',
          image: '/wormhole/tiles/pl20261123-v1-4.jpg',
        },
        {
          text: 'Level 2: Microaggregates are bound by persistent organic compounds and bacterial glues.',
          image: '/wormhole/tiles/pl20261123-v1-5.jpg',
        },
        {
          text: 'Level 2: Macroaggregates are held by roots and fungal hyphae, so they break down when tillage cuts those networks.',
          image: '/wormhole/tiles/pl20261123-v1-6.jpg',
        },
        { text: 'Source: Tisdall and Oades, 1982.', image: '/wormhole/tiles/pl20261123-v1-7.jpg' },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/23-11-2026-two-levels-soil-aggregates-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261130 slides v1',
    post: 'pl20261130',
    set: {
      slides: [
        { text: 'This is a ciliate.', image: '/wormhole/tiles/pl20261130-v1-1.jpg' },
        { text: 'Hair-like cilia cover its body.', image: '/wormhole/tiles/pl20261130-v1-2.jpg' },
        { text: 'Lots of them in compost or tea?', image: '/wormhole/tiles/pl20261130-v1-3.jpg' },
        {
          text: 'Oxygen has run low. Fix it before you apply.',
          image: '/wormhole/tiles/pl20261130-v1-4.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/30-11-2026-read-the-drop-ciliates-v1.pptx. Micrograph: Patricia J Coppola. Tea brewer photo: SFW library.',
  },
  {
    key: '2026-10-23 pl20261205 slides v1',
    post: 'pl20261205',
    set: {
      slides: [
        {
          text: "Happy World Soil Day. Here's a year of living soil.",
          image: '/wormhole/tiles/pl20261205-v1-1.jpg',
        },
        {
          text: 'Boubacar, Guinea. Coffee grown in a syntropic agroforest.',
          image: '/wormhole/tiles/pl20261205-v1-2.jpg',
        },
        {
          text: 'Christina, Tennessee. From advertising to a soil business.',
          image: '/wormhole/tiles/pl20261205-v1-3.jpg',
        },
        {
          text: 'Ibrahim, Turkey. More than 80 growers going regenerative.',
          image: '/wormhole/tiles/pl20261205-v1-4.jpg',
        },
        {
          text: 'Arthur, Brazil. A prize-winning farm school.',
          image: '/wormhole/tiles/pl20261205-v1-5.jpg',
        },
        {
          text: 'Joseph, Kenya. Teaching his whole community.',
          image: '/wormhole/tiles/pl20261205-v1-6.jpg',
        },
        {
          text: 'Thank you for protecting the ground we all stand on.',
          image: '/wormhole/tiles/pl20261205-v1-7.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/05-12-2026-world-soil-day-v1.pptx. Boubacar photo from his own post (d02). Globe: Natural Earth (public domain). Theme line "Our future is rooted in soil" from the FAO World Soil Day site: verify it is the 2026 theme. Other graduates: PHOTO placeholders.',
  },
  {
    key: '2026-10-23 pl20261206 slides v1',
    post: 'pl20261206',
    set: {
      slides: [
        { text: 'Trial name, place and season.', image: '/wormhole/tiles/pl20261206-v1-1.jpg' },
        { text: 'The question they tested.', image: '/wormhole/tiles/pl20261206-v1-2.jpg' },
        { text: 'The method in 3 lines.', image: '/wormhole/tiles/pl20261206-v1-3.jpg' },
        { text: 'The result, one big number.', image: '/wormhole/tiles/pl20261206-v1-4.jpg' },
        {
          text: "What surprised them, including what didn't work.",
          image: '/wormhole/tiles/pl20261206-v1-5.jpg',
        },
        { text: 'Who ran it.', image: '/wormhole/tiles/pl20261206-v1-6.jpg' },
      ],
    },
    reason:
      'Template visuals (Linnea, 23 Oct): placeholder text kept as written, labelled PHOTO spaces to fill. Deck: /wormhole/decks/06-12-2026-field-notes-02-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261207 slides v1',
    post: 'pl20261207',
    set: {
      slides: [
        {
          text: 'Myth: "Add 1% organic matter and your soil holds 20,000 more gallons of water per acre."',
          image: '/wormhole/tiles/pl20261207-v1-1.jpg',
        },
        {
          text: 'A 2018 review of about 60 studies tested that claim.',
          image: '/wormhole/tiles/pl20261207-v1-2.jpg',
        },
        {
          text: 'A 1% rise in soil organic carbon raised available water only slightly, on average about 1 mm per 10 cm of soil.',
          image: '/wormhole/tiles/pl20261207-v1-3.jpg',
        },
        {
          text: 'The effect was larger in sandy soils and smaller in clays.',
          image: '/wormhole/tiles/pl20261207-v1-4.jpg',
        },
        {
          text: 'Where biology really helps water: aggregates and pores that let rain soak in instead of running off.',
          image: '/wormhole/tiles/pl20261207-v1-5.jpg',
        },
        {
          text: 'Honest numbers build trust. Source on the slide.',
          image: '/wormhole/tiles/pl20261207-v1-6.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/07-12-2026-myth-organic-matter-and-water-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261209 slides v1',
    post: 'pl20261209',
    set: {
      slides: [
        { text: 'FREE WEBINAR', image: '/wormhole/tiles/pl20261209-v1-1.jpg' },
        { text: '[Webinar title]', image: '/wormhole/tiles/pl20261209-v1-2.jpg' },
        { text: '[Date and time, three time zones]', image: '/wormhole/tiles/pl20261209-v1-3.jpg' },
        { text: '[Host name]', image: '/wormhole/tiles/pl20261209-v1-4.jpg' },
        { text: 'Free. Link in bio.', image: '/wormhole/tiles/pl20261209-v1-5.jpg' },
      ],
    },
    reason:
      'Template visuals (Linnea, 23 Oct): placeholder text kept as written, labelled PHOTO spaces to fill. Deck: /wormhole/decks/09-12-2026-free-webinar-december-v1.pptx. Micrograph: Casey Williams.',
  },
  {
    key: '2026-10-23 pl20261212 slides v1',
    post: 'pl20261212',
    set: {
      slides: [
        { text: 'Your worms get cold too.', image: '/wormhole/tiles/pl20261212-v1-1.jpg' },
        {
          text: 'Red wigglers slow down below about 10°C and die if the bin freezes.',
          image: '/wormhole/tiles/pl20261212-v1-2.jpg',
        },
        {
          text: 'Move the bin to a shed, garage or basement.',
          image: '/wormhole/tiles/pl20261212-v1-3.jpg',
        },
        {
          text: 'Add extra shredded cardboard as insulation, and feed less.',
          image: '/wormhole/tiles/pl20261212-v1-4.jpg',
        },
        {
          text: 'Keep the bedding damp, like a wrung-out sponge.',
          image: '/wormhole/tiles/pl20261212-v1-5.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/12-12-2026-do-this-weekend-worm-bin-winter-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261214 slides v1',
    post: 'pl20261214',
    set: {
      slides: [
        {
          text: "33% of the world's soils are moderately to highly degraded.",
          image: '/wormhole/tiles/pl20261214-v1-1.jpg',
        },
        {
          text: 'The causes: erosion, loss of organic carbon, salinization, compaction, acidification and pollution.',
          image: '/wormhole/tiles/pl20261214-v1-2.jpg',
        },
        {
          text: 'Forming a few centimeters of new soil can take centuries.',
          image: '/wormhole/tiles/pl20261214-v1-3.jpg',
        },
        {
          text: 'Restoring soil biology is one of the fastest ways to rebuild it.',
          image: '/wormhole/tiles/pl20261214-v1-4.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/14-12-2026-soil-in-numbers-degraded-v1.pptx. Micrograph: Marco Trevisan.',
  },
  {
    key: '2026-10-23 pl20261218 slides v1',
    post: 'pl20261218',
    set: {
      slides: [
        { text: 'Fun Soil News: December 2026.', image: '/wormhole/tiles/pl20261218-v1-1.jpg' },
        {
          text: 'Story 1. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261218-v1-2.jpg',
        },
        {
          text: 'Story 2. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261218-v1-3.jpg',
        },
        {
          text: 'Story 3. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261218-v1-4.jpg',
        },
        {
          text: 'Story 4. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261218-v1-5.jpg',
        },
        {
          text: 'Story 5. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261218-v1-6.jpg',
        },
      ],
    },
    reason:
      'Template visuals (Linnea, 23 Oct): placeholder text kept as written, labelled PHOTO spaces to fill. Deck: /wormhole/decks/18-12-2026-fun-soil-news-december-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261219 slides v1',
    post: 'pl20261219',
    set: {
      slides: [
        {
          text: 'What is your soil made of? Find out with a jar.',
          image: '/wormhole/tiles/pl20261219-v1-1.jpg',
        },
        {
          text: 'Fill a jar one third with soil, top up with water and a pinch of dish soap. Shake hard.',
          image: '/wormhole/tiles/pl20261219-v1-2.jpg',
        },
        {
          text: 'Sand settles in about a minute. Mark the line.',
          image: '/wormhole/tiles/pl20261219-v1-3.jpg',
        },
        {
          text: 'Silt settles over a few hours. Mark it. Clay can take a day or more.',
          image: '/wormhole/tiles/pl20261219-v1-4.jpg',
        },
        {
          text: 'Compare the layers to find your texture.',
          image: '/wormhole/tiles/pl20261219-v1-5.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/19-12-2026-do-this-weekend-jar-test-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261223 slides v1',
    post: 'pl20261223',
    set: {
      slides: [
        { text: 'FROM OUR PARTNERS', image: '/wormhole/tiles/pl20261223-v1-1.jpg' },
        { text: '[Partner name]', image: '/wormhole/tiles/pl20261223-v1-2.jpg' },
        { text: '[One line on their work]', image: '/wormhole/tiles/pl20261223-v1-3.jpg' },
      ],
    },
    reason:
      'Template visuals (Linnea, 23 Oct): placeholder text kept as written, labelled PHOTO spaces to fill. Deck: /wormhole/decks/23-12-2026-partner-share-december-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261228 slides v1',
    post: 'pl20261228',
    set: {
      slides: [
        {
          text: 'Myth: "Humus is a special, stable substance in soil."',
          image: '/wormhole/tiles/pl20261228-v1-1.jpg',
        },
        {
          text: 'For a century, textbooks described humic substances as large, unique molecules.',
          image: '/wormhole/tiles/pl20261228-v1-2.jpg',
        },
        {
          text: 'Modern imaging found little of that in intact soil. Much of it came from the harsh extraction method.',
          image: '/wormhole/tiles/pl20261228-v1-3.jpg',
        },
        {
          text: 'The current view: organic matter is a continuum of compounds being broken down by microbes.',
          image: '/wormhole/tiles/pl20261228-v1-4.jpg',
        },
        {
          text: "Carbon stays in soil mainly when it's protected in aggregates or bound to minerals.",
          image: '/wormhole/tiles/pl20261228-v1-5.jpg',
        },
        {
          text: 'Microbes are part of the answer. Source on the slide.',
          image: '/wormhole/tiles/pl20261228-v1-6.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): flat brand colour, real micrographs and photos, simple drawn diagrams, no AI images. Deck: /wormhole/decks/28-12-2026-myth-humus-v1.pptx. Micrograph: Marco Trevisan.',
  },
  {
    key: '2026-10-23 pl20261230 slides v1',
    post: 'pl20261230',
    set: {
      slides: [
        {
          text: 'Soil Regenerators in the wild. [Name], Simalungun Regency, Sumatra, Indonesia',
          image: '/wormhole/tiles/pl20261230-v1-1.jpg',
        },
        {
          text: 'Farming the way their parents did. Then they looked under a microscope.',
          image: '/wormhole/tiles/pl20261230-v1-2.jpg',
        },
        {
          text: 'Regenerative compost, checked under the microscope.',
          image: '/wormhole/tiles/pl20261230-v1-3.jpg',
        },
        {
          text: 'Fields mapped, companion plants and ground cover planted.',
          image: '/wormhole/tiles/pl20261230-v1-4.jpg',
        },
        {
          text: '"It has enriched the people, plants and animals in the Simalungun regency where I call home."',
          image: '/wormhole/tiles/pl20261230-v1-5.jpg',
        },
      ],
    },
    reason:
      'Template visuals (Linnea, 23 Oct): placeholder text kept as written, labelled PHOTO spaces to fill. Deck: /wormhole/decks/30-12-2026-soil-regenerators-sumatra-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261107 slides v1',
    post: 'pl20261107',
    set: {
      slides: [
        { text: 'Trial name, place and season.', image: '/wormhole/tiles/pl20261107-v1-1.jpg' },
        { text: 'The question they tested.', image: '/wormhole/tiles/pl20261107-v1-2.jpg' },
        { text: 'The method in 3 lines.', image: '/wormhole/tiles/pl20261107-v1-3.jpg' },
        { text: 'The result, one big number.', image: '/wormhole/tiles/pl20261107-v1-4.jpg' },
        {
          text: "What surprised them, including what didn't work.",
          image: '/wormhole/tiles/pl20261107-v1-5.jpg',
        },
        { text: 'Who ran it.', image: '/wormhole/tiles/pl20261107-v1-6.jpg' },
      ],
    },
    reason:
      'Template visuals (Linnea, 23 Oct): placeholder text kept as written, labelled PHOTO spaces to fill. Deck: /wormhole/decks/07-11-2026-field-notes-01-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261125 slides v1',
    post: 'pl20261125',
    set: {
      slides: [
        { text: 'Meet our mentors. [Name], [role].', image: '/wormhole/tiles/pl20261125-v1-1.jpg' },
        {
          text: '[Their one line of advice, in their words.]',
          image: '/wormhole/tiles/pl20261125-v1-2.jpg',
        },
      ],
    },
    reason:
      'Template visuals (Linnea, 23 Oct): placeholder text kept as written, labelled PHOTO spaces to fill. Deck: /wormhole/decks/25-11-2026-mentor-spotlight-november-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261127 slides v1',
    post: 'pl20261127',
    set: {
      slides: [
        { text: 'Fun Soil News: November 2026.', image: '/wormhole/tiles/pl20261127-v1-1.jpg' },
        {
          text: 'Story 1. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261127-v1-2.jpg',
        },
        {
          text: 'Story 2. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261127-v1-3.jpg',
        },
        {
          text: 'Story 3. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261127-v1-4.jpg',
        },
        {
          text: 'Story 4. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261127-v1-5.jpg',
        },
        {
          text: 'Story 5. Country in big type, one sentence, source.',
          image: '/wormhole/tiles/pl20261127-v1-6.jpg',
        },
      ],
    },
    reason:
      'Template visuals (Linnea, 23 Oct): placeholder text kept as written, labelled PHOTO spaces to fill. Deck: /wormhole/decks/27-11-2026-fun-soil-news-november-v1.pptx.',
  },
  {
    key: '2026-10-23 d10 slides v1',
    post: 'd10',
    set: {
      slides: [
        {
          text: 'What does "regenerative" actually mean, and who gets to decide?',
          image: '/wormhole/tiles/d10-v1-1.jpg',
        },
      ],
    },
    reason:
      'New image (Linnea, 23 Oct): flat brand colour, real soil cutouts. Deck: /wormhole/decks/15-10-2026-what-does-regenerative-mean-v1.pptx.',
  },
  {
    key: '2026-10-23 d16 single image',
    post: 'd16',
    set: { slides: [{ text: '', image: '/wormhole/tiles/d16-w1.jpg' }] },
    reason:
      'Removed two empty slides (no text, no image, 23 Oct): this LinkedIn post is a single image.',
  },
  {
    key: '2026-10-23 pl20261102 slides v1',
    post: 'pl20261102',
    set: {
      slides: [
        {
          text: 'Bacterial feeder: open, tube-shaped mouth',
          image: '/wormhole/tiles/pl20261102-v1-1.jpg',
        },
        {
          text: 'Fungal feeder: a thin stylet to pierce hyphae',
          image: '/wormhole/tiles/pl20261102-v1-2.jpg',
        },
        {
          text: 'Root feeder: a heavy stylet to pierce roots',
          image: '/wormhole/tiles/pl20261102-v1-3.jpg',
        },
        { text: 'Predator: teeth or a wide mouth', image: '/wormhole/tiles/pl20261102-v1-4.jpg' },
        { text: 'Read the mouth, know the job.', image: '/wormhole/tiles/pl20261102-v1-5.jpg' },
      ],
    },
    reason:
      'New Reel cards (Linnea, 23 Oct): real micrographs in lenses with labelled arrows; 1080 x 1920 versions in the deck: /wormhole/decks/02-11-2026-read-the-drop-nematode-mouths-v1.pptx. Micrographs (CC BY 4.0, cropped, credited on each slide): Tandingan De Ley et al. 2023 PLOS ONE; Munawar et al. 2024 Microorganisms; Handoo et al. 2021 Plants; Altash et al. 2024 ZooKeys.',
  },
  {
    key: '2026-10-23 pl20261221 slides v1',
    post: 'pl20261221',
    set: {
      slides: [
        {
          text: 'Fungal hypha: same width along its whole length.',
          image: '/wormhole/tiles/pl20261221-v1-1.jpg',
        },
        { text: 'Parallel walls, often branching.', image: '/wormhole/tiles/pl20261221-v1-2.jpg' },
        {
          text: 'Debris: irregular edges, changing width.',
          image: '/wormhole/tiles/pl20261221-v1-3.jpg',
        },
        {
          text: 'Actinomycetes: much thinner threads.',
          image: '/wormhole/tiles/pl20261221-v1-4.jpg',
        },
      ],
    },
    reason:
      'New Reel cards (Linnea, 23 Oct): real micrographs in lenses with labelled arrows; 1080 x 1920 versions in the deck: /wormhole/decks/21-12-2026-read-the-drop-hyphae-or-debris-v1.pptx. Micrographs (CC BY 4.0, cropped, credited on each slide): Gondal, Rauf and Naz 2019 Scientific Reports; Matthew Rozanoff / iNaturalist (the debris photo is a squash of an earth-fan fungus, not a soil extract); Du et al. 2025 PLOS ONE.',
  },
  {
    key: '2026-10-23 pl20261225 slides v1',
    post: 'pl20261225',
    set: {
      slides: [
        { text: 'Happy holidays', image: '/wormhole/tiles/pl20261225-v1-1.jpg' },
        {
          text: 'from all of us at the Soil Food Web School.',
          image: '/wormhole/tiles/pl20261225-v1-2.jpg',
        },
      ],
    },
    reason:
      'New card (Linnea, 23 Oct): real tardigrades cut out of micrographs, drawn Santa hats and leaves, on cream. Credits on the slides: Stec et al. 2018 PLOS ONE; Jan Ebr and Ivana Ebrová / iNaturalist; CC BY 4.0. Deck: /wormhole/decks/25-12-2026-holiday-card-tardigrades-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261114 slides v1',
    post: 'pl20261114',
    set: {
      slides: [
        {
          text: 'Your fallen leaves can become fungal compost.',
          image: '/wormhole/tiles/pl20261114-v1-1.jpg',
        },
        {
          text: 'Pack wet leaves into a wire cage or a bag with holes.',
          image: '/wormhole/tiles/pl20261114-v1-2.jpg',
        },
        {
          text: 'Keep them damp. Fungi do the work, slowly.',
          image: '/wormhole/tiles/pl20261114-v1-3.jpg',
        },
        {
          text: 'In 1 to 2 years you get dark, crumbly leaf mold.',
          image: '/wormhole/tiles/pl20261114-v1-4.jpg',
        },
        {
          text: 'Use it as mulch or mix it into potting soil.',
          image: '/wormhole/tiles/pl20261114-v1-5.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): openly licensed real photos (CC BY, CC0 or public domain, credited on each slide) and simple drawn diagrams on a flat brand colour. Deck: /wormhole/decks/14-11-2026-do-this-weekend-leaf-mold-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261115 slides v1',
    post: 'pl20261115',
    set: {
      slides: [
        {
          text: 'Imagine a world without earthworms.',
          image: '/wormhole/tiles/pl20261115-v1-1.jpg',
        },
        { text: 'It already exists.', image: '/wormhole/tiles/pl20261115-v1-2.jpg' },
        {
          text: 'Many northern North American forests evolved without them after the last Ice Age.',
          image: '/wormhole/tiles/pl20261115-v1-3.jpg',
        },
        {
          text: 'Introduced worms now eat through the leaf litter those forests depend on.',
          image: '/wormhole/tiles/pl20261115-v1-4.jpg',
        },
        {
          text: 'Even a good organism can be the wrong one in the wrong place.',
          image: '/wormhole/tiles/pl20261115-v1-5.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): openly licensed real photos (CC BY, CC0 or public domain, credited on each slide) and simple drawn diagrams on a flat brand colour. Reel: 1080 x 1920 cards in the deck. Deck: /wormhole/decks/15-11-2026-a-world-without-worms-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261121 slides v1',
    post: 'pl20261121',
    set: {
      slides: [
        {
          text: "Bare soil in winter is soil you're losing.",
          image: '/wormhole/tiles/pl20261121-v1-1.jpg',
        },
        {
          text: 'Rain hits bare soil hard, breaks aggregates apart and washes the fine particles away.',
          image: '/wormhole/tiles/pl20261121-v1-2.jpg',
        },
        {
          text: 'Cover it: leaf mulch, straw, woodchips or a winter cover crop.',
          image: '/wormhole/tiles/pl20261121-v1-3.jpg',
        },
        {
          text: 'Soil life keeps working under the cover, and your beds are ready in spring.',
          image: '/wormhole/tiles/pl20261121-v1-4.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): openly licensed real photos (CC BY, CC0 or public domain, credited on each slide) and simple drawn diagrams on a flat brand colour. Deck: /wormhole/decks/21-11-2026-do-this-weekend-cover-bare-beds-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261126 slides v1',
    post: 'pl20261126',
    set: {
      slides: [
        {
          text: 'This Thanksgiving, thank the soil life that grew your dinner.',
          image: '/wormhole/tiles/pl20261126-v1-1.jpg',
        },
        {
          text: 'The potatoes: fungi and bacteria cycled the nutrients.',
          image: '/wormhole/tiles/pl20261126-v1-2.jpg',
        },
        {
          text: 'The green beans: rhizobia in the roots turned air into nitrogen.',
          image: '/wormhole/tiles/pl20261126-v1-3.jpg',
        },
        {
          text: 'The pumpkin pie: mycorrhizal fungi helped the vines find water and phosphorus.',
          image: '/wormhole/tiles/pl20261126-v1-4.jpg',
        },
        {
          text: 'Happy Thanksgiving from all of us. 💚',
          image: '/wormhole/tiles/pl20261126-v1-5.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): openly licensed real photos (CC BY, CC0 or public domain, credited on each slide) and simple drawn diagrams on a flat brand colour. The nodule photo is a soybean (no openly licensed green-bean nodule photo found); the label says so. Deck: /wormhole/decks/26-11-2026-thanksgiving-soil-life-v1.pptx.',
  },
  {
    key: '2026-10-23 pl20261211 slides v1',
    post: 'pl20261211',
    set: {
      slides: [
        {
          text: 'Mountain soils are thin, young and fragile.',
          image: '/wormhole/tiles/pl20261211-v1-1.jpg',
        },
        {
          text: 'Cold and steep slopes slow soil formation.',
          image: '/wormhole/tiles/pl20261211-v1-2.jpg',
        },
        {
          text: 'Without roots and cover, one heavy storm can wash away centuries of soil.',
          image: '/wormhole/tiles/pl20261211-v1-3.jpg',
        },
        {
          text: 'Terraces, cover and living roots hold mountain farms together.',
          image: '/wormhole/tiles/pl20261211-v1-4.jpg',
        },
      ],
    },
    reason:
      'New slides (Linnea, 23 Oct): openly licensed real photos (CC BY, CC0 or public domain, credited on each slide) and simple drawn diagrams on a flat brand colour. Deck: /wormhole/decks/11-12-2026-mountain-day-mountain-soils-v1.pptx.',
  },
  {
    key: '2026-10-23 save soil ss-01',
    post: 'ss-01',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: "Save Soil shoutout: Valluvan's coconut farm, 0.86% to 2.33% organic matter",
      platform: 'Instagram',
      caption:
        "Valluvan's yields did nothing for three years. Then they climbed. 🌴\n\nHis Tamil Nadu coconut farm started at 0.86% soil organic matter. He dug trenches between the coconut rows and filled them with leaf litter, stopped burning fronds, mulched around every crop, and planted nutmeg, banana, black pepper, turmeric and timber trees in layers under the palms.\n\nFrom year four the coconuts rose: 140 nuts per tree, up from 90-100. By year seven the soil read 1.5% organic matter, and the latest test reads 2.33%. Fertiliser costs are under a tenth of what they were.\n\nIn 2018, after two years of drought, more than 1,200 mm of rain fell in a few days. His neighbours' open wells stood 6-7 feet lower than his.\n\nThat buried leaf litter is food for fungi and bacteria, and their glues and threads are what turn soil into a sponge.\n\nFull case study from Save Soil (Isha Foundation). Link in bio: https://consciousplanet.org/en/save-soil/news/save-soil-movement-model-farm-proof-of-concept\n\n#SaveSoil #ConsciousPlanet #SoilFoodWeb #SoilHealth #SoilBiology #LivingSoil",
      slides: [
        {
          text: 'A coconut farm went from 0.86% to 2.33% soil organic matter',
          image: '/wormhole/tiles/ss-01-v1-1.jpg',
        },
        {
          text: 'Coconuts per tree: 90-100 before, 140 now. Nothing changed in the first three years.',
          image: '/wormhole/tiles/ss-01-v1-2.jpg',
        },
        {
          text: 'Fertiliser spending: under 10% of what it was. Workers: 1, down from 10-20.',
          image: '/wormhole/tiles/ss-01-v1-3.jpg',
        },
        {
          text: '2018: over 1,200 mm of rain in a few days, after two years of drought.',
          image: '/wormhole/tiles/ss-01-v1-4.jpg',
        },
        {
          text: "His neighbours' open wells stood 6-7 feet lower than his.",
          image: '/wormhole/tiles/ss-01-v1-5.jpg',
        },
        {
          text: 'What he did: leaf litter trenches between rows, mulch, layered crops, no burning, no summer ploughing.',
          image: '/wormhole/tiles/ss-01-v1-6.jpg',
        },
      ],
      cta: 'Read the full case study',
      link: 'https://consciousplanet.org/en/save-soil/news/save-soil-movement-model-farm-proof-of-concept',
      sources: [
        'https://consciousplanet.org/en/save-soil/news/save-soil-movement-model-farm-proof-of-concept',
      ],
      visual_note:
        'Instagram carousel, 6 slides, article repost card (the pinned New York Times format). Built with tools/wormhole-visuals/savesoil.py. Photo: Save Soil (Isha Foundation), from the article.',
      note: "Checked against the Save Soil page on 23 Oct. The article's own table gives different figures (160 nuts per tree now, fertigation down 75%) from its text (140 nuts, fertiliser under 10%); the caption uses the text. 'No runoff' was cut: not on the page. Collab tag: add Save Soil's Instagram handle if Linnea confirms it.",
      status: 'draft',
    },
    reason:
      "Save Soil shoutout (Linnea, 23 Oct): from Evan's share of the Save Soil analysis library. Undated draft with its repost card.",
  },
  {
    key: '2026-10-23 save soil ss-02',
    post: 'ss-02',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Save Soil shoutout: 5 numbers that show what soil life does',
      platform: 'Instagram',
      caption:
        'Same almond yields, twice the profit, and water that soaks in six times faster. 🌱\n\nThat is one of the numbers Save Soil (Isha Foundation) gathered to argue that soil biology belongs in how countries track climate adaptation. Our favourites:\n\n1. Infiltration 6x faster in regenerative almond orchards (LaCanne et al. 2021).\n2. Microbial biomass carbon 133% higher in regenerative organic systems (Mäder et al. 2025).\n3. Diversified rotations had 2.4 to 13.5 times more earthworm biomass than rye monoculture in a long-term Lithuanian trial (Bogušas et al. 2022).\n4. Glomalin-related soil protein, made by mycorrhizal fungi, up 24% under perennial pasture restoration (Abán et al. 2025).\n5. In drought years, maize in legume and manure systems outyielded conventional by 38 to 137% (Lotter et al. 2003).\n\nEvery one of these is the soil food web at work. Save this for the next time someone asks whether biology shows up in the numbers.\n\nLink in bio: https://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga\n\n#SaveSoil #ConsciousPlanet #SoilFoodWeb #SoilHealth #SoilBiology #LivingSoil',
      slides: [
        {
          text: '5 numbers that show what soil life does',
          image: '/wormhole/tiles/ss-02-v1-1.jpg',
        },
        {
          text: '6x faster: water soaking into regenerative almond orchards (LaCanne et al. 2021)',
          image: '/wormhole/tiles/ss-02-v1-2.jpg',
        },
        {
          text: '133% more microbial biomass carbon in regenerative organic soils (Mäder et al. 2025)',
          image: '/wormhole/tiles/ss-02-v1-3.jpg',
        },
        {
          text: '2.4 to 13.5x more earthworm biomass in diversified rotations than in rye monoculture (Bogušas et al. 2022)',
          image: '/wormhole/tiles/ss-02-v1-4.jpg',
        },
        {
          text: '+24% glomalin, the fungal protein that glues soil crumbs together, under perennial pasture (Abán et al. 2025)',
          image: '/wormhole/tiles/ss-02-v1-5.jpg',
        },
        {
          text: '+38-137% maize yield in drought years in legume and manure systems (Lotter et al. 2003)',
          image: '/wormhole/tiles/ss-02-v1-6.jpg',
        },
      ],
      cta: 'Save this',
      link: 'https://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga',
      sources: [
        'https://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga',
      ],
      visual_note:
        'Instagram carousel, 6 slides, article repost card (the pinned New York Times format). Built with tools/wormhole-visuals/savesoil.py. Photo: Donald Hobern, CC BY 2.0 (Wikimedia Commons, Lumbricus terrestris 26559560801).',
      note: "Checked against the Save Soil page on 23 Oct. 'Continuous rye' became 'rye monoculture' and 'bean monoculture' was cut: the page says neither. Collab tag: add Save Soil's Instagram handle if Linnea confirms it.",
      status: 'draft',
    },
    reason:
      "Save Soil shoutout (Linnea, 23 Oct): from Evan's share of the Save Soil analysis library. Undated draft with its repost card.",
  },
  {
    key: '2026-10-23 save soil ss-03',
    post: 'ss-03',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Save Soil shoutout: COP30, USD 1 trillion for energy, USD 9 billion for agriculture',
      platform: 'LinkedIn',
      caption:
        "COP30's Action Agenda put nearly USD 1 trillion behind renewable energy and modern grids. Agriculture and food systems: USD 9 billion.\n\nSave Soil's (Isha Foundation) COP30 analysis lays out the gap. The Sharm el-Sheikh Joint Work, the only official negotiation track on agriculture and food systems, closed with no outcome, and its mandate ends in 2026. Their verdict on the USD 9 billion: an order of magnitude too small to unlock what soils can do for the climate.\n\nWhat would it take for soil to get its own line in climate finance?\n\nhttps://consciousplanet.org/en/save-soil/news/cop30-a-turning-point-for-climate-action-but-agriculture-and-soils-left-behind",
      slides: [
        {
          text: 'USD 1 trillion for energy. USD 9 billion for agriculture.',
          image: '/wormhole/tiles/ss-03-v1-1.jpg',
        },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/cop30-a-turning-point-for-climate-action-but-agriculture-and-soils-left-behind',
      sources: [
        'https://consciousplanet.org/en/save-soil/news/cop30-a-turning-point-for-climate-action-but-agriculture-and-soils-left-behind',
      ],
      visual_note:
        'LinkedIn single image, 1200 x 627, article repost card (the pinned New York Times format). Built with tools/wormhole-visuals/savesoil.py. Photo: High-Level Champions, CC BY 4.0 (Wikimedia Commons, COP30 High Level Event, 19 Nov 2025).',
      note: "Checked against the Save Soil page on 23 Oct. The paragraph about farmers carrying the cost of the transition years was cut: not in the article. Collab tag: add Save Soil's Instagram handle if Linnea confirms it.",
      status: 'draft',
    },
    reason:
      "Save Soil shoutout (Linnea, 23 Oct): from Evan's share of the Save Soil analysis library. Undated draft with its repost card.",
  },
  {
    key: '2026-10-23 save soil ss-04',
    post: 'ss-04',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Save Soil shoutout: tillage releases carbon that soil life locked away',
      platform: 'LinkedIn',
      caption:
        'A plough releases carbon that soil life spent years locking away.\n\nRoots feed microbes, microbes make sticky polysaccharides, fungal hyphae wrap soil particles into aggregates, and carbon inside those crumbs is shielded from decomposition. Tillage breaks the crumbs open.\n\nA meta-analysis of 46 studies found tilled soils emitted 21% more CO2 than untilled ones, and 29% more where soil organic carbon was below 1% (Abdalla et al. 2016). A six-year field trial measured 51% less CO2 on average under no-till with surface mulch (Mühlbachová et al. 2023).\n\nSave Soil (Isha Foundation) gathers these in their paper on regenerative agriculture and climate.\n\nWhat has cutting tillage looked like on the land you work with?\n\nhttps://consciousplanet.org/en/save-soil/news/mitigating-climate-change-through-soil-revitalization-using-regenerative-ag',
      slides: [
        {
          text: 'Tilled soil released 21% more CO2. In low-carbon soil, 29%.',
          image: '/wormhole/tiles/ss-04-v1-1.jpg',
        },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/mitigating-climate-change-through-soil-revitalization-using-regenerative-ag',
      sources: [
        'https://consciousplanet.org/en/save-soil/news/mitigating-climate-change-through-soil-revitalization-using-regenerative-ag',
      ],
      visual_note:
        'LinkedIn single image, 1200 x 627, article repost card (the pinned New York Times format). Built with tools/wormhole-visuals/savesoil.py. Photo: USDA NRCS South Dakota, public domain (Wikimedia Commons, No-till farming system in Brookings Co., SD).',
      note: "Checked against the Save Soil page on 23 Oct. The mechanism paragraph is SFW's own explanation; the Save Soil page covers roots, microbes and aggregates but not polysaccharides or hyphae. Collab tag: add Save Soil's Instagram handle if Linnea confirms it.",
      status: 'draft',
    },
    reason:
      "Save Soil shoutout (Linnea, 23 Oct): from Evan's share of the Save Soil analysis library. Undated draft with its repost card.",
  },
  {
    key: '2026-10-23 save soil ss-05',
    post: 'ss-05',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Save Soil shoutout: soil may hold 59% of all life on Earth',
      platform: 'Instagram',
      caption:
        "Soil may be home to 59% of all life on Earth (Anthony et al., PNAS 2023). 🔬\n\nBacteria, archaea, fungi, protozoa, nematodes, mites, springtails, earthworms, beetles. Save Soil's (Isha Foundation) paper on soil degradation and biodiversity walks through how they build the ground: microbes feed on sugars from roots and make sticky substances, fungal hyphae bind particles into crumbs, and earthworms and mites open channels for air and water.\n\nAbout 33% of the world's soils are already moderately to highly degraded. Every one of those organisms is what regeneration brings back.\n\nLink in bio: https://consciousplanet.org/en/save-soil/news/soil-degradation-and-biodiversity-loss\n\n#SaveSoil #ConsciousPlanet #SoilFoodWeb #SoilHealth #SoilBiology #LivingSoil",
      slides: [
        {
          text: 'Soil may be home to 59% of all life on Earth',
          image: '/wormhole/tiles/ss-05-v1-1.jpg',
        },
      ],
      cta: 'Send this to someone who thinks soil is just dirt',
      link: 'https://consciousplanet.org/en/save-soil/news/soil-degradation-and-biodiversity-loss',
      sources: [
        'https://consciousplanet.org/en/save-soil/news/soil-degradation-and-biodiversity-loss',
      ],
      visual_note:
        'Instagram single image, article repost card (the pinned New York Times format). Built with tools/wormhole-visuals/savesoil.py. Photo: Lewis Fausak, CC BY-SA 4.0 (Wikimedia Commons, Springtail on soil).',
      note: "Checked against the Save Soil page on 23 Oct. 'More than half of all species' became '59% of all life', the paper's wording. Collab tag: add Save Soil's Instagram handle if Linnea confirms it.",
      status: 'draft',
    },
    reason:
      "Save Soil shoutout (Linnea, 23 Oct): from Evan's share of the Save Soil analysis library. Undated draft with its repost card.",
  },
  {
    key: '2026-10-23 save soil ss-06',
    post: 'ss-06',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Save Soil shoutout: healthy soil and healthy humans',
      platform: 'Instagram',
      caption:
        "In baboons, the soil they lived on shaped their gut bacteria 15 times more strongly than their genes. 🦠\n\nIn people, a study of over 1,000 adults found that less than 8% of the gut microbiome is inherited (Rothschild et al. 2018). The rest comes from what we eat and where we live, and soil is part of that.\n\nThe same soil life decides what is in our food. Mycorrhizal fungi move copper, iron, nitrogen, phosphorus and zinc into roots. Rhizobia in legume roots fix nitrogen from the air.\n\nFrom Save Soil's (Isha Foundation) paper Healthy Soil and Healthy Humans. Link in bio: https://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans\n\n#SaveSoil #ConsciousPlanet #SoilFoodWeb #SoilHealth #SoilBiology #LivingSoil",
      slides: [
        {
          text: 'Where you live shapes your gut more than your genes do',
          image: '/wormhole/tiles/ss-06-v1-1.jpg',
        },
        {
          text: 'Baboons: the soil around them shaped their gut microbes 15x more strongly than their genetics',
          image: '/wormhole/tiles/ss-06-v1-2.jpg',
        },
        {
          text: 'People: under 8% of the gut microbiome is inherited (Rothschild et al. 2018)',
          image: '/wormhole/tiles/ss-06-v1-3.jpg',
        },
        {
          text: 'Mycorrhizal fungi carry copper, iron, nitrogen, phosphorus and zinc into crops',
          image: '/wormhole/tiles/ss-06-v1-4.jpg',
        },
        {
          text: 'Rhizobia in legume roots turn nitrogen from the air into plant food',
          image: '/wormhole/tiles/ss-06-v1-5.jpg',
        },
      ],
      cta: 'Save this',
      link: 'https://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans',
      sources: ['https://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans'],
      visual_note:
        'Instagram carousel, 5 slides, article repost card (the pinned New York Times format). Built with tools/wormhole-visuals/savesoil.py. Photo: Marc-André Selosse, CC0 (Wikimedia Commons, arbuscular mycorrhiza in maize root), cropped to remove its labels.',
      note: "Checked against the Save Soil page on 23 Oct. The leafy greens figure (80% less magnesium and calcium) was cut: it is not on the page. The hook says 'where you live' because the human study measured environment, not soil alone. Collab tag: add Save Soil's Instagram handle if Linnea confirms it.",
      status: 'draft',
    },
    reason:
      "Save Soil shoutout (Linnea, 23 Oct): from Evan's share of the Save Soil analysis library. Undated draft with its repost card.",
  },
  {
    key: '2026-10-23 save soil ss-07',
    post: 'ss-07',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Save Soil shoutout: Secure Soil, Save Life',
      platform: 'LinkedIn',
      caption:
        "Soil is starting to be written into law as a matter of security.\n\nThree recent steps: the IUCN's mandate, from the World Conservation Congress, to develop a global legal instrument for soil security; the Pan-African Parliament's endorsement of a Model Law on sustainable soil management; and the European Union's Soil Monitoring Law.\n\nSecure Soil, Save Life, from the Aroura Soil Security Think Tank, IUCN's World Commission on Environmental Law and Save Soil (Isha Foundation), calls soil \"the planet's quiet infrastructure\": it feeds people, filters water, regulates climate and holds biodiversity.\n\nShould soil be treated as critical infrastructure where you work?\n\nhttps://consciousplanet.org/en/save-soil/news/secure-soil-save-life",
      slides: [
        {
          text: 'Soil is becoming security policy.',
          image: '/wormhole/tiles/ss-07-v1-1.jpg',
        },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/secure-soil-save-life',
      sources: ['https://consciousplanet.org/en/save-soil/news/secure-soil-save-life'],
      visual_note:
        'LinkedIn single image, 1200 x 627, article repost card (the pinned New York Times format). Built with tools/wormhole-visuals/savesoil.py. Photo: Mclund, CC BY 4.0 (Wikimedia Commons, Soil profile 0-125cm).',
      note: "Checked against the Save Soil page on 23 Oct. 'Soil law moved further in 2025 than in the decade before it' was cut: the report does not claim it. Collab tag: add Save Soil's Instagram handle if Linnea confirms it.",
      status: 'draft',
    },
    reason:
      "Save Soil shoutout (Linnea, 23 Oct): from Evan's share of the Save Soil analysis library. Undated draft with its repost card.",
  },
  {
    key: '2026-10-23 save soil ss-08',
    post: 'ss-08',
    create: {
      iso_date: '2026-10-23',
      date_tbd: true,
      topic: 'Save Soil shoutout: the soil carbon sponge cools the land',
      platform: 'Instagram',
      caption:
        "Land with living soil runs cooler than bare ground, and water is the reason. 💧\n\nSave Soil's (Isha Foundation) report The Soil Carbon Sponge, built on Walter Jehne's work, explains it. Soil rich in organic matter soaks up rain and holds it. Plants pull that water up and release it through their leaves, and evaporation carries heat away. When soil degrades, the water runs off, and the same sunlight heats the air instead.\n\nFrom the soil food web side: the sponge is built by biology. Fungal hyphae and bacterial glues hold the pores open, and cover crops and mulch keep it from drying out.\n\nLink in bio: https://consciousplanet.org/en/save-soil/news/the-soil-carbon-sponge\n\n#SaveSoil #ConsciousPlanet #SoilFoodWeb #SoilHealth #SoilBiology #LivingSoil",
      slides: [
        {
          text: 'Healthy soil cools the land',
          image: '/wormhole/tiles/ss-08-v1-1.jpg',
        },
        {
          text: 'Water in soil evaporates through plants and carries heat away',
          image: '/wormhole/tiles/ss-08-v1-2.jpg',
        },
        {
          text: "Bare, degraded soil can't hold that water, so the sun heats the air instead",
          image: '/wormhole/tiles/ss-08-v1-3.jpg',
        },
        {
          text: 'Cover crops and mulch keep the ground from baking',
          image: '/wormhole/tiles/ss-08-v1-4.jpg',
        },
        {
          text: "Fungal threads and bacterial glues hold the sponge's pores open",
          image: '/wormhole/tiles/ss-08-v1-5.jpg',
        },
      ],
      cta: 'Save this',
      link: 'https://consciousplanet.org/en/save-soil/news/the-soil-carbon-sponge',
      sources: ['https://consciousplanet.org/en/save-soil/news/the-soil-carbon-sponge'],
      visual_note:
        'Instagram carousel, 5 slides, article repost card (the pinned New York Times format). Built with tools/wormhole-visuals/savesoil.py. Photo: Antonio Jordán, CC BY-SA 3.0 (Wikimedia Commons, Subangular Blocky Soil Aggregate in Spain).',
      note: "Checked against the Save Soil page on 23 Oct. 'Organic matter holds many times its own weight in water' was cut: not on the page. The page's 250,000 litres per 1% figure is unsourced, so it is not used. Collab tag: add Save Soil's Instagram handle if Linnea confirms it.",
      status: 'draft',
    },
    reason:
      "Save Soil shoutout (Linnea, 23 Oct): from Evan's share of the Save Soil analysis library. Undated draft with its repost card.",
  },
  {
    key: '2026-10-23 p18 slides v5',
    post: 'p18',
    set: {
      slides: [
        { text: 'Vampire amoeba.', image: '/wormhole/tiles/p18-v5-1.jpg' },
        {
          text: 'It latches onto an algal cell and drills through the wall.',
          image: '/wormhole/tiles/p18-v5-2.jpg',
        },
        { text: 'Then it drains what is inside.', image: '/wormhole/tiles/p18-v5-3.jpg' },
        {
          text: 'Our mentor Wes Sander wrote all about them on our blog. Link in bio.',
          image: '/wormhole/tiles/p18-v5-4.jpg',
        },
      ],
    },
    caption: [
      [
        '\n#Halloween #SoilFoodWeb',
        '\nPhotos: Hess, Sausen & Melkonian 2012, PLoS ONE, cropped, CC BY 4.0 (creativecommons.org/licenses/by/4.0)\n#Halloween #SoilFoodWeb',
      ],
    ],
    reason:
      'Reel finished (Linnea, 23 Oct): the cover plus three cards with real Vampyrella lateritia photos (Hess, Sausen and Melkonian 2012, PLoS ONE, CC BY 4.0), credit added to the caption. 1080 x 1920 cards in the deck: /wormhole/decks/31-10-2026-vampire-amoeba-reel-v5.pptx. Blog headers for Wes: "Meet the Vampire Amoeba" is a working title.',
  },
  {
    key: '2026-10-24 ss-01 to 23 Dec',
    post: 'ss-01',
    set: { iso_date: '2026-12-23', date_tbd: false },
    reason:
      "Dated Wed 23 Dec (Linnea, 24 Oct): Valluvan's farm fills the December partner share slot.",
  },
  {
    key: '2026-10-24 pl20261223 replaced',
    post: 'pl20261223',
    set: { date_tbd: true },
    reason:
      'Date TBD (Linnea, 24 Oct): the 23 Dec partner share slot now goes to the Save Soil shoutout ss-01. This template stays for the next partner.',
  },
  {
    key: '2026-10-24 evan ev-01',
    post: 'ev-01',
    create: {
      iso_date: '2026-10-24',
      date_tbd: true,
      topic: 'Reshare: Ashley McKeon, From surviving to thriving: the case for soil health',
      platform: 'LinkedIn',
      caption:
        "The Soil Health Institute's new President and CEO, Ashley McKeon, makes the case for soil health in her first long piece since taking the role in June.\n\n[One line from the article that matches what we teach: name the organism or the practice.]\n\n[One line on why it matters for growers.]\n\nRead it here: https://www.linkedin.com/pulse/from-surviving-thriving-case-soil-health-ashley-r-mckeon-nsrsc\n\n#SoilHealth #SoilFoodWeb #RegenerativeAgriculture",
      slides: [{ text: 'LinkedIn reshare: the article preview card is the visual.', image: null }],
      cta: 'Read the article',
      link: 'https://www.linkedin.com/pulse/from-surviving-thriving-case-soil-health-ashley-r-mckeon-nsrsc',
      sources: [
        'https://www.linkedin.com/pulse/from-surviving-thriving-case-soil-health-ashley-r-mckeon-nsrsc',
        'https://hpj.com/2026/05/29/mckean-to-lead-soil-health-institute/',
      ],
      visual_note:
        "Reshare on LinkedIn with the article's own preview card. Tag Ashley McKeon and the Soil Health Institute.",
      note: 'From Evan (Tue): "From surviving to thriving, the case for soil health". LinkedIn blocks automated reading, so the two bracketed lines need one quote each from the article itself. McKeon became SHI President and CEO on 1 June 2026 (High Plains Journal).',
      status: 'draft',
    },
    reason: "Evan's share (Linnea, 24 Oct): LinkedIn reshare draft.",
  },
  {
    key: '2026-10-24 evan ev-02',
    post: 'ev-02',
    create: {
      iso_date: '2026-10-24',
      date_tbd: true,
      topic: 'Shoutout: beopen.earth',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        '[Hook: the one thing beopen.earth does that our community should know.]\n\n[Two lines on what they do and who it is for.]\n\nGo have a look: https://beopen.earth/\n\n#SoilFoodWeb #SoilHealth',
      slides: [{ text: 'beopen.earth', image: null }],
      cta: 'Visit beopen.earth',
      link: 'https://beopen.earth/',
      sources: ['https://beopen.earth/'],
      visual_note:
        'Partner shoutout. Use a screenshot of their site or a photo they share with us, inside the flat colour-box layout.',
      note: 'From Evan (Tue): "This is worth a share and shoutout!" The site blocks automated reading, so the description lines need their About text. Tag their account.',
      status: 'draft',
    },
    reason: "Evan's share (Linnea, 24 Oct): shoutout draft.",
  },
  {
    key: '2026-10-24 n20261023a sheffield',
    post: 'n20261023a',
    set: {
      link: 'https://sheffield.ac.uk/biosciences/news/ancient-fungus-unlocks-secret-support-system-major-food-crops-could-transform-farming-practices',
      sources: [
        'https://sheffield.ac.uk/biosciences/news/ancient-fungus-unlocks-secret-support-system-major-food-crops-could-transform-farming-practices',
        'https://doi.org/10.1016/j.cub.2026.09.061',
        'https://phys.org/news/2026-10-ancient-fungus-secret-major-food.html',
      ],
      visual_note:
        'Collage carousel, 3 slides, one soil profile under all three. Deck: news-mustard-plant-fungus.pptx. LinkedIn version: same caption, tag Professor Katie Field and the University of Sheffield School of Biosciences.',
    },
    caption: [
      [
        'For us it is one more reminder that the soil food web reaches further than the textbooks said.\nRead the study through the link in bio.',
        'Professor Jurriaan Ton calls it an "ideal model system" for finding out how plants build this other kind of partnership. Taking it from the lab to the field could cut reliance on "expensive chemical fertilisers".\nFor us it is one more reminder that the soil food web reaches further than the textbooks said.\nRead the University of Sheffield story through the link in bio.',
      ],
      [' #Mycorrhiza', ''],
    ],
    reason:
      'Evan shared the University of Sheffield story (24 Oct, "Breakthrough science alert!"). Link now goes to Sheffield\'s own page, Jurriaan Ton\'s quote added, #Mycorrhiza dropped because the fungus is a fine root endophyte, and the LinkedIn note now tags the lab instead of ending on a question. Evan also asked Stephanie to invite the researchers to a Q1 webinar.',
  },
  {
    key: '2026-10-24 save soil ss-05 date',
    post: 'ss-05',
    set: { iso_date: '2026-11-08', date_tbd: false },
    reason:
      'Dated (24 Oct): Sun 8 Nov, an empty day: a single card that works any time. Partner shares go on days outside the Mon/Wed/Fri feed posts where possible.',
  },
  {
    key: '2026-10-24 save soil ss-04 date',
    post: 'ss-04',
    set: { iso_date: '2026-11-17', date_tbd: false },
    reason:
      'Dated (24 Oct): Tue 17 Nov on LinkedIn, an empty day. Partner shares go on days outside the Mon/Wed/Fri feed posts where possible.',
  },
  {
    key: '2026-10-24 save soil ss-08 date',
    post: 'ss-08',
    set: { iso_date: '2026-11-19', date_tbd: false },
    reason:
      "Dated (24 Oct): Thu 19 Nov, two days before 'Do this weekend: cover bare beds' (21 Nov): same message, cover the ground. Partner shares go on days outside the Mon/Wed/Fri feed posts where possible.",
  },
  {
    key: '2026-10-24 save soil ss-06 date',
    post: 'ss-06',
    set: { iso_date: '2026-11-24', date_tbd: false },
    reason:
      'Dated (24 Oct): Tue 24 Nov, Thanksgiving week: soil, food and health before the Thanksgiving post (26 Nov). Partner shares go on days outside the Mon/Wed/Fri feed posts where possible.',
  },
  {
    key: '2026-10-24 save soil ss-03 date',
    post: 'ss-03',
    set: { iso_date: '2026-12-01', date_tbd: false },
    reason:
      'Dated (24 Oct): Tue 1 Dec on LinkedIn, an empty feed day. Partner shares go on days outside the Mon/Wed/Fri feed posts where possible.',
  },
  {
    key: '2026-10-24 save soil ss-02 date',
    post: 'ss-02',
    set: { iso_date: '2026-12-08', date_tbd: false },
    reason:
      'Dated (24 Oct): Tue 8 Dec, an empty day after World Soil Day. Partner shares go on days outside the Mon/Wed/Fri feed posts where possible.',
  },
  {
    key: '2026-10-24 save soil ss-07 date',
    post: 'ss-07',
    set: { iso_date: '2026-12-10', date_tbd: false },
    reason:
      'Dated (24 Oct): Thu 10 Dec on LinkedIn, an empty day. Partner shares go on days outside the Mon/Wed/Fri feed posts where possible.',
  },
  {
    key: '2026-10-24 save soil ss-01 slides v2',
    post: 'ss-01',
    set: {
      slides: [
        {
          text: 'A coconut farm went from 0.86% to 2.33% soil organic matter',
          image: '/wormhole/tiles/ss-01-v2-1.jpg',
        },
        {
          text: 'Coconuts per tree: 90-100 before, 140 now. Nothing changed in the first three years.',
          image: '/wormhole/tiles/ss-01-v2-2.jpg',
        },
        {
          text: 'Fertiliser spending: under 10% of what it was. Workers: 1, down from 10-20.',
          image: '/wormhole/tiles/ss-01-v2-3.jpg',
        },
        {
          text: '2018: over 1,200 mm of rain in a few days, after two years of drought.',
          image: '/wormhole/tiles/ss-01-v2-4.jpg',
        },
        {
          text: "His neighbours' open wells stood 6-7 feet lower than his.",
          image: '/wormhole/tiles/ss-01-v2-5.jpg',
        },
        {
          text: 'What he did: leaf litter trenches between rows, mulch, layered crops, no burning, no summer ploughing.',
          image: '/wormhole/tiles/ss-01-v2-6.jpg',
        },
      ],
    },
    reason:
      'New cards (24 Oct), on brand: Food Web Green background, cream card, Soil Brown Montserrat headline, Regenerative Green bar, Source Sans 3 body, per the 2026 brand guide and color guidelines. v1 had a near-black background and Poppins.',
  },
  {
    key: '2026-10-24 save soil ss-02 slides v2',
    post: 'ss-02',
    set: {
      slides: [
        {
          text: '5 numbers that show what soil life does',
          image: '/wormhole/tiles/ss-02-v2-1.jpg',
        },
        {
          text: '6x faster: water soaking into regenerative almond orchards (LaCanne et al. 2021)',
          image: '/wormhole/tiles/ss-02-v2-2.jpg',
        },
        {
          text: '133% more microbial biomass carbon in regenerative organic soils (Mäder et al. 2025)',
          image: '/wormhole/tiles/ss-02-v2-3.jpg',
        },
        {
          text: '2.4 to 13.5x more earthworm biomass in diversified rotations than in rye monoculture (Bogušas et al. 2022)',
          image: '/wormhole/tiles/ss-02-v2-4.jpg',
        },
        {
          text: '+24% glomalin, the fungal protein that glues soil crumbs together, under perennial pasture (Abán et al. 2025)',
          image: '/wormhole/tiles/ss-02-v2-5.jpg',
        },
        {
          text: '+38-137% maize yield in drought years in legume and manure systems (Lotter et al. 2003)',
          image: '/wormhole/tiles/ss-02-v2-6.jpg',
        },
      ],
    },
    reason:
      'New cards (24 Oct), on brand: Food Web Green background, cream card, Soil Brown Montserrat headline, Regenerative Green bar, Source Sans 3 body, per the 2026 brand guide and color guidelines. v1 had a near-black background and Poppins.',
  },
  {
    key: '2026-10-24 save soil ss-03 slides v2',
    post: 'ss-03',
    set: {
      slides: [
        {
          text: 'USD 1 trillion for energy. USD 9 billion for agriculture.',
          image: '/wormhole/tiles/ss-03-v2-1.jpg',
        },
      ],
    },
    reason:
      'New cards (24 Oct), on brand: Food Web Green background, cream card, Soil Brown Montserrat headline, Regenerative Green bar, Source Sans 3 body, per the 2026 brand guide and color guidelines. v1 had a near-black background and Poppins.',
  },
  {
    key: '2026-10-24 save soil ss-04 slides v2',
    post: 'ss-04',
    set: {
      slides: [
        {
          text: 'Tilled soil released 21% more CO2. In low-carbon soil, 29%.',
          image: '/wormhole/tiles/ss-04-v2-1.jpg',
        },
      ],
    },
    reason:
      'New cards (24 Oct), on brand: Food Web Green background, cream card, Soil Brown Montserrat headline, Regenerative Green bar, Source Sans 3 body, per the 2026 brand guide and color guidelines. v1 had a near-black background and Poppins.',
  },
  {
    key: '2026-10-24 save soil ss-05 slides v2',
    post: 'ss-05',
    set: {
      slides: [
        {
          text: 'Soil may be home to 59% of all life on Earth',
          image: '/wormhole/tiles/ss-05-v2-1.jpg',
        },
      ],
    },
    reason:
      'New cards (24 Oct), on brand: Food Web Green background, cream card, Soil Brown Montserrat headline, Regenerative Green bar, Source Sans 3 body, per the 2026 brand guide and color guidelines. v1 had a near-black background and Poppins.',
  },
  {
    key: '2026-10-24 save soil ss-06 slides v2',
    post: 'ss-06',
    set: {
      slides: [
        {
          text: 'Where you live shapes your gut more than your genes do',
          image: '/wormhole/tiles/ss-06-v2-1.jpg',
        },
        {
          text: 'Baboons: the soil around them shaped their gut microbes 15x more strongly than their genetics',
          image: '/wormhole/tiles/ss-06-v2-2.jpg',
        },
        {
          text: 'People: under 8% of the gut microbiome is inherited (Rothschild et al. 2018)',
          image: '/wormhole/tiles/ss-06-v2-3.jpg',
        },
        {
          text: 'Mycorrhizal fungi carry copper, iron, nitrogen, phosphorus and zinc into crops',
          image: '/wormhole/tiles/ss-06-v2-4.jpg',
        },
        {
          text: 'Rhizobia in legume roots turn nitrogen from the air into plant food',
          image: '/wormhole/tiles/ss-06-v2-5.jpg',
        },
      ],
    },
    reason:
      'New cards (24 Oct), on brand: Food Web Green background, cream card, Soil Brown Montserrat headline, Regenerative Green bar, Source Sans 3 body, per the 2026 brand guide and color guidelines. v1 had a near-black background and Poppins.',
  },
  {
    key: '2026-10-24 save soil ss-07 slides v2',
    post: 'ss-07',
    set: {
      slides: [
        { text: 'Soil is becoming security policy.', image: '/wormhole/tiles/ss-07-v2-1.jpg' },
      ],
    },
    reason:
      'New cards (24 Oct), on brand: Food Web Green background, cream card, Soil Brown Montserrat headline, Regenerative Green bar, Source Sans 3 body, per the 2026 brand guide and color guidelines. v1 had a near-black background and Poppins.',
  },
  {
    key: '2026-10-24 save soil ss-08 slides v2',
    post: 'ss-08',
    set: {
      slides: [
        { text: 'Healthy soil cools the land', image: '/wormhole/tiles/ss-08-v2-1.jpg' },
        {
          text: 'Water in soil evaporates through plants and carries heat away',
          image: '/wormhole/tiles/ss-08-v2-2.jpg',
        },
        {
          text: "Bare, degraded soil can't hold that water, so the sun heats the air instead",
          image: '/wormhole/tiles/ss-08-v2-3.jpg',
        },
        {
          text: 'Cover crops and mulch keep the ground from baking',
          image: '/wormhole/tiles/ss-08-v2-4.jpg',
        },
        {
          text: "Fungal threads and bacterial glues hold the sponge's pores open",
          image: '/wormhole/tiles/ss-08-v2-5.jpg',
        },
      ],
    },
    reason:
      'New cards (24 Oct), on brand: Food Web Green background, cream card, Soil Brown Montserrat headline, Regenerative Green bar, Source Sans 3 body, per the 2026 brand guide and color guidelines. v1 had a near-black background and Poppins.',
  },
  {
    key: '2026-10-24 ev-01 caption',
    post: 'ev-01',
    caption: [
      [
        "The Soil Health Institute's new President and CEO, Ashley McKeon, makes the case for soil health in her first long piece since taking the role in June.\n\n[One line from the article that matches what we teach: name the organism or the practice.]\n\n[One line on why it matters for growers.]",
        'Cotton farmers with established soil health systems earned $118 more net income per acre than they did under their old conventional systems.\n\nThat is Soil Health Institute research, shared by SHI President and CEO Ashley McKeon after a plenary panel at the Textile Exchange Conference in Vancouver. For context, USDA estimated the 2025 US cotton crop fell about $201 per planted acre short of its full economic cost. She is careful to say the two numbers are not directly comparable.\n\nHer message to the apparel companies in the room: stop asking when you can stop paying for regenerative agriculture. Savings on inputs and equipment come first. Yield, yield stability and revenue follow later, as soil health indicators improve. So support should change with each stage, from cost-share, equipment financing and technical help early on to multi-year purchasing commitments and payments for ecosystem outcomes later.\n\nUnder every one of those indicators is soil biology: the fungi and bacteria that build structure, hold water and cycle nutrients. That is the part we teach.',
      ],
    ],
    reason:
      "Caption written from the article text Linnea pasted (24 Oct): McKeon, 19 Oct 2026, after the Textile Exchange Conference panel. Figures as she gives them: SHI's $118/acre net income gain, USDA's $201/acre 2025 shortfall, with her caveat that they are not directly comparable.",
  },
  {
    key: '2026-10-24 ev-02 caption',
    post: 'ev-02',
    set: {
      link: 'https://beopen.earth/atlas',
      sources: [
        'https://beopen.earth/',
        'https://beopen.earth/atlas',
        'https://fields4ever.biomemakers.com/',
      ],
      slides: [
        { text: 'An open map of soil life', image: null },
        { text: '100,000 soil samples. 90+ countries. One protocol.', image: null },
        {
          text: 'Bacteria and fungi, open to everyone. Explore the Atlas at beopen.earth',
          image: null,
        },
      ],
      visual_note:
        'Partner shoutout carousel, 3 slides. Slide 1: a screenshot of the BeOpen Atlas map inside a flat colour box. Slides 2 and 3: brand colour boxes over a soil or microscope photo from our library. Tag BeOpen and Biome Makers.',
    },
    caption: [
      [
        '[Hook: the one thing beopen.earth does that our community should know.]\n\n[Two lines on what they do and who it is for.]\n\nGo have a look: https://beopen.earth/',
        'There is now an open map of the bacteria and fungi in more than 100,000 soil samples from over 90 countries.\n\nBeOpen, an open project by Biome Makers, collects, sequences and analyses every sample with the same protocol, so a sample from one continent can be compared directly with one from another. Researchers get free access to raw reads and processed data. Regulators can see which soil microorganisms have been found in each region, with every data point linked to where it came from. Labs can join as contributors with the Becrop Standard protocol.\n\nOver 200 research partners and 3,000 datasets so far. Supported by the European Union and powered by Fields4Ever.\n\nGo explore the Atlas: https://beopen.earth/atlas',
      ],
      [
        '#SoilFoodWeb #SoilHealth',
        '#SoilFoodWeb #SoilMicrobiome #SoilBiology #OpenScience #SoilHealth',
      ],
    ],
    reason:
      "Caption and slide text written from beopen.earth's own page text, pasted by Linnea (24 Oct). Figures from the site: 100k samples, 90+ countries, 200+ partners, 3k datasets.",
  },
  {
    key: '2026-10-24 november ev-02',
    post: 'ev-02',
    set: { iso_date: '2026-11-18', date_tbd: false },
    reason:
      'Moved into November (Linnea, 24 Oct): everything Evan has already shared goes out in November at the latest, because December is kept for new material. Wed 18 Nov, an empty day.',
  },
  {
    key: '2026-10-24 november ss-01',
    post: 'ss-01',
    set: { iso_date: '2026-11-20', date_tbd: false },
    reason:
      'Moved into November (Linnea, 24 Oct): everything Evan has already shared goes out in November at the latest, because December is kept for new material. Fri 20 Nov, an empty day.',
  },
  {
    key: '2026-10-24 november ss-02',
    post: 'ss-02',
    set: { iso_date: '2026-11-22', date_tbd: false },
    reason:
      'Moved into November (Linnea, 24 Oct): everything Evan has already shared goes out in November at the latest, because December is kept for new material. Sun 22 Nov, an empty day.',
  },
  {
    key: '2026-10-24 november ss-07',
    post: 'ss-07',
    set: { iso_date: '2026-11-19', date_tbd: false },
    reason:
      'Moved into November (Linnea, 24 Oct): everything Evan has already shared goes out in November at the latest, because December is kept for new material. Thu 19 Nov on LinkedIn, beside the Instagram-only carbon sponge post.',
  },
  {
    key: '2026-10-24 november ss-03',
    post: 'ss-03',
    set: { iso_date: '2026-11-24', date_tbd: false },
    reason:
      'Moved into November (Linnea, 24 Oct): everything Evan has already shared goes out in November at the latest, because December is kept for new material. Tue 24 Nov on LinkedIn, beside the Instagram-only gut microbes post.',
  },
  {
    key: '2026-10-24 november ev-01',
    post: 'ev-01',
    set: { iso_date: '2026-11-30', date_tbd: false },
    reason:
      'Moved into November (Linnea, 24 Oct): everything Evan has already shared goes out in November at the latest, because December is kept for new material. Mon 30 Nov on LinkedIn, beside the ciliates Reel (Instagram only).',
  },
  {
    key: '2026-10-24 november pl20261223 back',
    post: 'pl20261223',
    set: { iso_date: '2026-12-23', date_tbd: false },
    reason:
      'Back on Wed 23 Dec (24 Oct): the Save Soil post moved to November, so the December partner share slot is free for new material.',
  },
  {
    key: '2026-10-24 d26 slides v2',
    post: 'd26',
    set: {
      slides: [
        { text: 'The smell of rain is a chemical signal.', image: '/wormhole/tiles/d26-v2-1.jpg' },
        { text: 'Geosmin, made by Streptomyces bacteria.', image: '/wormhole/tiles/d26-v2-2.jpg' },
        { text: 'It attracts springtails.', image: '/wormhole/tiles/d26-v2-3.jpg' },
        {
          text: 'They eat the colony and carry its spores away.',
          image: '/wormhole/tiles/d26-v2-4.jpg',
        },
      ],
    },
    caption: [
      [
        '#Petrichor #SoilBiology',
        'Photos: no-till soil after rain; actinobacteria by Rodrigue Ullens; Collembola by Cameron Radman (SFW microscope library)\n#Petrichor #SoilBiology',
      ],
    ],
    reason:
      'New visual (Linnea, 24 Oct): the old one had italic type and small flower cutouts on cream. Now flat brand-colour boxes over real photos from the SFW microscope library, with one green band running across all four slides. Built with tools/wormhole-visuals/d26_rain.py.',
  },
  {
    key: '2026-10-24 save soil ss-01-li',
    post: 'ss-01-li',
    create: {
      iso_date: '2026-12-23',
      date_tbd: false,
      topic:
        "Save Soil shoutout (LinkedIn): Valluvan's coconut farm, 0.86% to 2.33% organic matter",
      platform: 'LinkedIn',
      caption:
        "Valluvan's yields did nothing for three years. Then they climbed.\n\nHis Tamil Nadu coconut farm started at 0.86% soil organic matter. He dug trenches between the coconut rows and filled them with leaf litter, stopped burning fronds, mulched around every crop, and planted nutmeg, banana, black pepper, turmeric and timber trees in layers under the palms.\n\nFrom year four the coconuts rose: 140 nuts per tree, up from 90-100. By year seven the soil read 1.5% organic matter, and the latest test reads 2.33%. Fertiliser costs are under a tenth of what they were.\n\nIn 2018, after two years of drought, more than 1,200 mm of rain fell in a few days. His neighbours' open wells stood 6-7 feet lower than his.\n\nThat buried leaf litter is food for fungi and bacteria, and their glues and threads are what turn soil into a sponge.\n\nFull case study from Save Soil (Isha Foundation).\n\nIf you farm or advise farmers: how long did your soil take before the yields answered?\n\nhttps://consciousplanet.org/en/save-soil/news/save-soil-movement-model-farm-proof-of-concept",
      slides: [
        {
          text: 'A coconut farm went from 0.86% to 2.33% soil organic matter',
          image: '/wormhole/tiles/ss-01-li-v1-1.jpg',
        },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/save-soil-movement-model-farm-proof-of-concept',
      sources: [
        'https://consciousplanet.org/en/save-soil/news/save-soil-movement-model-farm-proof-of-concept',
      ],
      visual_note:
        'LinkedIn single image, 1200 x 627, the same repost card as the Instagram post ss-01. Built with tools/wormhole-visuals/savesoil.py --linkedin-twins.',
      note: "LinkedIn twin of ss-01, same day. Caption is the Instagram caption without hashtags, emoji or 'link in bio', ending with a question (CLAUDE.md: every LinkedIn post ends with a real question).",
      status: 'draft',
    },
    reason:
      'LinkedIn version of the Save Soil shoutout (Linnea, 24 Oct: the landscape repost card works well for LinkedIn).',
  },
  {
    key: '2026-10-24 save soil ss-02-li',
    post: 'ss-02-li',
    create: {
      iso_date: '2026-12-08',
      date_tbd: false,
      topic: 'Save Soil shoutout (LinkedIn): 5 numbers that show what soil life does',
      platform: 'LinkedIn',
      caption:
        'Same almond yields, twice the profit, and water that soaks in six times faster.\n\nThat is one of the numbers Save Soil (Isha Foundation) gathered to argue that soil biology belongs in how countries track climate adaptation. Our favourites:\n\n1. Infiltration 6x faster in regenerative almond orchards (LaCanne et al. 2021).\n2. Microbial biomass carbon 133% higher in regenerative organic systems (Mäder et al. 2025).\n3. Diversified rotations had 2.4 to 13.5 times more earthworm biomass than rye monoculture in a long-term Lithuanian trial (Bogušas et al. 2022).\n4. Glomalin-related soil protein, made by mycorrhizal fungi, up 24% under perennial pasture restoration (Abán et al. 2025).\n5. In drought years, maize in legume and manure systems outyielded conventional by 38 to 137% (Lotter et al. 2003).\n\nEvery one of these is the soil food web at work. Save this for the next time someone asks whether biology shows up in the numbers.\n\nWhich soil biology measure would you want national adaptation plans to track first?\n\nhttps://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga',
      slides: [
        {
          text: '5 numbers that show what soil life does',
          image: '/wormhole/tiles/ss-02-li-v1-1.jpg',
        },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga',
      sources: [
        'https://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga',
      ],
      visual_note:
        'LinkedIn single image, 1200 x 627, the same repost card as the Instagram post ss-02. Built with tools/wormhole-visuals/savesoil.py --linkedin-twins.',
      note: "LinkedIn twin of ss-02, same day. Caption is the Instagram caption without hashtags, emoji or 'link in bio', ending with a question (CLAUDE.md: every LinkedIn post ends with a real question).",
      status: 'draft',
    },
    reason:
      'LinkedIn version of the Save Soil shoutout (Linnea, 24 Oct: the landscape repost card works well for LinkedIn).',
  },
  {
    key: '2026-10-24 save soil ss-05-li',
    post: 'ss-05-li',
    create: {
      iso_date: '2026-11-08',
      date_tbd: false,
      topic: 'Save Soil shoutout (LinkedIn): soil may hold 59% of all life on Earth',
      platform: 'LinkedIn',
      caption:
        "Soil may be home to 59% of all life on Earth (Anthony et al., PNAS 2023).\n\nBacteria, archaea, fungi, protozoa, nematodes, mites, springtails, earthworms, beetles. Save Soil's (Isha Foundation) paper on soil degradation and biodiversity walks through how they build the ground: microbes feed on sugars from roots and make sticky substances, fungal hyphae bind particles into crumbs, and earthworms and mites open channels for air and water.\n\nAbout 33% of the world's soils are already moderately to highly degraded. Every one of those organisms is what regeneration brings back.\n\nWhich soil organism do you think deserves more attention than it gets?\n\nhttps://consciousplanet.org/en/save-soil/news/soil-degradation-and-biodiversity-loss",
      slides: [
        {
          text: 'Soil may be home to 59% of all life on Earth',
          image: '/wormhole/tiles/ss-05-li-v1-1.jpg',
        },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/soil-degradation-and-biodiversity-loss',
      sources: [
        'https://consciousplanet.org/en/save-soil/news/soil-degradation-and-biodiversity-loss',
      ],
      visual_note:
        'LinkedIn single image, 1200 x 627, the same repost card as the Instagram post ss-05. Built with tools/wormhole-visuals/savesoil.py --linkedin-twins.',
      note: "LinkedIn twin of ss-05, same day. Caption is the Instagram caption without hashtags, emoji or 'link in bio', ending with a question (CLAUDE.md: every LinkedIn post ends with a real question).",
      status: 'draft',
    },
    reason:
      'LinkedIn version of the Save Soil shoutout (Linnea, 24 Oct: the landscape repost card works well for LinkedIn).',
  },
  {
    key: '2026-10-24 save soil ss-06-li',
    post: 'ss-06-li',
    create: {
      iso_date: '2026-11-24',
      date_tbd: false,
      topic: 'Save Soil shoutout (LinkedIn): healthy soil and healthy humans',
      platform: 'LinkedIn',
      caption:
        "In baboons, the soil they lived on shaped their gut bacteria 15 times more strongly than their genes.\n\nIn people, a study of over 1,000 adults found that less than 8% of the gut microbiome is inherited (Rothschild et al. 2018). The rest comes from what we eat and where we live, and soil is part of that.\n\nThe same soil life decides what is in our food. Mycorrhizal fungi move copper, iron, nitrogen, phosphorus and zinc into roots. Rhizobia in legume roots fix nitrogen from the air.\n\nFrom Save Soil's (Isha Foundation) paper Healthy Soil and Healthy Humans.\n\nShould soil health have a place in public health conversations?\n\nhttps://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans",
      slides: [
        {
          text: 'Where you live shapes your gut more than your genes do',
          image: '/wormhole/tiles/ss-06-li-v1-1.jpg',
        },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans',
      sources: ['https://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans'],
      visual_note:
        'LinkedIn single image, 1200 x 627, the same repost card as the Instagram post ss-06. Built with tools/wormhole-visuals/savesoil.py --linkedin-twins.',
      note: "LinkedIn twin of ss-06, same day. Caption is the Instagram caption without hashtags, emoji or 'link in bio', ending with a question (CLAUDE.md: every LinkedIn post ends with a real question).",
      status: 'draft',
    },
    reason:
      'LinkedIn version of the Save Soil shoutout (Linnea, 24 Oct: the landscape repost card works well for LinkedIn).',
  },
  {
    key: '2026-10-24 save soil ss-08-li',
    post: 'ss-08-li',
    create: {
      iso_date: '2026-11-19',
      date_tbd: false,
      topic: 'Save Soil shoutout (LinkedIn): the soil carbon sponge cools the land',
      platform: 'LinkedIn',
      caption:
        "Land with living soil runs cooler than bare ground, and water is the reason.\n\nSave Soil's (Isha Foundation) report The Soil Carbon Sponge, built on Walter Jehne's work, explains it. Soil rich in organic matter soaks up rain and holds it. Plants pull that water up and release it through their leaves, and evaporation carries heat away. When soil degrades, the water runs off, and the same sunlight heats the air instead.\n\nFrom the soil food web side: the sponge is built by biology. Fungal hyphae and bacterial glues hold the pores open, and cover crops and mulch keep it from drying out.\n\nWhere have you seen covered ground stay cooler or wetter than bare ground nearby?\n\nhttps://consciousplanet.org/en/save-soil/news/the-soil-carbon-sponge",
      slides: [
        {
          text: 'Healthy soil cools the land',
          image: '/wormhole/tiles/ss-08-li-v1-1.jpg',
        },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/the-soil-carbon-sponge',
      sources: ['https://consciousplanet.org/en/save-soil/news/the-soil-carbon-sponge'],
      visual_note:
        'LinkedIn single image, 1200 x 627, the same repost card as the Instagram post ss-08. Built with tools/wormhole-visuals/savesoil.py --linkedin-twins.',
      note: "LinkedIn twin of ss-08, same day. Caption is the Instagram caption without hashtags, emoji or 'link in bio', ending with a question (CLAUDE.md: every LinkedIn post ends with a real question).",
      status: 'draft',
    },
    reason:
      'LinkedIn version of the Save Soil shoutout (Linnea, 24 Oct: the landscape repost card works well for LinkedIn).',
  },
  {
    key: '2026-10-24 p25 slides b1',
    post: 'p25',
    set: {
      slides: [
        { text: "Dr. Elaine's papers, in one place.", image: '/wormhole/tiles/p25-b1-1.jpg' },
        {
          text: 'Four decades of research, open to read. 77 journal papers, 6 book chapters and 10 EPA and technical reports, each linked to where you can read it.',
          image: '/wormhole/tiles/p25-b1-2.jpg',
        },
      ],
    },
    reason:
      'New visual (Linnea, 24 Oct): the old one used Fredoka, italics or flower cutouts on a plain background, outside the brand. Now flat brand-colour boxes over real photos in Montserrat and Source Sans 3, the same style as the smell of rain post. Built with tools/wormhole-visuals/boxes.py.',
  },
  {
    key: '2026-10-24 p26 slides b1',
    post: 'p26',
    set: {
      slides: [
        { text: 'Welcome to our newest consultants.', image: '/wormhole/tiles/p26-b1-1.jpg' },
        {
          text: 'Kyle Babcock, United States. Certified Soil Food Web Consultant.',
          image: '/wormhole/tiles/p26-b1-2.jpg',
        },
        {
          text: 'Joshua Stone, United States. Certified Soil Food Web Consultant.',
          image: '/wormhole/tiles/p26-b1-3.jpg',
        },
      ],
    },
    caption: [
      ['[Names and countries.]', 'Kyle Babcock, United States\nJoshua Stone, United States'],
    ],
    reason:
      'New visual (Linnea, 24 Oct): the old one used Fredoka, italics or flower cutouts on a plain background, outside the brand. Now flat brand-colour boxes over real photos in Montserrat and Source Sans 3, the same style as the smell of rain post. Built with tools/wormhole-visuals/boxes.py. Joshua Stone has no photo yet, so his slide is a name card: send one and it gets his portrait.',
  },
  {
    key: '2026-10-24 pl20261114 slides b1',
    post: 'pl20261114',
    set: {
      slides: [
        {
          text: 'Your fallen leaves can become fungal compost.',
          image: '/wormhole/tiles/pl20261114-b1-1.jpg',
        },
        {
          text: 'Pack wet leaves into a wire cage or a bag with holes.',
          image: '/wormhole/tiles/pl20261114-b1-2.jpg',
        },
        {
          text: 'Keep them damp. Fungi do the work, slowly.',
          image: '/wormhole/tiles/pl20261114-b1-3.jpg',
        },
        {
          text: 'In 1 to 2 years you get dark, crumbly leaf mold.',
          image: '/wormhole/tiles/pl20261114-b1-4.jpg',
        },
        {
          text: 'Use it as mulch or mix it into potting soil.',
          image: '/wormhole/tiles/pl20261114-b1-5.jpg',
        },
      ],
    },
    reason:
      'New visual (Linnea, 24 Oct): the old one used Fredoka, italics or flower cutouts on a plain background, outside the brand. Now flat brand-colour boxes over real photos in Montserrat and Source Sans 3, the same style as the smell of rain post. Built with tools/wormhole-visuals/boxes.py.',
  },
  {
    key: '2026-10-24 pl20261115 slides b1',
    post: 'pl20261115',
    set: {
      slides: [
        {
          text: 'Imagine a world without earthworms.',
          image: '/wormhole/tiles/pl20261115-b1-1.jpg',
        },
        { text: 'It already exists.', image: '/wormhole/tiles/pl20261115-b1-2.jpg' },
        {
          text: 'Many northern North American forests evolved without them after the last Ice Age.',
          image: '/wormhole/tiles/pl20261115-b1-3.jpg',
        },
        {
          text: 'Introduced worms now eat through the leaf litter those forests depend on.',
          image: '/wormhole/tiles/pl20261115-b1-4.jpg',
        },
        {
          text: 'Even a good organism can be the wrong one in the wrong place.',
          image: '/wormhole/tiles/pl20261115-b1-5.jpg',
        },
      ],
    },
    reason:
      'New visual (Linnea, 24 Oct): the old one used Fredoka, italics or flower cutouts on a plain background, outside the brand. Now flat brand-colour boxes over real photos in Montserrat and Source Sans 3, the same style as the smell of rain post. Built with tools/wormhole-visuals/boxes.py.',
  },
  {
    key: '2026-10-24 p27 duplicate',
    post: 'p27',
    set: { date_tbd: true },
    reason:
      'Date TBD (24 Oct): a duplicate of cr20261112, "A day at the Costa Rica workshop" on 12 Nov, and it gave 18 to 25 January where the workshop runs 18 to 29 January. Kept here in case the copy is wanted.',
  },
  {
    key: '2026-10-24 p26 slides f1',
    post: 'p26',
    set: {
      slides: [
        { text: 'Welcome to our newest consultants.', image: '/wormhole/tiles/p26-f1-1.jpg' },
        {
          text: 'Kyle Babcock, United States. Certified Soil Food Web Consultant.',
          image: '/wormhole/tiles/p26-f1-2.jpg',
        },
        {
          text: 'Joshua Stone, United States. Certified Soil Food Web Consultant.',
          image: '/wormhole/tiles/p26-f1-3.jpg',
        },
      ],
      visual_note:
        'Family: I, portrait. Brown cover with both faces, then one large round portrait per slide. Joshua Stone shows his initials until his photo arrives. Built with tools/wormhole-visuals/families.py.',
    },
    reason:
      'Restyled (Linnea, 24 Oct): the feed must vary, so neighbouring posts never share a style family (tools/wormhole-visuals/FEED-GUIDE.md). Nov 10 to 15 now run brand boxes, portrait, full-bleed photo, numbered steps, type only.',
  },
  {
    key: '2026-10-24 pl20261114 slides f1',
    post: 'pl20261114',
    set: {
      slides: [
        {
          text: 'Your fallen leaves can become fungal compost.',
          image: '/wormhole/tiles/pl20261114-f1-1.jpg',
        },
        {
          text: '1. Pack wet leaves into a wire cage or a bag with holes.',
          image: '/wormhole/tiles/pl20261114-f1-2.jpg',
        },
        {
          text: '2. Keep them damp. Fungi do the work, slowly.',
          image: '/wormhole/tiles/pl20261114-f1-3.jpg',
        },
        {
          text: '3. In 1 to 2 years you get dark, crumbly leaf mold.',
          image: '/wormhole/tiles/pl20261114-f1-4.jpg',
        },
        {
          text: '4. Use it as mulch or mix it into potting soil.',
          image: '/wormhole/tiles/pl20261114-f1-5.jpg',
        },
      ],
      visual_note:
        'Family: J, numbered steps. Big EB Garamond step numbers, a square photo with its credit on each slide. Built with tools/wormhole-visuals/families.py.',
    },
    reason:
      'Restyled (Linnea, 24 Oct): the feed must vary, so neighbouring posts never share a style family (tools/wormhole-visuals/FEED-GUIDE.md). Nov 10 to 15 now run brand boxes, portrait, full-bleed photo, numbered steps, type only.',
  },
  {
    key: '2026-10-24 pl20261115 slides f1',
    post: 'pl20261115',
    set: {
      slides: [
        {
          text: 'Imagine a world without earthworms.',
          image: '/wormhole/tiles/pl20261115-f1-1.jpg',
        },
        { text: 'It already exists.', image: '/wormhole/tiles/pl20261115-f1-2.jpg' },
        {
          text: 'Many northern North American forests evolved without them after the last Ice Age.',
          image: '/wormhole/tiles/pl20261115-f1-3.jpg',
        },
        {
          text: 'Introduced worms now eat through the leaf litter those forests depend on.',
          image: '/wormhole/tiles/pl20261115-f1-4.jpg',
        },
        {
          text: 'Even a good organism can be the wrong one in the wrong place.',
          image: '/wormhole/tiles/pl20261115-f1-5.jpg',
        },
      ],
      visual_note:
        'Family: G, type only. Reel, five cards, one statement each on a different flat brand colour. Built with tools/wormhole-visuals/families.py.',
    },
    reason:
      'Restyled (Linnea, 24 Oct): the feed must vary, so neighbouring posts never share a style family (tools/wormhole-visuals/FEED-GUIDE.md). Nov 10 to 15 now run brand boxes, portrait, full-bleed photo, numbered steps, type only.',
  },
  {
    key: '2026-10-24 p25 family note',
    post: 'p25',
    set: { visual_note: 'Family: A, brand boxes. Built with tools/wormhole-visuals/boxes.py.' },
    reason: 'Style family recorded (24 Oct), per tools/wormhole-visuals/FEED-GUIDE.md.',
  },
  {
    key: '2026-10-24 d26 family note',
    post: 'd26',
    set: { visual_note: 'Family: A, brand boxes. Built with tools/wormhole-visuals/d26_rain.py.' },
    reason: 'Style family recorded (24 Oct), per tools/wormhole-visuals/FEED-GUIDE.md.',
  },
  {
    key: '2026-10-24 pl20261114 slides f2',
    post: 'pl20261114',
    set: {
      slides: [
        {
          text: 'Your fallen leaves can become fungal compost.',
          image: '/wormhole/tiles/pl20261114-f2-1.jpg',
        },
        {
          text: '1. Pack wet leaves into a wire cage or a bag with holes.',
          image: '/wormhole/tiles/pl20261114-f2-2.jpg',
        },
        {
          text: '2. Keep them damp. Fungi do the work, slowly.',
          image: '/wormhole/tiles/pl20261114-f2-3.jpg',
        },
        {
          text: '3. In 1 to 2 years you get dark, crumbly leaf mold.',
          image: '/wormhole/tiles/pl20261114-f2-4.jpg',
        },
        {
          text: '4. Use it as mulch or mix it into potting soil.',
          image: '/wormhole/tiles/pl20261114-f2-5.jpg',
        },
      ],
    },
    reason:
      "Re-spaced (Linnea, 24 Oct: 'fix the spacing'): the instruction text no longer runs into the photo. Layout measured from the glyphs, with a clear gap between number, text and photo. Same photos and credits. Family: J, numbered steps.",
  },
  {
    key: '2026-10-24 dated d05',
    post: 'd05',
    set: { iso_date: '2026-10-26', date_tbd: false },
    reason:
      'Dated Mon 26 Oct (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Mentors go out in October and November, one a day, as early as possible.',
  },
  {
    key: '2026-10-24 dated d11',
    post: 'd11',
    set: { iso_date: '2026-10-27', date_tbd: false },
    reason:
      'Dated Tue 27 Oct (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Mentors go out in October and November, one a day, as early as possible.',
  },
  {
    key: '2026-10-24 dated d12',
    post: 'd12',
    set: { iso_date: '2026-10-28', date_tbd: false },
    reason:
      'Dated Wed 28 Oct (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Mentors go out in October and November, one a day, as early as possible.',
  },
  {
    key: '2026-10-24 dated d13',
    post: 'd13',
    set: { iso_date: '2026-10-29', date_tbd: false },
    reason:
      'Dated Thu 29 Oct (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Mentors go out in October and November, one a day, as early as possible.',
  },
  {
    key: '2026-10-24 dated d10',
    post: 'd10',
    set: { iso_date: '2026-10-29', date_tbd: false },
    reason:
      'Dated Thu 29 Oct (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December.',
  },
  {
    key: '2026-10-24 dated d06',
    post: 'd06',
    set: { iso_date: '2026-10-30', date_tbd: false },
    reason:
      'Dated Fri 30 Oct (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December.',
  },
  {
    key: '2026-10-24 dated d24',
    post: 'd24',
    set: { iso_date: '2026-11-01', date_tbd: false },
    reason:
      'Dated Sun 1 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December.',
  },
  {
    key: '2026-10-24 dated sh-w1-01',
    post: 'sh-w1-01',
    set: { iso_date: '2026-11-01', date_tbd: false },
    reason:
      'Dated Sun 1 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Caption still to write before it goes out.',
  },
  {
    key: '2026-10-24 dated d21',
    post: 'd21',
    set: { iso_date: '2026-11-03', date_tbd: false },
    reason:
      'Dated Tue 3 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December.',
  },
  {
    key: '2026-10-24 dated d22',
    post: 'd22',
    set: { iso_date: '2026-11-05', date_tbd: false },
    reason:
      'Dated Thu 5 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December.',
  },
  {
    key: '2026-10-24 dated sh-w1-02',
    post: 'sh-w1-02',
    set: { iso_date: '2026-11-05', date_tbd: false },
    reason:
      'Dated Thu 5 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Caption still to write before it goes out.',
  },
  {
    key: '2026-10-24 dated d26',
    post: 'd26',
    set: { iso_date: '2026-11-06', date_tbd: false },
    reason:
      'Dated Fri 6 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December.',
  },
  {
    key: '2026-10-24 dated sh-w1-03',
    post: 'sh-w1-03',
    set: { iso_date: '2026-11-10', date_tbd: false },
    reason:
      'Dated Tue 10 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Caption still to write before it goes out.',
  },
  {
    key: '2026-10-24 dated d23',
    post: 'd23',
    set: { iso_date: '2026-11-13', date_tbd: false },
    reason:
      'Dated Fri 13 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December.',
  },
  {
    key: '2026-10-24 dated sh-w1-04',
    post: 'sh-w1-04',
    set: { iso_date: '2026-11-13', date_tbd: false },
    reason:
      'Dated Fri 13 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Caption still to write before it goes out.',
  },
  {
    key: '2026-10-24 dated ss-01-li',
    post: 'ss-01-li',
    set: { iso_date: '2026-11-20', date_tbd: false },
    reason:
      "Dated Fri 20 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Evan's shares go out in November at the latest; this is the LinkedIn version beside the Instagram post.",
  },
  {
    key: '2026-10-24 dated ss-02-li',
    post: 'ss-02-li',
    set: { iso_date: '2026-11-22', date_tbd: false },
    reason:
      "Dated Sun 22 Nov (Linnea, 24 Oct): every undated post gets a date, sooner rather than later, and nothing waiting goes to December. Evan's shares go out in November at the latest; this is the LinkedIn version beside the Instagram post.",
  },
  {
    key: '2026-10-24 new x20261108',
    post: 'x20261108',
    create: {
      iso_date: '2026-11-08',
      date_tbd: false,
      topic: 'Diwali: a festival of light, from the soil up',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Happy Diwali to our students, mentors and partners in India, and to everyone celebrating around the world. \ud83e\ude94\n\nThe lamps are filled with oil from seeds, the sweets with grain, milk and sugarcane, and the doorways are hung with marigolds. Every one of them started in living soil.\n\nMay your fields, gardens and compost piles be full of light and life this year.\n\n#HappyDiwali #Diwali2026 #SoilFoodWeb #LivingSoil #SFWIndia',
      slides: [
        { text: 'Happy Diwali.', image: null },
        {
          text: 'Light, sweets and marigolds. Every one of them starts in living soil.',
          image: null,
        },
      ],
      cta: '',
      link: '',
      sources: ['https://www.awarenessdays.com/awareness-days-calendar/diwali'],
      visual_note:
        'No visual yet. Single image. Marigolds and a clay diya on dark soil, warm and simple. Our own India workshop photo if Kavi has one.',
      note: 'Diwali is Sun 8 Nov 2026 (Lakshmi Puja). Greeting post for the India community.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261109',
    post: 'x20261109',
    create: {
      iso_date: '2026-11-09',
      date_tbd: false,
      topic: 'COP31 opens in Antalya: where is soil?',
      platform: 'LinkedIn',
      caption:
        "COP31 opens today in Antalya, T\u00fcrkiye, and runs to 20 November.\n\nOne thing to watch: the Sharm el-Sheikh Joint Work on agriculture and food security, the UN climate talks' own track for farming, closed at COP30 without an outcome, and its mandate ends in 2026. What replaces it decides whether soil gets a real place in climate policy for the next decade.\n\nSoil is the largest carbon store on land. Its biology decides how much of that carbon stays put: fungi and bacteria build the aggregates that lock carbon away, and tillage breaks them open.\n\nWe'll be following the agriculture negotiations over the next two weeks.\n\n#COP31 #SoilHealth #ClimateAction #RegenerativeAgriculture #SoilFoodWeb",
      slides: [
        {
          text: "COP31 opens today. Agriculture's own negotiating track runs out in 2026.",
          image: null,
        },
      ],
      cta: '',
      link: 'https://en.wikipedia.org/wiki/2026_United_Nations_Climate_Change_Conference',
      sources: [
        'https://en.wikipedia.org/wiki/2026_United_Nations_Climate_Change_Conference',
        'https://consciousplanet.org/en/save-soil/news/cop30-a-turning-point-for-climate-action-but-agriculture-and-soils-left-behind',
      ],
      visual_note:
        'No visual yet. LinkedIn single image, 1200 x 627. One strong line of type on a flat brand colour.',
      note: 'COP31: 9 to 20 Nov 2026, Antalya Expo Center. LinkedIn only; the Instagram feed has the nematode numbers post that day.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261117',
    post: 'x20261117',
    create: {
      iso_date: '2026-11-17',
      date_tbd: false,
      topic: 'Permaculture: the three ethics',
      platform: 'Instagram, Facebook',
      caption:
        'Before a single bed is drawn, every permaculture design answers to three ethics. \ud83c\udf0d\n\nEarth care: leave the land more alive than you found it.\nPeople care: design for the people who live and work there.\nFair share: take what you need and return the surplus.\n\nBill Mollison and David Holmgren set them down in the 1970s, and they still decide every choice in a design. Living soil serves all three: it grows the food, it holds the water, and the compost you make from your surplus goes straight back into it.\n\nOur Permaculture Design Certificate cohort is working through them right now.\n\n#Permaculture #PermacultureEthics #EarthCare #SoilFoodWeb #PermacultureDesign',
      slides: [
        { text: 'Every permaculture design starts with three ethics.', image: null },
        { text: 'Earth care.', image: null },
        { text: 'People care.', image: null },
        { text: 'Fair share.', image: null },
        { text: 'Living soil serves all three.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        "No visual yet. Carousel, 5 slides. Type and drawn icons on flat brand colours, or real photos of a student's design site.",
      note: 'Permaculture series. LinkedIn already has the Save Soil tillage post that day, so this one is Instagram and Facebook.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261118',
    post: 'x20261118',
    create: {
      iso_date: '2026-11-18',
      date_tbd: false,
      topic: 'Compost Intensive Course: the January cohort',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Most compost guides stop at the recipe. Ours ends at the microscope. \ud83d\udd2c\n\nThe Compost Intensive Course is ten weeks of building your own thermal compost, tracking its temperature, and checking under the microscope whether the biology you wanted is really there, with our mentors guiding you each week.\n\nThe next cohort starts in January 2027. Enroll through the link in bio.\n\n#CompostIntensive #Compost #ThermalCompost #SoilFoodWeb #SoilMicroscopy',
      slides: [
        { text: 'Ten weeks to make compost you can prove.', image: null },
        { text: 'Compost Intensive Course, starting January 2027.', image: null },
        { text: 'Build, monitor and read your own piles under the microscope.', image: null },
        { text: 'With mentors every week.', image: null },
        { text: 'Enroll now, link in bio.', image: null },
      ],
      cta: 'Enroll, link in bio',
      link: '[CIC enrollment page]',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 5 slides. Students building and checking piles, a thermometer, a microscope view of compost, real workshop photos.',
      note: 'Promo calendar: CIC promo period 19 Oct to 30 Nov, cohort runs from the week of 18 Jan 2027 (10 weeks). Confirm the start date and enrollment link with Stephanie.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261125',
    post: 'x20261125',
    create: {
      iso_date: '2026-11-25',
      date_tbd: false,
      topic: 'Foundation Courses: start any time',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Winter is the best time to learn what your soil needs before spring. \u2744\ufe0f\n\nOur Foundation Courses take you through Dr. Elaine Ingham's soil food web science, how to make biologically complete compost, extracts and teas, and how to read soil under the microscope. You study at your own pace, from anywhere, and start whenever you're ready.\n\nMore than 10,000 people in over 100 countries have started here.\n\nLink in bio.\n\n#FoundationCourses #SoilFoodWeb #DrElaineIngham #OnlineLearning #SoilHealth",
      slides: [
        { text: 'Start learning the soil food web this winter.', image: null },
        { text: 'The Foundation Courses: at your own pace, from anywhere.', image: null },
        { text: 'The science, the compost, the extracts and teas, the microscope.', image: null },
        { text: '10,000+ people in 100+ countries have started here.', image: null },
      ],
      cta: 'Start learning, link in bio',
      link: 'https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses',
      sources: ['https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses'],
      visual_note:
        'No visual yet. Carousel, 4 slides. Course screenshots and real student microscope photos.',
      note: 'Promo calendar: Foundation Courses promo period 19 Oct to 30 Nov. The 10,000+ and 100+ countries figures are the Foundation facts in the content guide. Allison: check the course list wording.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261128',
    post: 'x20261128',
    create: {
      iso_date: '2026-11-28',
      date_tbd: false,
      topic: 'Small Business Saturday: hire a local soil consultant',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "It's Small Business Saturday, and the soil has small businesses too. \ud83e\uddd1\u200d\ud83c\udf3e\n\nOur certified Soil Food Web Consultants are independent business owners. They read your soil under the microscope, build biologically complete compost, and walk your fields with you to plan what comes next.\n\nHiring one near you keeps the money local and the advice fitted to your soil, climate and crops.\n\nFind a consultant in our directory, link in bio.\n\n#SmallBusinessSaturday #ShopLocal #SoilConsultant #SoilFoodWeb #SoilHealth",
      slides: [
        { text: 'Small Business Saturday.', image: null },
        { text: 'Shop local for your soil too.', image: null },
        {
          text: 'Certified Soil Food Web Consultants run their own businesses: labs, compost operations and on-farm advice.',
          image: null,
        },
        { text: 'Find one near you.', image: null },
      ],
      cta: 'Find a consultant, link in bio',
      link: 'https://soilfoodweb.com [consultant directory URL]',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 4 slides. A consultant at the microscope or in a field, real photos from consultants who agree to be featured.',
      note: 'Small Business Saturday is the Saturday after US Thanksgiving (26 Nov 2026). Same directory link as p23 on 6 Nov.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261129',
    post: 'x20261129',
    create: {
      iso_date: '2026-11-29',
      date_tbd: false,
      topic: 'Permaculture: plant a fruit tree guild',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'In permaculture, a fruit tree is never planted alone. \ud83c\udf4e\n\nA guild is a small community of plants around one tree. White clover under the canopy fixes nitrogen with its rhizobia. Comfrey grows fast and gets cut and dropped as mulch several times a year. Chives and other alliums fill the gaps. The ground stays covered, roots stay living all year, and the soil food web around the tree has a steady supply of food.\n\nPlan yours this winter and plant it in spring.\n\n\ud83d\udcbe Save this for planting season.\n\n#Permaculture #FruitTreeGuild #FoodForest #SoilFoodWeb #CompanionPlanting',
      slides: [
        { text: 'A fruit tree grows better with friends.', image: null },
        { text: 'Clover underneath fixes nitrogen.', image: null },
        { text: 'Comfrey gets cut and dropped as mulch.', image: null },
        { text: 'Chives and other alliums fill the gaps.', image: null },
        { text: 'Together they keep the soil covered and alive.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 5 slides. A drawn guild plan from above, then real photos of each plant.',
      note: 'Permaculture series. Avoid claims that comfrey mines minerals from deep soil; keep it to mulch.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261130',
    post: 'x20261130',
    create: {
      iso_date: '2026-11-30',
      date_tbd: false,
      topic: 'Compost Intensive Course: last week of the promo',
      platform: 'Instagram, Facebook',
      caption:
        'If one of your goals for 2027 is compost you can trust, this is the course. \ud83c\udf21\ufe0f\n\nIn the Compost Intensive Course you build your own thermal piles, hold them between 131 and 155\u00b0F, and check the result under the microscope with a mentor, week by week for ten weeks.\n\nThe January cohort is enrolling now. Link in bio.\n\n#CompostIntensive #Compost #SoilFoodWeb #NewYearGoals',
      slides: [
        { text: 'Your compost, checked under the microscope.', image: null },
        { text: 'The Compost Intensive Course starts in January.', image: null },
        { text: 'Enroll now, link in bio.', image: null },
      ],
      cta: 'Enroll, link in bio',
      link: '[CIC enrollment page]',
      sources: [],
      visual_note:
        'No visual yet. Single image. Full-bleed photo of a steaming pile with a thermometer in it.',
      note: 'Promo calendar: last day of the CIC promo period. Instagram and Facebook; LinkedIn has the McKeon reshare that day.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261201',
    post: 'x20261201',
    create: {
      iso_date: '2026-12-01',
      date_tbd: false,
      topic: 'GivingTuesday: fund a scholarship',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Today is GivingTuesday, and one gift can reach a whole community. \ud83d\udc9a\n\nOur scholarships put farmers, gardeners and students into Soil Food Web courses they couldn't otherwise afford. They learn to read soil under the microscope and make biologically complete compost, then take it home to their own farms and teach the people around them.\n\n[One line from a scholarship recipient, with their permission and handle.]\n\nEvery gift today goes to scholarships. Give through the link in bio.\n\n#GivingTuesday #Scholarships #SoilFoodWeb #Nonprofit #SoilHealth",
      slides: [
        { text: 'Today is GivingTuesday.', image: null },
        {
          text: "A scholarship puts a farmer, gardener or student in a course they couldn't otherwise take.",
          image: null,
        },
        { text: 'They take it home to their own soil, and teach their neighbours.', image: null },
        { text: 'Give today, link in bio.', image: null },
      ],
      cta: 'Give today, link in bio',
      link: '[Givebutter donate link]',
      sources: ['https://www.givingtuesday.org/'],
      visual_note:
        "No visual yet. Carousel, 4 slides. A scholarship recipient's own photo (permission given, handles in the spreadsheet), with their words.",
      note: 'GivingTuesday 2026 is Tue 1 Dec, the Tuesday after US Thanksgiving. Confirm with Stephanie that gifts go to scholarships and get the Givebutter link.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261202',
    post: 'x20261202',
    create: {
      iso_date: '2026-12-02',
      date_tbd: false,
      topic: 'From shovel to slide: how we read a soil sample',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'One drop of soil and water can tell you what your soil needs next. \ud83d\udd2c\n\nThis is the method our students learn: take a small sample from the root zone, mix it with water, put a single drop on a slide and look. Under the microscope you count the organisms that run the soil food web, the bacteria, fungal hyphae, protozoa and nematodes, and compare the numbers with what your plants need.\n\nA garden bed and an orchard want very different biology, and the microscope shows you which one you have.\n\nLearn to do it yourself in our Foundation Courses, link in bio.\n\n#SoilMicroscopy #SoilFoodWeb #SoilTesting #SoilBiology #Microscope',
      slides: [
        { text: 'From shovel to slide.', image: null },
        { text: '1. Take a small sample from the root zone.', image: null },
        { text: '2. Mix it with water.', image: null },
        { text: '3. Put one drop on a slide.', image: null },
        { text: '4. Count what you see: bacteria, fungi, protozoa, nematodes.', image: null },
        { text: 'That count tells you what your soil needs.', image: null },
      ],
      cta: 'Learn it, link in bio',
      link: 'https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses',
      sources: ['https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses'],
      visual_note:
        'No visual yet. Carousel, 6 slides. Real photos of each step from our own workshops, ending on a microscope library photo.',
      note: 'Process post. Allison: check the dilution wording against the course before approval.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261203',
    post: 'x20261203',
    create: {
      iso_date: '2026-12-03',
      date_tbd: false,
      topic: 'Costa Rica: six weeks to go',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Six weeks from now, our next Accelerator Workshop starts in Costa Rica. \ud83c\udf3f\n\n18 to 29 January 2027: twelve days of building compost piles with your hands in the morning and reading them under the microscope in the afternoon, with mentors beside you the whole time.\n\nPlaces are still open. Register through the link in bio.\n\n#CostaRica #AcceleratorWorkshop #Compost #SoilFoodWeb #Workshop',
      slides: [
        { text: 'Six weeks to Costa Rica.', image: null },
        { text: '18 to 29 January 2027.', image: null },
        { text: 'Compost piles in the morning, the microscope in the afternoon.', image: null },
        { text: 'Places are still open.', image: null },
      ],
      cta: 'Register, link in bio',
      link: 'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      sources: [
        'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'No visual yet. Single image or short carousel. Full-bleed photo from a past Costa Rica workshop.',
      note: 'Promo. Check with Stephanie that places are open before it goes out; dates from the Costa Rica sales page.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261204',
    post: 'x20261204',
    create: {
      iso_date: '2026-12-04',
      date_tbd: false,
      topic: 'Wildlife Conservation Day: the wildlife under your feet',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Today is World Wildlife Conservation Day, so meet the wildlife living under your feet. \ud83d\udc3e\n\nBacteria and fungi feed on what roots release and on dead plant material. Protozoa and nematodes eat the bacteria and fungi, and release the nutrients plants take up. Springtails and mites shred, graze and carry spores around.\n\nTheir habitat is the pores and crumbs of living soil. Keep the ground covered, keep roots growing, and dig as little as you can, and every one of them has somewhere to live.\n\nAll photos from our students' microscopes.\n\n#WildlifeConservationDay #SoilBiology #SoilFoodWeb #Microscopy #Biodiversity",
      slides: [
        { text: 'Wildlife Conservation Day.', image: null },
        { text: 'Meet the wildlife under your feet.', image: null },
        { text: 'Bacteria.', image: null },
        { text: 'Fungi.', image: null },
        { text: 'Protozoa.', image: null },
        { text: 'Nematodes.', image: null },
        { text: 'Microarthropods.', image: null },
        { text: 'Protect their habitat: keep soil covered and roots growing.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 8 slides. One microscope library photo per group, credited by name (Microbe library in the Worms and soil Drive folder).',
      note: 'World Wildlife Conservation Day is 4 December.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261208',
    post: 'x20261208',
    create: {
      iso_date: '2026-12-08',
      date_tbd: false,
      topic: 'Soil food web 101: who eats whom',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Your plants are farmers, and the soil food web is how they get paid. \ud83c\udf3e\n\nRoots leak sugars and proteins into the soil around them. Bacteria and fungi gather to eat them and lock up nitrogen and other nutrients in their bodies. Then protozoa and nematodes eat the bacteria and fungi, keep what they need, and release the rest right next to the root, in a form the plant can take up.\n\nTake out one link in that chain, with tillage, compaction or bare soil, and the plant goes hungry no matter how much is in the ground.\n\n\ud83d\udcbe Save this one.\n\n#SoilFoodWeb #NutrientCycling #SoilBiology #RegenerativeAgriculture #DrElaineIngham',
      slides: [
        { text: 'Who eats whom in your soil?', image: null },
        { text: 'Plants feed bacteria and fungi through their roots.', image: null },
        { text: 'Protozoa and nematodes eat the bacteria and fungi.', image: null },
        { text: "What they don't need comes out as nutrients plants can take up.", image: null },
        { text: 'Lose a link, and the plant goes hungry.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 5 slides. A simple drawn diagram on flat brand colour, one link of the chain per slide.',
      note: 'Core SFW teaching, no outside source needed.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261210',
    post: 'x20261210',
    create: {
      iso_date: '2026-12-10',
      date_tbd: false,
      topic: 'Soil in numbers: 131 to 155\u00b0F',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Thermal compost has a sweet spot, and a thermometer is the cheapest tool you'll own. \ud83c\udf21\ufe0f\n\nDr. Elaine Ingham's method holds the pile at 131\u00b0F (55\u00b0C) for at least three full days, long enough to kill weed seeds, pathogens and pests. But keep it below 155 to 160\u00b0F (68 to 71\u00b0C): go hotter and the beneficial bacteria and fungi you're trying to grow die with the weeds.\n\nWhen the temperature climbs too high too fast, turn the pile. Most piles need three to five turns.\n\n\ud83d\udcbe Save this for your next build.\n\n#ThermalCompost #Compost #SoilFoodWeb #DrElaineIngham #CompostTips",
      slides: [
        { text: '131\u00b0F (55\u00b0C).', image: null },
        { text: 'Hold it for 3 days to kill weed seeds and pathogens.', image: null },
        { text: 'Keep it under 155 to 160\u00b0F (68 to 71\u00b0C).', image: null },
        { text: 'Hotter, and the beneficial organisms die too.', image: null },
        { text: 'Turn the pile when it climbs too high, too fast.', image: null },
      ],
      cta: '',
      link: 'https://practicalfarmers.org/wp-content/uploads/2019/05/Ingham-Compost.pdf',
      sources: ['https://practicalfarmers.org/wp-content/uploads/2019/05/Ingham-Compost.pdf'],
      visual_note:
        'No visual yet. Single image or short carousel. A compost thermometer in a steaming pile, our own workshop photo.',
      note: "Figures from Dr. Elaine Ingham's compost presentation (Practical Farmers of Iowa copy). Celsius conversions ours.",
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261213',
    post: 'x20261213',
    create: {
      iso_date: '2026-12-13',
      date_tbd: false,
      topic: 'Read the drop: testate amoebae, protozoa with a shell',
      platform: 'Instagram Reel',
      caption:
        "This amoeba carries its house with it. \ud83d\udc1a\n\nTestate amoebae are protozoa that build a shell, called a test, either from their own secretions or from tiny mineral grains they glue together. They push their pseudopods out of a single opening to catch bacteria, and like other protozoa they release the nutrients they don't need right where roots can take them up.\n\nSpot one on your slide and you've found one of the oldest groups of soil life we know.\n\n#ReadTheDrop #TestateAmoeba #Protozoa #SoilMicroscopy #SoilFoodWeb",
      slides: [
        { text: 'This amoeba lives in a house it built.', image: null },
        {
          text: 'Testate amoebae make a shell from their own secretions or from grains of mineral.',
          image: null,
        },
        { text: 'They eat bacteria and release nutrients plants can use.', image: null },
        { text: 'Lots of them usually means a wetter, fungal-rich soil.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Reel, 15 to 20 seconds. Testate amoeba from the microbe library (Luke Hardy, 40x).',
      note: 'Read the drop series. Allison or a mentor: check slide 4 before approval.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261215',
    post: 'x20261215',
    create: {
      iso_date: '2026-12-15',
      date_tbd: false,
      topic: 'Year-end giving: what a scholarship becomes',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "A scholarship never stays with one person. \ud83d\udc9a\n\nOne course becomes one farm that builds compost and stops fighting its soil. Then a neighbour sees the difference over the fence, and asks how.\n\n[One real example from the impact story sheet, with the person's permission and handle.]\n\nIf you'd like to give before the year ends, every gift goes to scholarships. Link in bio.\n\n#YearEndGiving #Scholarships #SoilFoodWeb #Nonprofit #SoilRegenerators",
      slides: [
        { text: 'What does one scholarship become?', image: null },
        { text: 'One course.', image: null },
        { text: 'One farm that changes how it builds soil.', image: null },
        { text: 'A neighbour who sees the difference.', image: null },
        { text: 'Give before the year ends, link in bio.', image: null },
      ],
      cta: 'Give, link in bio',
      link: '[Givebutter donate link]',
      sources: [],
      visual_note:
        "No visual yet. Carousel, 5 slides. One scholarship recipient's own field photos, before and after where they exist.",
      note: 'December year-end giving, per the social media SOP: short and honest. Use a recipient from the impact story sheet.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261216',
    post: 'x20261216',
    create: {
      iso_date: '2026-12-16',
      date_tbd: false,
      topic: 'Permaculture: zones, and where the compost goes',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Where should the compost bin go? Permaculture has an answer. \ud83d\uddfa\ufe0f\n\nA design is laid out in zones by how often you visit. Zone 0 is the house. Zone 1 is what you touch every day: herbs, salad greens and the compost bin, so the kitchen scraps make it there and you notice when the pile needs turning. Zones 2 to 4 move out through orchard, field, pasture and woodlot. Zone 5 is left wild, where you go to watch and learn.\n\nPut the compost where you'll walk past it.\n\n\ud83d\udcbe Save this before you plan next year's garden.\n\n#Permaculture #PermacultureZones #GardenDesign #Compost #SoilFoodWeb",
      slides: [
        { text: 'Permaculture zones.', image: null },
        { text: 'Zone 0: the house.', image: null },
        { text: 'Zone 1: what you visit every day. Herbs, salad, the compost bin.', image: null },
        { text: 'Zones 2 to 4: orchard, field, pasture, woodlot.', image: null },
        { text: 'Zone 5: left wild.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 5 slides. A simple drawn zone map of rings around a house, one zone per slide.',
      note: 'Permaculture series.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261217',
    post: 'x20261217',
    create: {
      iso_date: '2026-12-17',
      date_tbd: false,
      topic: 'Science explained: nitrogen from thin air',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "The air around every plant is 78% nitrogen, and plants can't touch any of it. \ud83c\udf31\n\nNitrogen gas is locked by one of the strongest bonds in chemistry. Rhizobium and Bradyrhizobium bacteria break it inside the root nodules of beans, peas and clover, and hand the plant nitrogen it can use. In return the plant feeds them sugar.\n\nBiological nitrogen fixation supplies 25 to 40% of the world's annual reactive nitrogen and 10 to 20% of what cultivated crops need (Coyne & Mikkelsen 2015, via Save Soil).\n\nSplit open a pink nodule on a pea root this spring: the colour comes from leghemoglobin, which keeps oxygen away from the enzyme that does the work.\n\n\ud83d\udcbe Save this for planting season.\n\n#NitrogenFixation #Rhizobia #SoilBiology #SoilFoodWeb #CoverCrops",
      slides: [
        { text: 'Nitrogen from thin air.', image: null },
        { text: "Air is 78% nitrogen gas. Plants can't use it.", image: null },
        { text: 'Rhizobia bacteria in legume roots turn it into a form plants can.', image: null },
        {
          text: "Biological fixation supplies 25 to 40% of the world's yearly reactive nitrogen.",
          image: null,
        },
        { text: 'No bag required.', image: null },
      ],
      cta: '',
      link: 'https://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans',
      sources: ['https://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans'],
      visual_note:
        'No visual yet. Carousel, 5 slides. Root nodules on a legume root (openly licensed photo with credit), then a simple drawn diagram of air to nodule to plant.',
      note: 'Figures from the Save Soil paper Healthy Soil and Healthy Humans, citing Coyne & Mikkelsen 2015. Air is 78% nitrogen by volume.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261220',
    post: 'x20261220',
    create: {
      iso_date: '2026-12-20',
      date_tbd: false,
      topic: 'Congratulations to our PDC cohort',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Congratulations to everyone finishing our Permaculture Design Certificate this week! \ud83c\udf89\n\nTwelve weeks ago you started with a blank map. Now each of you has a full design for a real place, built on living soil from the ground up.\n\n[One or two designs, with the students' permission.]\n\nWe are so proud of you. Go plant it.\n\n#PermacultureDesign #PDC #Permaculture #SoilFoodWeb #Graduation",
      slides: [
        { text: 'Congratulations to our Permaculture Design Certificate cohort.', image: null },
        { text: 'Twelve weeks, one design each.', image: null },
        { text: "We can't wait to see what you build.", image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        "No visual yet. Carousel. Students' own design drawings or site photos, with permission.",
      note: 'PDC cohort runs 16 Sep to 20 Dec 2026 (from the website audit). Confirm the end date with Kavi before it goes out.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261222',
    post: 'x20261222',
    create: {
      iso_date: '2026-12-22',
      date_tbd: false,
      topic: "Holiday reading: Dr. Elaine's papers",
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Looking for something to read between the holidays? \u2615\n\nDr. Elaine Ingham's published research is now gathered in one place on our website: 77 journal papers, 6 book chapters and 10 EPA and technical reports, each linked to where you can read it.\n\nPick one, pour a coffee, and spend an afternoon with the science behind everything we teach.\n\nLink in bio.\n\n#DrElaineIngham #SoilScience #HolidayReading #SoilFoodWeb #Research",
      slides: [
        { text: 'Holiday reading.', image: null },
        { text: "Four decades of Dr. Elaine Ingham's research, linked in one place.", image: null },
        { text: 'Start with one. Pour a coffee.', image: null },
      ],
      cta: 'Read them, link in bio',
      link: 'https://soilfoodweb.com [publications URL]',
      sources: [],
      visual_note:
        'No visual yet. Single image. Type on a flat brand colour, or a coffee cup beside a printed paper.',
      note: 'Follows the 10 Nov publications page post.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261224',
    post: 'x20261224',
    create: {
      iso_date: '2026-12-24',
      date_tbd: false,
      topic: 'After the holidays: turn your tree into fungal mulch',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'When the decorations come down, your tree still has one more gift to give. \ud83c\udf84\n\nChipped conifer branches make a woody mulch that fungi love. Spread it around trees, shrubs and perennial beds, where fungal-dominated soil suits the plants best, and it keeps the ground covered while it slowly breaks down.\n\nMany towns collect trees in January and chip them for free. Ask yours, and ask for some chips back.\n\n\ud83d\udcbe Save this for January.\n\n#ChristmasTree #Mulch #Compost #SoilFoodWeb #FungalSoil',
      slides: [
        { text: 'Your Christmas tree has one more job.', image: null },
        { text: 'Chip it, or ask if your town does.', image: null },
        { text: 'Woody mulch feeds fungi.', image: null },
        { text: 'Spread it around trees and shrubs.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 4 slides. A pile of chipped conifer, mulch around a young tree, real photos with credits.',
      note: '',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261226',
    post: 'x20261226',
    create: {
      iso_date: '2026-12-26',
      date_tbd: false,
      topic: 'What wrapping paper can go in the compost?',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "The morning after the presents, the compost pile asks: what can I have? \ud83c\udf81\n\nPlain paper and cardboard boxes, shredded or torn small, are carbon your pile can use. Glossy, foil, glitter or plastic-coated paper isn't: it won't break down and it leaves bits in your finished compost. Pull the tape and ribbons off first.\n\nA quick test: scrunch it. If it stays scrunched, it's usually plain paper. If it springs back, leave it out.\n\n#BoxingDay #Compost #ZeroWaste #SoilFoodWeb #CompostTips",
      slides: [
        { text: 'Can wrapping paper go in the compost?', image: null },
        { text: 'Plain paper and cardboard: yes, shredded.', image: null },
        { text: 'Glossy, foil, glitter or plastic-coated: no.', image: null },
        { text: 'Tape and ribbons off first.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 4 slides. Shredded brown paper and boxes next to a compost bin, real photos.',
      note: '',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261227',
    post: 'x20261227',
    create: {
      iso_date: '2026-12-27',
      date_tbd: false,
      topic: 'Permaculture: chop and drop',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'The laziest mulch in permaculture is also one of the best. \u2702\ufe0f\n\nChop and drop means cutting plants back and leaving the cuttings right where they fall: comfrey, cover crops, prunings, spent annuals. The layer shades the soil, keeps moisture in, and slowly feeds the fungi and bacteria underneath. The roots you left in the ground decompose too, leaving channels for air and water.\n\nNo wheelbarrow, no bare ground.\n\n#ChopAndDrop #Permaculture #Mulch #SoilFoodWeb #NoDig',
      slides: [
        { text: 'Chop and drop.', image: null },
        { text: 'Cut the plant. Leave it where it falls.', image: null },
        { text: 'It shades the soil and feeds the fungi and bacteria underneath.', image: null },
        { text: 'No hauling, no bare ground.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 4 slides. Real photos of cut comfrey or cover crop lying as mulch.',
      note: 'Permaculture series.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261229',
    post: 'x20261229',
    create: {
      iso_date: '2026-12-29',
      date_tbd: false,
      topic: '2026 in soil science: discoveries we loved',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "2026 was a good year for soil science, and these are the discoveries we kept talking about. \ud83d\udd2c\n\n1. University of Sheffield researchers showed that Arabidopsis, a mustard plant everyone believed could not partner with fungi, trades nutrients with an ancient soil fungus (Current Biology).\n2. BeOpen, by Biome Makers, opened an atlas of the bacteria and fungi in more than 100,000 soil samples from over 90 countries, all analysed the same way.\n3. Save Soil gathered the evidence for soil biology as a climate adaptation indicator, including regenerative almond orchards where water soaked in six times faster with the same yield (LaCanne et al.).\n\nHere's to more in 2027.\n\n#SoilScience #YearInReview #SoilBiology #SoilFoodWeb #Research",
      slides: [
        { text: '2026 in soil science.', image: null },
        {
          text: "A mustard plant that 'couldn't' partner with fungi traded food with one.",
          image: null,
        },
        { text: 'An open map of the bacteria and fungi in 100,000 soil samples.', image: null },
        {
          text: 'Regenerative almond orchards: water soaked in 6x faster, same yield.',
          image: null,
        },
        { text: "Here's to more in 2027.", image: null },
      ],
      cta: '',
      link: '',
      sources: [
        'https://sheffield.ac.uk/biosciences/news/ancient-fungus-unlocks-secret-support-system-major-food-crops-could-transform-farming-practices',
        'https://beopen.earth/',
        'https://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga',
      ],
      visual_note:
        'No visual yet. Carousel, 5 slides. One image per discovery: the Sheffield root image (credit), the BeOpen atlas map (screenshot), an almond orchard.',
      note: "The LaCanne almond study is 2021; it appears here as part of Save Soil's 2025 synthesis.",
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 new x20261231',
    post: 'x20261231',
    create: {
      iso_date: '2026-12-31',
      date_tbd: false,
      topic: 'Happy New Year: our 2027 workshops',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Happy New Year from all of us at the Soil Food Web Foundation! \ud83c\udf86\n\nIn 2027 we're building compost and reading soil with you in three places:\n\nCosta Rica, 18 to 29 January\nNew Mexico, 3 to 14 May\nUnited Kingdom, September\n\nEvery workshop is twelve hands-on days with our mentors. See them all through the link in bio.\n\n#HappyNewYear #2027 #AcceleratorWorkshop #SoilFoodWeb #Workshops",
      slides: [
        { text: 'Happy New Year from the soil.', image: null },
        { text: 'Costa Rica, 18 to 29 January.', image: null },
        { text: 'New Mexico, 3 to 14 May.', image: null },
        { text: 'United Kingdom, September.', image: null },
        { text: 'Which one is yours?', image: null },
      ],
      cta: 'See the workshops, link in bio',
      link: 'https://soilfoodweb.com/workshops [VERIFY URL]',
      sources: [
        'https://school.soilfoodweb.com/courses/accelerator-workshop-costa-rica-january-2027',
      ],
      visual_note:
        'No visual yet. Carousel, 5 slides. One full photo per place, from past workshops there.',
      note: 'Dates from the workshop calendar; the UK dates (13 Sep to 1 Oct 2027) are unconfirmed, so the slide says September only. Confirm with Stephanie.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): towards seven posts a week, from holidays, global events, the 2027 promotions calendar and organic permaculture and soil science content.',
  },
  {
    key: '2026-10-24 unposted p02 to 2026-10-25',
    post: 'p02',
    set: { iso_date: '2026-10-25', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series restarts: Casey first, Sun 25 Oct.',
  },
  {
    key: '2026-10-24 unposted p03 to 2026-10-26',
    post: 'p03',
    set: { iso_date: '2026-10-26', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series, day 2.',
  },
  {
    key: '2026-10-24 unposted p04 to 2026-10-27',
    post: 'p04',
    set: { iso_date: '2026-10-27', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series, day 3.',
  },
  {
    key: '2026-10-24 unposted p06 to 2026-10-28',
    post: 'p06',
    set: { iso_date: '2026-10-28', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series, day 4.',
  },
  {
    key: '2026-10-24 unposted p09 to 2026-10-29',
    post: 'p09',
    set: { iso_date: '2026-10-29', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series, day 5.',
  },
  {
    key: '2026-10-24 unposted d05 to 2026-10-30',
    post: 'd05',
    set: { iso_date: '2026-10-30', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series, day 6.',
  },
  {
    key: '2026-10-24 unposted d11 to 2026-10-31',
    post: 'd11',
    set: { iso_date: '2026-10-31', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series, day 7.',
  },
  {
    key: '2026-10-24 unposted d12 to 2026-11-01',
    post: 'd12',
    set: { iso_date: '2026-11-01', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series, day 8.',
  },
  {
    key: '2026-10-24 unposted d13 to 2026-11-02',
    post: 'd13',
    set: { iso_date: '2026-11-02', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Mentor series, day 9.',
  },
  {
    key: '2026-10-24 unposted d14 to 2026-11-04',
    post: 'd14',
    set: { iso_date: '2026-11-04', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Never posted on 19 Oct; moved to Wed 4 Nov, a light day.',
  },
  {
    key: '2026-10-24 unposted p10 to 2026-11-09',
    post: 'p10',
    set: { iso_date: '2026-11-09', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Never posted on 22 Oct; moved to Mon 9 Nov, a light day, with its LinkedIn post d16.',
  },
  {
    key: '2026-10-24 unposted d16 to 2026-11-09',
    post: 'd16',
    set: { iso_date: '2026-11-09', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Never posted on 23 Oct; same day as the Instagram post p10.',
  },
  {
    key: '2026-10-24 unposted d27 to 2026-11-11',
    post: 'd27',
    set: { iso_date: '2026-11-11', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Never posted on 22 Oct; moved to Wed 11 Nov, a light day.',
  },
  {
    key: '2026-10-24 unposted promo-fall-bundle to 2026-11-12',
    post: 'promo-fall-bundle',
    set: { iso_date: '2026-11-12', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. Never posted on 20 Oct; moved to Thu 12 Nov, a light day. Caption still needed.',
  },
  {
    key: '2026-10-24 unposted p08 to 2027-10-21',
    post: 'p08',
    set: { iso_date: '2027-10-21', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. World Earthworm Day was 21 Oct and this was not posted; the caption is about the day itself, so it waits for World Earthworm Day 2027.',
  },
  {
    key: '2026-10-24 unposted d15 to 2027-10-21',
    post: 'd15',
    set: { iso_date: '2027-10-21', date_tbd: false },
    reason:
      'Linnea, Sat 24 Oct: nothing dated before today went out, and no mentor has been posted yet. World Earthworm Day story, not posted on 21 Oct; waits for World Earthworm Day 2027.',
  },
  {
    key: '2026-10-24 new w20261103',
    post: 'w20261103',
    create: {
      iso_date: '2026-11-03',
      date_tbd: false,
      topic: 'Website: a tour of our new website',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "We rebuilt our website from the ground up, and it's finally here. \ud83c\udf31\n\nEverything now lives in one place: every course and where to start, every workshop and event, past and coming, the consultant directory, and four decades of Dr. Elaine Ingham's research, linked paper by paper.\n\nTake a look around and tell us what you find. Link in bio.\n\n#SoilFoodWeb #NewWebsite #SoilHealth #LearnSoil",
      slides: [
        { text: 'Our new website is here.', image: null },
        { text: 'Learn: every course, and where to start.', image: null },
        { text: 'Workshops and events, past and coming.', image: null },
        { text: 'Find a consultant near you.', image: null },
        { text: "Dr. Elaine's research, all in one place.", image: null },
        { text: 'Take the tour, link in bio.', image: null },
      ],
      cta: 'Explore, link in bio',
      link: 'https://soilfoodweb.com [VERIFY URL]',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 6 slides. Real screenshots of each section of the new site, framed on flat brand colours.',
      note: 'Website series. Post once the new site is live at the main address; confirm with Alex.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): more posts about the new website and the coming annual report.',
  },
  {
    key: '2026-10-24 new w20261106',
    post: 'w20261106',
    create: {
      iso_date: '2026-11-06',
      date_tbd: false,
      topic: 'Website: projects from the field',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Our new Projects pages are where the science meets the field. \ud83c\udf3e\n\nEach one follows a real farm, vineyard or restoration site: what the soil looked like at the start, what they changed, and what happened next, with the photos and numbers to show it.\n\nRead them through the link in bio.\n\n#SoilFoodWeb #CaseStudy #RegenerativeAgriculture #SoilHealth',
      slides: [
        { text: 'What does living soil look like on a real farm?', image: null },
        { text: 'Our new Projects pages show you.', image: null },
        { text: 'Farms, vineyards and restoration sites.', image: null },
        { text: 'What they changed, and what happened.', image: null },
      ],
      cta: 'Read them, link in bio',
      link: 'https://soilfoodweb.com [VERIFY URL]',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 4 slides. Before and after photos from one project page.',
      note: 'Website series. Confirm the Projects section is live and which project to feature.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): more posts about the new website and the coming annual report.',
  },
  {
    key: '2026-10-24 new ar20261123',
    post: 'ar20261123',
    create: {
      iso_date: '2026-11-23',
      date_tbd: false,
      topic: 'Annual report: coming soon',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "One year in, we're putting it all on paper. \ud83d\udcd6\n\nOur first annual report is almost ready: the students who learned with us, the workshops on four continents, the scholarships you funded, and where the money went.\n\nWatch this space.\n\n#AnnualReport #SoilFoodWeb #Nonprofit #Transparency",
      slides: [
        { text: 'Our first annual report is almost here.', image: null },
        { text: 'A year of courses, workshops and scholarships.', image: null },
        { text: 'Coming soon.', image: null },
      ],
      cta: '',
      link: '',
      sources: [],
      visual_note:
        'No visual yet. Single image. Type on a flat brand colour, or a first look at the report cover.',
      note: 'Annual report series. Confirm the release date with Stephanie or Evan and adjust both posts; the four continents line needs checking against the report.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): more posts about the new website and the coming annual report.',
  },
  {
    key: '2026-10-24 new w20261206',
    post: 'w20261206',
    create: {
      iso_date: '2026-12-06',
      date_tbd: false,
      topic: 'Website: find your course in three questions',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Gardener, farmer, or future consultant: there's a path through our courses built for you. \ud83e\udded\n\nOur new website starts with one question, what brings you to the soil food web, and shows you which courses to take and in what order.\n\nFind your path through the link in bio.\n\n#SoilFoodWeb #LearnSoil #OnlineCourses #SoilHealth",
      slides: [
        { text: 'Not sure where to start?', image: null },
        { text: 'What brings you to the soil food web?', image: null },
        { text: "Gardener, farmer or future consultant: there's a path for you.", image: null },
        { text: 'Find yours, link in bio.', image: null },
      ],
      cta: 'Find your path, link in bio',
      link: 'https://soilfoodweb.com [VERIFY URL]',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 4 slides. The learning path cards from the website (Drive: "What brings you to the soil food web?" card images).',
      note: 'Website series.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): more posts about the new website and the coming annual report.',
  },
  {
    key: '2026-10-24 new ar20261208',
    post: 'ar20261208',
    create: {
      iso_date: '2026-12-08',
      date_tbd: false,
      topic: 'Annual report: our year in numbers',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Our first annual report is out. \ud83d\udcd6\n\n[Three to five numbers from the report: students, countries, scholarships awarded, workshops, consultants certified.]\n\nThank you to every student, mentor, partner and donor who made this year happen. Read the full report through the link in bio.\n\n#AnnualReport #SoilFoodWeb #Nonprofit #YearInReview',
      slides: [
        { text: 'Our year in numbers.', image: null },
        { text: '[students]', image: null },
        { text: '[countries]', image: null },
        { text: '[scholarships]', image: null },
        { text: '[workshops]', image: null },
        { text: 'Read the full report, link in bio.', image: null },
      ],
      cta: 'Read the report, link in bio',
      link: '[annual report link]',
      sources: [],
      visual_note:
        'No visual yet. Carousel, 6 slides. One big number per slide in EB Garamond, with a real photo behind or beside it.',
      note: 'Annual report series. Fill the numbers from the final report; date moves with the release.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): more posts about the new website and the coming annual report.',
  },
  {
    key: '2026-10-24 new ar20261208li',
    post: 'ar20261208li',
    create: {
      iso_date: '2026-12-08',
      date_tbd: false,
      topic: 'Annual report: LinkedIn release',
      platform: 'LinkedIn',
      caption:
        "Today we're publishing the Soil Food Web Foundation's first annual report.\n\n[Two or three lines on the year: reach, programs, finances.]\n\nWe wrote it for our students, partners and donors, and for anyone who wants to see how a soil biology nonprofit spends its year. Read it here: [annual report link]\n\n#AnnualReport #Nonprofit #SoilHealth #SoilFoodWeb",
      slides: [{ text: 'Our first annual report.', image: null }],
      cta: '',
      link: '[annual report link]',
      sources: [],
      visual_note: 'No visual yet. LinkedIn single image, 1200 x 627. The report cover.',
      note: 'Annual report series.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): more posts about the new website and the coming annual report.',
  },
  {
    key: '2026-10-24 new w20261209',
    post: 'w20261209',
    create: {
      iso_date: '2026-12-09',
      date_tbd: false,
      topic: 'Website: how the soil food web works',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'If someone asks you what the soil food web is, send them this page. \ud83d\udd01\n\nThe new How it works page on our website explains it in a single scroll: plants feeding microbes through their roots, the predators that release nutrients, and the structure they build together that holds water and carbon.\n\nLink in bio.\n\n#SoilFoodWeb #SoilBiology #HowItWorks #SoilHealth',
      slides: [
        { text: 'How does the soil food web work?', image: null },
        { text: 'Our new How it works page explains it in one scroll.', image: null },
        { text: 'From root to microbe to nutrient and back.', image: null },
        { text: 'Read it, link in bio.', image: null },
      ],
      cta: 'Read it, link in bio',
      link: 'https://soilfoodweb.com [VERIFY URL]',
      sources: [],
      visual_note: 'No visual yet. Carousel, 4 slides. Screenshots of the How it works page.',
      note: 'Website series.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): more posts about the new website and the coming annual report.',
  },
  {
    key: '2026-10-24 new w20261211',
    post: 'w20261211',
    create: {
      iso_date: '2026-12-11',
      date_tbd: false,
      topic: 'Website: a research library for professionals',
      platform: 'LinkedIn',
      caption:
        "For agronomists, researchers and consultants: our new website brings Dr. Elaine Ingham's published work into one library, with 77 journal papers, 6 book chapters and 10 EPA and technical reports, each linked to where you can read it.\n\nIt's the evidence base behind everything we teach, and it's open to everyone.\n\n#SoilScience #Research #DrElaineIngham #Agronomy #SoilFoodWeb",
      slides: [{ text: 'Four decades of soil biology research, searchable.', image: null }],
      cta: '',
      link: 'https://soilfoodweb.com [publications URL]',
      sources: [],
      visual_note:
        'No visual yet. LinkedIn single image, 1200 x 627. Screenshot of the publications page on a flat brand colour.',
      note: 'Website series. LinkedIn version for professionals; Instagram has Mountain Day that day.',
      status: 'draft',
    },
    reason:
      'New post (Linnea, 24 Oct): more posts about the new website and the coming annual report.',
  },
  {
    key: '2026-10-24 x20261108 visual v1',
    post: 'x20261108',
    set: {
      slides: [
        { text: 'Happy Diwali.', image: '/wormhole/tiles/x20261108-v1-1.jpg' },
        {
          text: 'Light, sweets and marigolds. Every one of them starts in living soil.',
          image: '/wormhole/tiles/x20261108-v1-2.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261109 visual v1',
    post: 'x20261109',
    set: {
      slides: [
        {
          text: "COP31 opens today. Agriculture's own negotiating track runs out in 2026.",
          image: '/wormhole/tiles/x20261109-v1-1.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261128 visual v1',
    post: 'x20261128',
    set: {
      slides: [
        { text: 'Small Business Saturday.', image: '/wormhole/tiles/x20261128-v1-1.jpg' },
        { text: 'Shop local for your soil too.', image: '/wormhole/tiles/x20261128-v1-2.jpg' },
        {
          text: 'Certified Soil Food Web Consultants run their own businesses: labs, compost operations and on-farm advice.',
          image: '/wormhole/tiles/x20261128-v1-3.jpg',
        },
        { text: 'Find one near you.', image: '/wormhole/tiles/x20261128-v1-4.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261217 visual v1',
    post: 'x20261217',
    set: {
      slides: [
        { text: 'Nitrogen from thin air.', image: '/wormhole/tiles/x20261217-v1-1.jpg' },
        {
          text: "Air is 78% nitrogen gas. Plants can't use it.",
          image: '/wormhole/tiles/x20261217-v1-2.jpg',
        },
        {
          text: 'Rhizobia bacteria in legume roots turn it into a form plants can.',
          image: '/wormhole/tiles/x20261217-v1-3.jpg',
        },
        {
          text: "Biological fixation supplies 25 to 40% of the world's yearly reactive nitrogen.",
          image: '/wormhole/tiles/x20261217-v1-4.jpg',
        },
        { text: 'No bag required.', image: '/wormhole/tiles/x20261217-v1-5.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261201 visual v1',
    post: 'x20261201',
    set: {
      slides: [
        { text: 'Today is GivingTuesday.', image: '/wormhole/tiles/x20261201-v1-1.jpg' },
        {
          text: "A scholarship puts a farmer, gardener or student in a course they couldn't otherwise take.",
          image: '/wormhole/tiles/x20261201-v1-2.jpg',
        },
        {
          text: 'They take it home to their own soil, and teach their neighbours.',
          image: '/wormhole/tiles/x20261201-v1-3.jpg',
        },
        { text: 'Give today, link in bio.', image: '/wormhole/tiles/x20261201-v1-4.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261202 visual v1',
    post: 'x20261202',
    set: {
      slides: [
        { text: 'From shovel to slide.', image: '/wormhole/tiles/x20261202-v1-1.jpg' },
        {
          text: '1. Take a small sample from the root zone.',
          image: '/wormhole/tiles/x20261202-v1-2.jpg',
        },
        { text: '2. Mix it with water.', image: '/wormhole/tiles/x20261202-v1-3.jpg' },
        { text: '3. Put one drop on a slide.', image: '/wormhole/tiles/x20261202-v1-4.jpg' },
        {
          text: '4. Count what you see: bacteria, fungi, protozoa, nematodes.',
          image: '/wormhole/tiles/x20261202-v1-5.jpg',
        },
        {
          text: 'That count tells you what your soil needs.',
          image: '/wormhole/tiles/x20261202-v1-6.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261203 visual v1',
    post: 'x20261203',
    set: {
      slides: [
        { text: 'Six weeks to Costa Rica.', image: '/wormhole/tiles/x20261203-v1-1.jpg' },
        { text: '18 to 29 January 2027.', image: '/wormhole/tiles/x20261203-v1-2.jpg' },
        {
          text: 'Compost piles in the morning, the microscope in the afternoon.',
          image: '/wormhole/tiles/x20261203-v1-3.jpg',
        },
        { text: 'Places are still open.', image: '/wormhole/tiles/x20261203-v1-4.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261204 visual v1',
    post: 'x20261204',
    set: {
      slides: [
        { text: 'Wildlife Conservation Day.', image: '/wormhole/tiles/x20261204-v1-1.jpg' },
        { text: 'Meet the wildlife under your feet.', image: '/wormhole/tiles/x20261204-v1-2.jpg' },
        { text: 'Bacteria.', image: '/wormhole/tiles/x20261204-v1-3.jpg' },
        { text: 'Fungi.', image: '/wormhole/tiles/x20261204-v1-4.jpg' },
        { text: 'Protozoa.', image: '/wormhole/tiles/x20261204-v1-5.jpg' },
        { text: 'Nematodes.', image: '/wormhole/tiles/x20261204-v1-6.jpg' },
        { text: 'Microarthropods.', image: '/wormhole/tiles/x20261204-v1-7.jpg' },
        {
          text: 'Protect their habitat: keep soil covered and roots growing.',
          image: '/wormhole/tiles/x20261204-v1-8.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261208 visual v1',
    post: 'x20261208',
    set: {
      slides: [
        { text: 'Who eats whom in your soil?', image: '/wormhole/tiles/x20261208-v1-1.jpg' },
        {
          text: 'Plants feed bacteria and fungi through their roots.',
          image: '/wormhole/tiles/x20261208-v1-2.jpg',
        },
        {
          text: 'Protozoa and nematodes eat the bacteria and fungi.',
          image: '/wormhole/tiles/x20261208-v1-3.jpg',
        },
        {
          text: "What they don't need comes out as nutrients plants can take up.",
          image: '/wormhole/tiles/x20261208-v1-4.jpg',
        },
        {
          text: 'Lose a link, and the plant goes hungry.',
          image: '/wormhole/tiles/x20261208-v1-5.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261213 visual v1',
    post: 'x20261213',
    set: {
      slides: [
        {
          text: 'This amoeba lives in a house it built.',
          image: '/wormhole/tiles/x20261213-v1-1.jpg',
        },
        {
          text: 'Testate amoebae make a shell from their own secretions or from grains of mineral.',
          image: '/wormhole/tiles/x20261213-v1-2.jpg',
        },
        {
          text: 'They eat bacteria and release nutrients plants can use.',
          image: '/wormhole/tiles/x20261213-v1-3.jpg',
        },
        {
          text: 'Lots of them usually means a wetter, fungal-rich soil.',
          image: '/wormhole/tiles/x20261213-v1-4.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261215 visual v1',
    post: 'x20261215',
    set: {
      slides: [
        { text: 'What does one scholarship become?', image: '/wormhole/tiles/x20261215-v1-1.jpg' },
        { text: 'One course.', image: '/wormhole/tiles/x20261215-v1-2.jpg' },
        {
          text: 'One farm that changes how it builds soil.',
          image: '/wormhole/tiles/x20261215-v1-3.jpg',
        },
        {
          text: 'A neighbour who sees the difference.',
          image: '/wormhole/tiles/x20261215-v1-4.jpg',
        },
        {
          text: 'Give before the year ends, link in bio.',
          image: '/wormhole/tiles/x20261215-v1-5.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261220 visual v1',
    post: 'x20261220',
    set: {
      slides: [
        {
          text: 'Congratulations to our Permaculture Design Certificate cohort.',
          image: '/wormhole/tiles/x20261220-v1-1.jpg',
        },
        { text: 'Twelve weeks, one design each.', image: '/wormhole/tiles/x20261220-v1-2.jpg' },
        {
          text: "We can't wait to see what you build.",
          image: '/wormhole/tiles/x20261220-v1-3.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261222 visual v1',
    post: 'x20261222',
    set: {
      slides: [
        { text: 'Holiday reading.', image: '/wormhole/tiles/x20261222-v1-1.jpg' },
        {
          text: "Four decades of Dr. Elaine Ingham's research, linked in one place.",
          image: '/wormhole/tiles/x20261222-v1-2.jpg',
        },
        { text: 'Start with one. Pour a coffee.', image: '/wormhole/tiles/x20261222-v1-3.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261224 visual v1',
    post: 'x20261224',
    set: {
      slides: [
        {
          text: 'Your Christmas tree has one more job.',
          image: '/wormhole/tiles/x20261224-v1-1.jpg',
        },
        { text: 'Chip it, or ask if your town does.', image: '/wormhole/tiles/x20261224-v1-2.jpg' },
        { text: 'Woody mulch feeds fungi.', image: '/wormhole/tiles/x20261224-v1-3.jpg' },
        { text: 'Spread it around trees and shrubs.', image: '/wormhole/tiles/x20261224-v1-4.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261226 visual v1',
    post: 'x20261226',
    set: {
      slides: [
        {
          text: 'Can wrapping paper go in the compost?',
          image: '/wormhole/tiles/x20261226-v1-1.jpg',
        },
        {
          text: 'Plain paper and cardboard: yes, shredded.',
          image: '/wormhole/tiles/x20261226-v1-2.jpg',
        },
        {
          text: 'Glossy, foil, glitter or plastic-coated: no.',
          image: '/wormhole/tiles/x20261226-v1-3.jpg',
        },
        { text: 'Tape and ribbons off first.', image: '/wormhole/tiles/x20261226-v1-4.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261229 visual v1',
    post: 'x20261229',
    set: {
      slides: [
        { text: '2026 in soil science.', image: '/wormhole/tiles/x20261229-v1-1.jpg' },
        {
          text: "A mustard plant that 'couldn't' partner with fungi traded food with one.",
          image: '/wormhole/tiles/x20261229-v1-2.jpg',
        },
        {
          text: 'An open map of the bacteria and fungi in 100,000 soil samples.',
          image: '/wormhole/tiles/x20261229-v1-3.jpg',
        },
        {
          text: 'Regenerative almond orchards: water soaked in 6x faster, same yield.',
          image: '/wormhole/tiles/x20261229-v1-4.jpg',
        },
        { text: "Here's to more in 2027.", image: '/wormhole/tiles/x20261229-v1-5.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261231 visual v1',
    post: 'x20261231',
    set: {
      slides: [
        { text: 'Happy New Year from the soil.', image: '/wormhole/tiles/x20261231-v1-1.jpg' },
        { text: 'Costa Rica, 18 to 29 January.', image: '/wormhole/tiles/x20261231-v1-2.jpg' },
        { text: 'New Mexico, 3 to 14 May.', image: '/wormhole/tiles/x20261231-v1-3.jpg' },
        { text: 'United Kingdom, September.', image: '/wormhole/tiles/x20261231-v1-4.jpg' },
        { text: 'Which one is yours?', image: '/wormhole/tiles/x20261231-v1-5.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261117 visual v1',
    post: 'x20261117',
    set: {
      slides: [
        {
          text: 'Every permaculture design starts with three ethics.',
          image: '/wormhole/tiles/x20261117-v1-1.jpg',
        },
        { text: 'Earth care.', image: '/wormhole/tiles/x20261117-v1-2.jpg' },
        { text: 'People care.', image: '/wormhole/tiles/x20261117-v1-3.jpg' },
        { text: 'Fair share.', image: '/wormhole/tiles/x20261117-v1-4.jpg' },
        { text: 'Living soil serves all three.', image: '/wormhole/tiles/x20261117-v1-5.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261118 visual v1',
    post: 'x20261118',
    set: {
      slides: [
        {
          text: 'Ten weeks to make compost you can prove.',
          image: '/wormhole/tiles/x20261118-v1-1.jpg',
        },
        {
          text: 'Compost Intensive Course, starting January 2027.',
          image: '/wormhole/tiles/x20261118-v1-2.jpg',
        },
        {
          text: 'Build, monitor and read your own piles under the microscope.',
          image: '/wormhole/tiles/x20261118-v1-3.jpg',
        },
        { text: 'With mentors every week.', image: '/wormhole/tiles/x20261118-v1-4.jpg' },
        { text: 'Enroll now, link in bio.', image: '/wormhole/tiles/x20261118-v1-5.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261125 visual v1',
    post: 'x20261125',
    set: {
      slides: [
        {
          text: 'Start learning the soil food web this winter.',
          image: '/wormhole/tiles/x20261125-v1-1.jpg',
        },
        {
          text: 'The Foundation Courses: at your own pace, from anywhere.',
          image: '/wormhole/tiles/x20261125-v1-2.jpg',
        },
        {
          text: 'The science, the compost, the extracts and teas, the microscope.',
          image: '/wormhole/tiles/x20261125-v1-3.jpg',
        },
        {
          text: '10,000+ people in 100+ countries have started here.',
          image: '/wormhole/tiles/x20261125-v1-4.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261129 visual v1',
    post: 'x20261129',
    set: {
      slides: [
        {
          text: 'A fruit tree grows better with friends.',
          image: '/wormhole/tiles/x20261129-v1-1.jpg',
        },
        { text: 'Clover underneath fixes nitrogen.', image: '/wormhole/tiles/x20261129-v1-2.jpg' },
        {
          text: 'Comfrey gets cut and dropped as mulch.',
          image: '/wormhole/tiles/x20261129-v1-3.jpg',
        },
        {
          text: 'Chives and other alliums fill the gaps.',
          image: '/wormhole/tiles/x20261129-v1-4.jpg',
        },
        {
          text: 'Together they keep the soil covered and alive.',
          image: '/wormhole/tiles/x20261129-v1-5.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261130 visual v1',
    post: 'x20261130',
    set: {
      slides: [
        {
          text: 'Your compost, checked under the microscope.',
          image: '/wormhole/tiles/x20261130-v1-1.jpg',
        },
        {
          text: 'The Compost Intensive Course starts in January.',
          image: '/wormhole/tiles/x20261130-v1-2.jpg',
        },
        { text: 'Enroll now, link in bio.', image: '/wormhole/tiles/x20261130-v1-3.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261216 visual v1',
    post: 'x20261216',
    set: {
      slides: [
        { text: 'Permaculture zones.', image: '/wormhole/tiles/x20261216-v1-1.jpg' },
        { text: 'Zone 0: the house.', image: '/wormhole/tiles/x20261216-v1-2.jpg' },
        {
          text: 'Zone 1: what you visit every day. Herbs, salad, the compost bin.',
          image: '/wormhole/tiles/x20261216-v1-3.jpg',
        },
        {
          text: 'Zones 2 to 4: orchard, field, pasture, woodlot.',
          image: '/wormhole/tiles/x20261216-v1-4.jpg',
        },
        { text: 'Zone 5: left wild.', image: '/wormhole/tiles/x20261216-v1-5.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261227 visual v1',
    post: 'x20261227',
    set: {
      slides: [
        { text: 'Chop and drop.', image: '/wormhole/tiles/x20261227-v1-1.jpg' },
        {
          text: 'Cut the plant. Leave it where it falls.',
          image: '/wormhole/tiles/x20261227-v1-2.jpg',
        },
        {
          text: 'It shades the soil and feeds the fungi and bacteria underneath.',
          image: '/wormhole/tiles/x20261227-v1-3.jpg',
        },
        { text: 'No hauling, no bare ground.', image: '/wormhole/tiles/x20261227-v1-4.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 w20261103 visual v1',
    post: 'w20261103',
    set: {
      slides: [
        { text: 'Our new website is here.', image: '/wormhole/tiles/w20261103-v1-1.jpg' },
        {
          text: 'Learn: every course, and where to start.',
          image: '/wormhole/tiles/w20261103-v1-2.jpg',
        },
        {
          text: 'Workshops and events, past and coming.',
          image: '/wormhole/tiles/w20261103-v1-3.jpg',
        },
        { text: 'Find a consultant near you.', image: '/wormhole/tiles/w20261103-v1-4.jpg' },
        {
          text: "Dr. Elaine's research, all in one place.",
          image: '/wormhole/tiles/w20261103-v1-5.jpg',
        },
        { text: 'Take the tour, link in bio.', image: '/wormhole/tiles/w20261103-v1-6.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 w20261106 visual v1',
    post: 'w20261106',
    set: {
      slides: [
        {
          text: 'What does living soil look like on a real farm?',
          image: '/wormhole/tiles/w20261106-v1-1.jpg',
        },
        { text: 'Our new Projects pages show you.', image: '/wormhole/tiles/w20261106-v1-2.jpg' },
        {
          text: 'Farms, vineyards and restoration sites.',
          image: '/wormhole/tiles/w20261106-v1-3.jpg',
        },
        {
          text: 'What they changed, and what happened.',
          image: '/wormhole/tiles/w20261106-v1-4.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 w20261206 visual v1',
    post: 'w20261206',
    set: {
      slides: [
        { text: 'Not sure where to start?', image: '/wormhole/tiles/w20261206-v1-1.jpg' },
        {
          text: 'What brings you to the soil food web?',
          image: '/wormhole/tiles/w20261206-v1-2.jpg',
        },
        {
          text: "Gardener, farmer or future consultant: there's a path for you.",
          image: '/wormhole/tiles/w20261206-v1-3.jpg',
        },
        { text: 'Find yours, link in bio.', image: '/wormhole/tiles/w20261206-v1-4.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 w20261209 visual v1',
    post: 'w20261209',
    set: {
      slides: [
        { text: 'How does the soil food web work?', image: '/wormhole/tiles/w20261209-v1-1.jpg' },
        {
          text: 'Our new How it works page explains it in one scroll.',
          image: '/wormhole/tiles/w20261209-v1-2.jpg',
        },
        {
          text: 'From root to microbe to nutrient and back.',
          image: '/wormhole/tiles/w20261209-v1-3.jpg',
        },
        { text: 'Read it, link in bio.', image: '/wormhole/tiles/w20261209-v1-4.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 w20261211 visual v1',
    post: 'w20261211',
    set: {
      slides: [
        {
          text: 'Four decades of soil biology research, searchable.',
          image: '/wormhole/tiles/w20261211-v1-1.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 ar20261123 visual v1',
    post: 'ar20261123',
    set: {
      slides: [
        {
          text: 'Our first annual report is almost here.',
          image: '/wormhole/tiles/ar20261123-v1-1.jpg',
        },
        {
          text: 'A year of courses, workshops and scholarships.',
          image: '/wormhole/tiles/ar20261123-v1-2.jpg',
        },
        { text: 'Coming soon.', image: '/wormhole/tiles/ar20261123-v1-3.jpg' },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 ev-02 visual v1',
    post: 'ev-02',
    set: {
      slides: [
        { text: 'An open map of soil life', image: '/wormhole/tiles/ev-02-v1-1.jpg' },
        {
          text: '100,000 soil samples. 90+ countries. One protocol.',
          image: '/wormhole/tiles/ev-02-v1-2.jpg',
        },
        {
          text: 'Bacteria and fungi, open to everyone. Explore the Atlas at beopen.earth',
          image: '/wormhole/tiles/ev-02-v1-3.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): built with tools/wormhole-visuals/feed_novdec.py, a different look from the posts on either side of it in the grid. Real photos from the SFW microscope library and workshops, credited on the slides.',
  },
  {
    key: '2026-10-24 x20261210 visual v1',
    post: 'x20261210',
    set: {
      slides: [
        {
          text: '131\u00b0F (55\u00b0C) for three full days kills weed seeds and pathogens.',
          image: '/wormhole/tiles/x20261210-v1-1.jpg',
        },
        {
          text: '155 to 160\u00b0F (68 to 71\u00b0C) is the ceiling. Hotter, and the beneficial organisms die too.',
          image: '/wormhole/tiles/x20261210-v1-2.jpg',
        },
        {
          text: 'Turn the pile when it climbs too high, too fast.',
          image: '/wormhole/tiles/x20261210-v1-3.jpg',
        },
        {
          text: 'Most piles need three to five turns.',
          image: '/wormhole/tiles/x20261210-v1-4.jpg',
        },
      ],
    },
    reason:
      'Visual (24 Oct): big numbers in EB Garamond with the pile thermometer photo; slides 2 and 3 of the draft merged into one.',
  },
  {
    key: '2026-10-24 x20261108 visual v2 photo-first',
    post: 'x20261108',
    set: {
      slides: [{ text: 'Happy Diwali.', image: '/wormhole/tiles/x20261108-v2-1.jpg' }],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261109 visual v2 photo-first',
    post: 'x20261109',
    set: {
      slides: [{ text: 'COP31 opens today.', image: '/wormhole/tiles/x20261109-v2-1.jpg' }],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 w20261106 visual v2 photo-first',
    post: 'w20261106',
    set: {
      slides: [
        { text: 'Real farms. Real soil.', image: '/wormhole/tiles/w20261106-v2-1.jpg' },
        {
          text: 'Photo only: misting a compost pile.',
          image: '/wormhole/tiles/w20261106-v2-2.jpg',
        },
        { text: 'Our new Projects pages.', image: '/wormhole/tiles/w20261106-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261117 visual v2 photo-first',
    post: 'x20261117',
    set: {
      slides: [
        { text: 'Earth care.', image: '/wormhole/tiles/x20261117-v2-1.jpg' },
        { text: 'People care.', image: '/wormhole/tiles/x20261117-v2-2.jpg' },
        { text: 'Fair share.', image: '/wormhole/tiles/x20261117-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261118 visual v2 photo-first',
    post: 'x20261118',
    set: {
      slides: [
        { text: 'Compost Intensive Course.', image: '/wormhole/tiles/x20261118-v2-1.jpg' },
        {
          text: 'Photo only: thermometer in the pile.',
          image: '/wormhole/tiles/x20261118-v2-2.jpg',
        },
        {
          text: 'Photo only: testate amoeba under the microscope.',
          image: '/wormhole/tiles/x20261118-v2-3.jpg',
        },
        { text: 'Starts January 2027. Link in bio.', image: '/wormhole/tiles/x20261118-v2-4.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 ev-02 visual v2 photo-first',
    post: 'ev-02',
    set: {
      slides: [
        { text: '100,000 soil samples, one open atlas.', image: '/wormhole/tiles/ev-02-v2-1.jpg' },
        { text: 'Photo only: fungal hypha.', image: '/wormhole/tiles/ev-02-v2-2.jpg' },
        { text: 'Explore it at beopen.earth', image: '/wormhole/tiles/ev-02-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 ar20261123 visual v2 photo-first',
    post: 'ar20261123',
    set: {
      slides: [
        { text: 'Our first annual report.', image: '/wormhole/tiles/ar20261123-v2-1.jpg' },
        {
          text: 'Photo only: turning a pile at a workshop.',
          image: '/wormhole/tiles/ar20261123-v2-2.jpg',
        },
        { text: 'Coming soon.', image: '/wormhole/tiles/ar20261123-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261128 visual v2 photo-first',
    post: 'x20261128',
    set: {
      slides: [
        { text: 'Small Business Saturday.', image: '/wormhole/tiles/x20261128-v2-1.jpg' },
        { text: 'Photo only: making an extract.', image: '/wormhole/tiles/x20261128-v2-2.jpg' },
        {
          text: 'Shop local for your soil. Find a consultant, link in bio.',
          image: '/wormhole/tiles/x20261128-v2-3.jpg',
        },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261129 visual v2 photo-first',
    post: 'x20261129',
    set: {
      slides: [
        { text: 'Trees grow better with friends.', image: '/wormhole/tiles/x20261129-v2-1.jpg' },
        { text: 'Photo only: mixed planting beds.', image: '/wormhole/tiles/x20261129-v2-2.jpg' },
        { text: 'Photo only: chard in straw mulch.', image: '/wormhole/tiles/x20261129-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261130 visual v2 photo-first',
    post: 'x20261130',
    set: {
      slides: [
        { text: '10 weeks of compost.', image: '/wormhole/tiles/x20261130-v2-1.jpg' },
        { text: 'Enroll now, link in bio.', image: '/wormhole/tiles/x20261130-v2-2.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261201 visual v2 photo-first',
    post: 'x20261201',
    set: {
      slides: [
        { text: 'Today is GivingTuesday.', image: '/wormhole/tiles/x20261201-v2-1.jpg' },
        { text: 'Photo only: garden beds.', image: '/wormhole/tiles/x20261201-v2-2.jpg' },
        { text: 'Give a scholarship, link in bio.', image: '/wormhole/tiles/x20261201-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261202 visual v2 photo-first',
    post: 'x20261202',
    set: {
      slides: [
        { text: 'From shovel to slide.', image: '/wormhole/tiles/x20261202-v2-1.jpg' },
        {
          text: 'Photo only: mixing the sample with water.',
          image: '/wormhole/tiles/x20261202-v2-2.jpg',
        },
        { text: 'Photo only: preparing the slide.', image: '/wormhole/tiles/x20261202-v2-3.jpg' },
        {
          text: 'Photo only: a nematode under the microscope.',
          image: '/wormhole/tiles/x20261202-v2-4.jpg',
        },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261203 visual v2 photo-first',
    post: 'x20261203',
    set: {
      slides: [
        { text: 'Costa Rica, 18 to 29 January 2027.', image: '/wormhole/tiles/x20261203-v2-1.jpg' },
        { text: 'Photo only: Costa Rican forest.', image: '/wormhole/tiles/x20261203-v2-2.jpg' },
        { text: 'Photo only: turning a pile.', image: '/wormhole/tiles/x20261203-v2-3.jpg' },
        { text: 'Places still open, link in bio.', image: '/wormhole/tiles/x20261203-v2-4.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261204 visual v2 photo-first',
    post: 'x20261204',
    set: {
      slides: [
        {
          text: 'Wildlife Conservation Day: meet the wildlife under your feet.',
          image: '/wormhole/tiles/x20261204-v2-1.jpg',
        },
        { text: 'Bacteria.', image: '/wormhole/tiles/x20261204-v2-2.jpg' },
        { text: 'Fungi.', image: '/wormhole/tiles/x20261204-v2-3.jpg' },
        { text: 'Protozoa.', image: '/wormhole/tiles/x20261204-v2-4.jpg' },
        { text: 'Nematodes.', image: '/wormhole/tiles/x20261204-v2-5.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 w20261206 visual v2 photo-first',
    post: 'w20261206',
    set: {
      slides: [
        { text: 'Not sure where to start?', image: '/wormhole/tiles/w20261206-v2-1.jpg' },
        {
          text: 'Photo only: Dr. Elaine in the garden.',
          image: '/wormhole/tiles/w20261206-v2-2.jpg',
        },
        { text: 'Find your path, link in bio.', image: '/wormhole/tiles/w20261206-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261208 visual v2 photo-first',
    post: 'x20261208',
    set: {
      slides: [
        { text: 'Who eats whom in your soil?', image: '/wormhole/tiles/x20261208-v2-1.jpg' },
        { text: 'Photo only: bacteria.', image: '/wormhole/tiles/x20261208-v2-2.jpg' },
        { text: 'Photo only: protozoa.', image: '/wormhole/tiles/x20261208-v2-3.jpg' },
        { text: 'Photo only: a nematode.', image: '/wormhole/tiles/x20261208-v2-4.jpg' },
        { text: 'And the plant gets fed.', image: '/wormhole/tiles/x20261208-v2-5.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 w20261209 visual v2 photo-first',
    post: 'w20261209',
    set: {
      slides: [
        { text: 'How does the soil food web work?', image: '/wormhole/tiles/w20261209-v2-1.jpg' },
        { text: 'Photo only: a nematode.', image: '/wormhole/tiles/w20261209-v2-2.jpg' },
        {
          text: 'Our new How it works page, link in bio.',
          image: '/wormhole/tiles/w20261209-v2-3.jpg',
        },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261210 visual v2 photo-first',
    post: 'x20261210',
    set: {
      slides: [
        { text: '131°F (55°C) for three days.', image: '/wormhole/tiles/x20261210-v2-1.jpg' },
        { text: 'Photo only: misting the pile.', image: '/wormhole/tiles/x20261210-v2-2.jpg' },
        { text: 'Then turn it.', image: '/wormhole/tiles/x20261210-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 w20261211 visual v2 photo-first',
    post: 'w20261211',
    set: {
      slides: [
        {
          text: "Four decades of Dr. Elaine Ingham's research, searchable.",
          image: '/wormhole/tiles/w20261211-v2-1.jpg',
        },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261213 visual v2 photo-first',
    post: 'x20261213',
    set: {
      slides: [
        { text: 'This amoeba built its own house.', image: '/wormhole/tiles/x20261213-v2-1.jpg' },
        { text: 'Photo only: the shell up close.', image: '/wormhole/tiles/x20261213-v2-2.jpg' },
        { text: 'Photo only: bacteria, its food.', image: '/wormhole/tiles/x20261213-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261216 visual v2 photo-first',
    post: 'x20261216',
    set: {
      slides: [
        { text: 'Permaculture zones.', image: '/wormhole/tiles/x20261216-v2-1.jpg' },
        {
          text: 'Zone 1: herbs, salad, the compost bin.',
          image: '/wormhole/tiles/x20261216-v2-2.jpg',
        },
        { text: 'Zone 5: left wild.', image: '/wormhole/tiles/x20261216-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261217 visual v2 photo-first',
    post: 'x20261217',
    set: {
      slides: [
        { text: 'Nitrogen from thin air.', image: '/wormhole/tiles/x20261217-v2-1.jpg' },
        { text: 'Photo only: bacteria.', image: '/wormhole/tiles/x20261217-v2-2.jpg' },
        { text: 'No bag required.', image: '/wormhole/tiles/x20261217-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261220 visual v2 photo-first',
    post: 'x20261220',
    set: {
      slides: [
        {
          text: 'Congratulations to our Permaculture Design Certificate class of 2026.',
          image: '/wormhole/tiles/x20261220-v2-1.jpg',
        },
        { text: 'Photo only: food forest.', image: '/wormhole/tiles/x20261220-v2-2.jpg' },
        { text: 'Go build it.', image: '/wormhole/tiles/x20261220-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261224 visual v2 photo-first',
    post: 'x20261224',
    set: {
      slides: [
        {
          text: 'Your Christmas tree has one more job.',
          image: '/wormhole/tiles/x20261224-v2-1.jpg',
        },
        { text: 'Chip it. Mulch it.', image: '/wormhole/tiles/x20261224-v2-2.jpg' },
        { text: 'Photo only: the fungi it feeds.', image: '/wormhole/tiles/x20261224-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261226 visual v2 photo-first',
    post: 'x20261226',
    set: {
      slides: [
        {
          text: 'Can wrapping paper go in the compost? Plain paper: yes.',
          image: '/wormhole/tiles/x20261226-v2-1.jpg',
        },
        { text: 'Glossy, foil, glitter, tape: no.', image: '/wormhole/tiles/x20261226-v2-2.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261227 visual v2 photo-first',
    post: 'x20261227',
    set: {
      slides: [
        { text: 'Chop and drop.', image: '/wormhole/tiles/x20261227-v2-1.jpg' },
        {
          text: 'Photo only: leaves left where they fall.',
          image: '/wormhole/tiles/x20261227-v2-2.jpg',
        },
        { text: 'Photo only: the fungi underneath.', image: '/wormhole/tiles/x20261227-v2-3.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261229 visual v2 photo-first',
    post: 'x20261229',
    set: {
      slides: [
        { text: '2026 in soil science.', image: '/wormhole/tiles/x20261229-v2-1.jpg' },
        { text: 'Photo only: bacteria.', image: '/wormhole/tiles/x20261229-v2-2.jpg' },
        {
          text: 'Photo only: no-till soil after rain.',
          image: '/wormhole/tiles/x20261229-v2-3.jpg',
        },
        { text: "Here's to more in 2027.", image: '/wormhole/tiles/x20261229-v2-4.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261231 visual v2 photo-first',
    post: 'x20261231',
    set: {
      slides: [
        { text: 'Happy New Year from the soil.', image: '/wormhole/tiles/x20261231-v2-1.jpg' },
        { text: 'Costa Rica, 18 to 29 January.', image: '/wormhole/tiles/x20261231-v2-2.jpg' },
        { text: 'New Mexico, 3 to 14 May.', image: '/wormhole/tiles/x20261231-v2-3.jpg' },
        { text: 'United Kingdom, September.', image: '/wormhole/tiles/x20261231-v2-4.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 pl20261114 visual v2 photo-first',
    post: 'pl20261114',
    set: {
      slides: [
        {
          text: 'Your fallen leaves can become fungal compost.',
          image: '/wormhole/tiles/pl20261114-v2-1.jpg',
        },
        {
          text: 'Photo only: wet leaves packed in a wire cage.',
          image: '/wormhole/tiles/pl20261114-v2-2.jpg',
        },
        { text: 'Photo only: leaves breaking down.', image: '/wormhole/tiles/pl20261114-v2-3.jpg' },
        { text: 'Photo only: finished leaf mold.', image: '/wormhole/tiles/pl20261114-v2-4.jpg' },
        {
          text: 'Use it as mulch or in potting soil.',
          image: '/wormhole/tiles/pl20261114-v2-5.jpg',
        },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 pl20261115 visual v2 photo-first',
    post: 'pl20261115',
    set: {
      slides: [
        {
          text: 'Imagine a world without earthworms.',
          image: '/wormhole/tiles/pl20261115-v2-1.jpg',
        },
        { text: 'Photo only: a northern forest.', image: '/wormhole/tiles/pl20261115-v2-2.jpg' },
        {
          text: 'Photo only: an introduced earthworm.',
          image: '/wormhole/tiles/pl20261115-v2-3.jpg',
        },
        {
          text: 'Even a good organism can be the wrong one in the wrong place.',
          image: '/wormhole/tiles/pl20261115-v2-4.jpg',
        },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 p26 visual v2 photo-first',
    post: 'p26',
    set: {
      slides: [
        {
          text: 'Welcome to our newest Certified Soil Food Web Consultants.',
          image: '/wormhole/tiles/p26-v2-1.jpg',
        },
        { text: 'Kyle Babcock, United States.', image: '/wormhole/tiles/p26-v2-2.jpg' },
      ],
    },
    reason:
      'Visual v2 (24 Oct, Linnea: "Visual should be visual, as little text as possible and only picture"): every slide is a real photo edge to edge, a few words at most, no type on plain colour. Built with tools/wormhole-visuals/photo_first.py.',
  },
  {
    key: '2026-10-24 x20261226 visual v3 more slides',
    post: 'x20261226',
    set: {
      slides: [
        {
          text: 'Can wrapping paper go in the compost? Plain paper: yes.',
          image: '/wormhole/tiles/x20261226-v3-1.jpg',
        },
        { text: 'Tape and ribbons off first.', image: '/wormhole/tiles/x20261226-v3-2.jpg' },
        {
          text: 'Tear it small and keep the pile damp.',
          image: '/wormhole/tiles/x20261226-v3-3.jpg',
        },
        {
          text: 'Photo only: fungi break the paper down.',
          image: '/wormhole/tiles/x20261226-v3-4.jpg',
        },
        {
          text: 'Glossy, foil, glitter or plastic-coated: no.',
          image: '/wormhole/tiles/x20261226-v3-5.jpg',
        },
      ],
    },
    reason:
      'Visual v3 (Linnea, 24 Oct: "add more slides to the wrapping paper one"): 5 photo slides instead of 2.',
  },
  {
    key: '2026-10-24 w20261106 visual v4 mixed looks',
    post: 'w20261106',
    set: {
      slides: [
        { text: 'New: Projects pages.', image: '/wormhole/tiles/w20261106-v4-1.jpg' },
        {
          text: 'Photo only: no-till soil after rain.',
          image: '/wormhole/tiles/w20261106-v4-2.jpg',
        },
        { text: 'Real farms. Real soil.', image: '/wormhole/tiles/w20261106-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261108 visual v4 mixed looks',
    post: 'x20261108',
    set: {
      slides: [{ text: 'Happy Diwali.', image: '/wormhole/tiles/x20261108-v4-1.jpg' }],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 p26 visual v4 mixed looks',
    post: 'p26',
    set: {
      slides: [
        {
          text: 'Welcome to our newest Certified Soil Food Web Consultant, Kyle Babcock.',
          image: '/wormhole/tiles/p26-v4-1.jpg',
        },
        {
          text: 'Photo only: a workshop turning a compost pile.',
          image: '/wormhole/tiles/p26-v4-2.jpg',
        },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 pl20261114 visual v4 mixed looks',
    post: 'pl20261114',
    set: {
      slides: [
        {
          text: 'Photo only: fallen leaves. Your leaves can become fungal compost.',
          image: '/wormhole/tiles/pl20261114-v4-1.jpg',
        },
        {
          text: 'Pack wet leaves into a wire cage or a bag with holes.',
          image: '/wormhole/tiles/pl20261114-v4-2.jpg',
        },
        { text: 'Photo only: leaves breaking down.', image: '/wormhole/tiles/pl20261114-v4-3.jpg' },
        { text: 'Photo only: finished leaf mold.', image: '/wormhole/tiles/pl20261114-v4-4.jpg' },
        {
          text: 'Use it as mulch or in potting soil.',
          image: '/wormhole/tiles/pl20261114-v4-5.jpg',
        },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 pl20261115 visual v4 mixed looks',
    post: 'pl20261115',
    set: {
      slides: [
        {
          text: 'Imagine a world without earthworms.',
          image: '/wormhole/tiles/pl20261115-v4-1.jpg',
        },
        { text: 'Photo only: a northern forest.', image: '/wormhole/tiles/pl20261115-v4-2.jpg' },
        {
          text: 'Photo only: an introduced earthworm.',
          image: '/wormhole/tiles/pl20261115-v4-3.jpg',
        },
        {
          text: 'Even a good organism can be the wrong one in the wrong place.',
          image: '/wormhole/tiles/pl20261115-v4-4.jpg',
        },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261117 visual v4 mixed looks',
    post: 'x20261117',
    set: {
      slides: [
        { text: 'Earth care.', image: '/wormhole/tiles/x20261117-v4-1.jpg' },
        { text: 'People care.', image: '/wormhole/tiles/x20261117-v4-2.jpg' },
        { text: 'Fair share.', image: '/wormhole/tiles/x20261117-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261118 visual v4 mixed looks',
    post: 'x20261118',
    set: {
      slides: [
        { text: 'Compost Intensive Course.', image: '/wormhole/tiles/x20261118-v4-1.jpg' },
        {
          text: 'Photo only: thermometer in the pile.',
          image: '/wormhole/tiles/x20261118-v4-2.jpg',
        },
        { text: 'Starts January 2027. Link in bio.', image: '/wormhole/tiles/x20261118-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 ev-02 visual v4 mixed looks',
    post: 'ev-02',
    set: {
      slides: [
        { text: '100,000 soil samples, one open atlas.', image: '/wormhole/tiles/ev-02-v4-1.jpg' },
        { text: 'Photo only: fungal hypha.', image: '/wormhole/tiles/ev-02-v4-2.jpg' },
        { text: 'Explore it at beopen.earth', image: '/wormhole/tiles/ev-02-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 ar20261123 visual v4 mixed looks',
    post: 'ar20261123',
    set: {
      slides: [
        { text: 'Our first annual report.', image: '/wormhole/tiles/ar20261123-v4-1.jpg' },
        {
          text: 'Photo only: turning a pile at a workshop.',
          image: '/wormhole/tiles/ar20261123-v4-2.jpg',
        },
        { text: 'Coming soon.', image: '/wormhole/tiles/ar20261123-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261129 visual v4 mixed looks',
    post: 'x20261129',
    set: {
      slides: [
        {
          text: 'Photo only: a food forest. Trees grow better with friends.',
          image: '/wormhole/tiles/x20261129-v4-1.jpg',
        },
        { text: 'Trees grow better with friends.', image: '/wormhole/tiles/x20261129-v4-2.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261130 visual v4 mixed looks',
    post: 'x20261130',
    set: {
      slides: [
        {
          text: '10 weeks of compost and microscope work.',
          image: '/wormhole/tiles/x20261130-v4-1.jpg',
        },
        { text: 'Enroll now, link in bio.', image: '/wormhole/tiles/x20261130-v4-2.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261201 visual v4 mixed looks',
    post: 'x20261201',
    set: {
      slides: [
        { text: 'Today is GivingTuesday.', image: '/wormhole/tiles/x20261201-v4-1.jpg' },
        { text: 'Photo only: garden beds.', image: '/wormhole/tiles/x20261201-v4-2.jpg' },
        { text: 'Give a scholarship, link in bio.', image: '/wormhole/tiles/x20261201-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261202 visual v4 mixed looks',
    post: 'x20261202',
    set: {
      slides: [
        { text: 'From shovel to slide.', image: '/wormhole/tiles/x20261202-v4-1.jpg' },
        {
          text: 'Photo only: mixing the sample with water.',
          image: '/wormhole/tiles/x20261202-v4-2.jpg',
        },
        {
          text: 'Photo only: a nematode under the microscope.',
          image: '/wormhole/tiles/x20261202-v4-3.jpg',
        },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261204 visual v4 mixed looks',
    post: 'x20261204',
    set: {
      slides: [
        {
          text: 'Wildlife Conservation Day: meet the wildlife under your feet.',
          image: '/wormhole/tiles/x20261204-v4-1.jpg',
        },
        { text: 'Bacteria.', image: '/wormhole/tiles/x20261204-v4-2.jpg' },
        { text: 'Fungi.', image: '/wormhole/tiles/x20261204-v4-3.jpg' },
        { text: 'Protozoa.', image: '/wormhole/tiles/x20261204-v4-4.jpg' },
        { text: 'Nematodes.', image: '/wormhole/tiles/x20261204-v4-5.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 w20261206 visual v4 mixed looks',
    post: 'w20261206',
    set: {
      slides: [
        { text: 'Not sure where to start?', image: '/wormhole/tiles/w20261206-v4-1.jpg' },
        { text: 'Find your path, link in bio.', image: '/wormhole/tiles/w20261206-v4-2.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261208 visual v4 mixed looks',
    post: 'x20261208',
    set: {
      slides: [
        { text: 'Who eats whom in your soil?', image: '/wormhole/tiles/x20261208-v4-1.jpg' },
        { text: 'Photo only: bacteria.', image: '/wormhole/tiles/x20261208-v4-2.jpg' },
        { text: 'Photo only: protozoa.', image: '/wormhole/tiles/x20261208-v4-3.jpg' },
        { text: 'Photo only: a nematode.', image: '/wormhole/tiles/x20261208-v4-4.jpg' },
        { text: 'And the plant gets fed.', image: '/wormhole/tiles/x20261208-v4-5.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261210 visual v4 mixed looks',
    post: 'x20261210',
    set: {
      slides: [
        { text: '131°F (55°C) for three days.', image: '/wormhole/tiles/x20261210-v4-1.jpg' },
        { text: 'Then turn it.', image: '/wormhole/tiles/x20261210-v4-2.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261213 visual v4 mixed looks',
    post: 'x20261213',
    set: {
      slides: [
        {
          text: 'Photo only: a testate amoeba, which built its own house.',
          image: '/wormhole/tiles/x20261213-v4-1.jpg',
        },
        { text: 'This amoeba built its own house.', image: '/wormhole/tiles/x20261213-v4-2.jpg' },
        { text: 'Photo only: bacteria, its food.', image: '/wormhole/tiles/x20261213-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261216 visual v4 mixed looks',
    post: 'x20261216',
    set: {
      slides: [
        { text: 'Permaculture zones.', image: '/wormhole/tiles/x20261216-v4-1.jpg' },
        {
          text: 'Zone 1: herbs, salad, the compost bin.',
          image: '/wormhole/tiles/x20261216-v4-2.jpg',
        },
        { text: 'Zone 5: left wild.', image: '/wormhole/tiles/x20261216-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261220 visual v4 mixed looks',
    post: 'x20261220',
    set: {
      slides: [
        {
          text: 'Congratulations to our Permaculture Design Certificate class of 2026.',
          image: '/wormhole/tiles/x20261220-v4-1.jpg',
        },
        { text: 'Photo only: food forest.', image: '/wormhole/tiles/x20261220-v4-2.jpg' },
        { text: 'Go build it.', image: '/wormhole/tiles/x20261220-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261224 visual v4 mixed looks',
    post: 'x20261224',
    set: {
      slides: [
        {
          text: 'Your Christmas tree has one more job.',
          image: '/wormhole/tiles/x20261224-v4-1.jpg',
        },
        { text: 'Chip it. Mulch it.', image: '/wormhole/tiles/x20261224-v4-2.jpg' },
        { text: 'Photo only: the fungi it feeds.', image: '/wormhole/tiles/x20261224-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261227 visual v4 mixed looks',
    post: 'x20261227',
    set: {
      slides: [
        {
          text: 'Photo only: chard in straw mulch. Chop and drop.',
          image: '/wormhole/tiles/x20261227-v4-1.jpg',
        },
        { text: 'Chop and drop.', image: '/wormhole/tiles/x20261227-v4-2.jpg' },
        { text: 'Photo only: the fungi underneath.', image: '/wormhole/tiles/x20261227-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261229 visual v4 mixed looks',
    post: 'x20261229',
    set: {
      slides: [
        { text: '2026 in soil science.', image: '/wormhole/tiles/x20261229-v4-1.jpg' },
        {
          text: 'Photo only: no-till soil after rain.',
          image: '/wormhole/tiles/x20261229-v4-2.jpg',
        },
        { text: "Here's to more in 2027.", image: '/wormhole/tiles/x20261229-v4-3.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 x20261231 visual v4 mixed looks',
    post: 'x20261231',
    set: {
      slides: [
        { text: 'Happy New Year from the soil.', image: '/wormhole/tiles/x20261231-v4-1.jpg' },
        { text: 'Costa Rica, 18 to 29 January.', image: '/wormhole/tiles/x20261231-v4-2.jpg' },
        { text: 'New Mexico, 3 to 14 May.', image: '/wormhole/tiles/x20261231-v4-3.jpg' },
        { text: 'United Kingdom, September.', image: '/wormhole/tiles/x20261231-v4-4.jpg' },
      ],
    },
    reason:
      'Visual v4 (Linnea, 24 Oct: "why are all of these also in the same visual format?"): still picture-only, now mixed across neighbouring days: clean photo, 2x2 mosaic, two stacked photos, brand-colour frame, circle inset, word tag. Built with tools/wormhole-visuals/photo_mix.py.',
  },
  {
    key: '2026-10-24 w20261106 back to visual v2',
    post: 'w20261106',
    set: {
      slides: [
        { text: 'Real farms. Real soil.', image: '/wormhole/tiles/w20261106-v2-1.jpg' },
        {
          text: 'Photo only: misting a compost pile.',
          image: '/wormhole/tiles/w20261106-v2-2.jpg',
        },
        { text: 'Our new Projects pages.', image: '/wormhole/tiles/w20261106-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261108 back to visual v2',
    post: 'x20261108',
    set: {
      slides: [{ text: 'Happy Diwali.', image: '/wormhole/tiles/x20261108-v2-1.jpg' }],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 p26 back to visual v2',
    post: 'p26',
    set: {
      slides: [
        {
          text: 'Welcome to our newest Certified Soil Food Web Consultants.',
          image: '/wormhole/tiles/p26-v2-1.jpg',
        },
        { text: 'Kyle Babcock, United States.', image: '/wormhole/tiles/p26-v2-2.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 pl20261114 back to visual v2',
    post: 'pl20261114',
    set: {
      slides: [
        {
          text: 'Your fallen leaves can become fungal compost.',
          image: '/wormhole/tiles/pl20261114-v2-1.jpg',
        },
        {
          text: 'Photo only: wet leaves packed in a wire cage.',
          image: '/wormhole/tiles/pl20261114-v2-2.jpg',
        },
        { text: 'Photo only: leaves breaking down.', image: '/wormhole/tiles/pl20261114-v2-3.jpg' },
        { text: 'Photo only: finished leaf mold.', image: '/wormhole/tiles/pl20261114-v2-4.jpg' },
        {
          text: 'Use it as mulch or in potting soil.',
          image: '/wormhole/tiles/pl20261114-v2-5.jpg',
        },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 pl20261115 back to visual v2',
    post: 'pl20261115',
    set: {
      slides: [
        {
          text: 'Imagine a world without earthworms.',
          image: '/wormhole/tiles/pl20261115-v2-1.jpg',
        },
        { text: 'Photo only: a northern forest.', image: '/wormhole/tiles/pl20261115-v2-2.jpg' },
        {
          text: 'Photo only: an introduced earthworm.',
          image: '/wormhole/tiles/pl20261115-v2-3.jpg',
        },
        {
          text: 'Even a good organism can be the wrong one in the wrong place.',
          image: '/wormhole/tiles/pl20261115-v2-4.jpg',
        },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261117 back to visual v2',
    post: 'x20261117',
    set: {
      slides: [
        { text: 'Earth care.', image: '/wormhole/tiles/x20261117-v2-1.jpg' },
        { text: 'People care.', image: '/wormhole/tiles/x20261117-v2-2.jpg' },
        { text: 'Fair share.', image: '/wormhole/tiles/x20261117-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261118 back to visual v2',
    post: 'x20261118',
    set: {
      slides: [
        { text: 'Compost Intensive Course.', image: '/wormhole/tiles/x20261118-v2-1.jpg' },
        {
          text: 'Photo only: thermometer in the pile.',
          image: '/wormhole/tiles/x20261118-v2-2.jpg',
        },
        {
          text: 'Photo only: testate amoeba under the microscope.',
          image: '/wormhole/tiles/x20261118-v2-3.jpg',
        },
        { text: 'Starts January 2027. Link in bio.', image: '/wormhole/tiles/x20261118-v2-4.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 ev-02 back to visual v2',
    post: 'ev-02',
    set: {
      slides: [
        { text: '100,000 soil samples, one open atlas.', image: '/wormhole/tiles/ev-02-v2-1.jpg' },
        { text: 'Photo only: fungal hypha.', image: '/wormhole/tiles/ev-02-v2-2.jpg' },
        { text: 'Explore it at beopen.earth', image: '/wormhole/tiles/ev-02-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 ar20261123 back to visual v2',
    post: 'ar20261123',
    set: {
      slides: [
        { text: 'Our first annual report.', image: '/wormhole/tiles/ar20261123-v2-1.jpg' },
        {
          text: 'Photo only: turning a pile at a workshop.',
          image: '/wormhole/tiles/ar20261123-v2-2.jpg',
        },
        { text: 'Coming soon.', image: '/wormhole/tiles/ar20261123-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261129 back to visual v2',
    post: 'x20261129',
    set: {
      slides: [
        { text: 'Trees grow better with friends.', image: '/wormhole/tiles/x20261129-v2-1.jpg' },
        { text: 'Photo only: mixed planting beds.', image: '/wormhole/tiles/x20261129-v2-2.jpg' },
        { text: 'Photo only: chard in straw mulch.', image: '/wormhole/tiles/x20261129-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261130 back to visual v2',
    post: 'x20261130',
    set: {
      slides: [
        { text: '10 weeks of compost.', image: '/wormhole/tiles/x20261130-v2-1.jpg' },
        { text: 'Enroll now, link in bio.', image: '/wormhole/tiles/x20261130-v2-2.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261201 back to visual v2',
    post: 'x20261201',
    set: {
      slides: [
        { text: 'Today is GivingTuesday.', image: '/wormhole/tiles/x20261201-v2-1.jpg' },
        { text: 'Photo only: garden beds.', image: '/wormhole/tiles/x20261201-v2-2.jpg' },
        { text: 'Give a scholarship, link in bio.', image: '/wormhole/tiles/x20261201-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261202 back to visual v2',
    post: 'x20261202',
    set: {
      slides: [
        { text: 'From shovel to slide.', image: '/wormhole/tiles/x20261202-v2-1.jpg' },
        {
          text: 'Photo only: mixing the sample with water.',
          image: '/wormhole/tiles/x20261202-v2-2.jpg',
        },
        { text: 'Photo only: preparing the slide.', image: '/wormhole/tiles/x20261202-v2-3.jpg' },
        {
          text: 'Photo only: a nematode under the microscope.',
          image: '/wormhole/tiles/x20261202-v2-4.jpg',
        },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261204 back to visual v2',
    post: 'x20261204',
    set: {
      slides: [
        {
          text: 'Wildlife Conservation Day: meet the wildlife under your feet.',
          image: '/wormhole/tiles/x20261204-v2-1.jpg',
        },
        { text: 'Bacteria.', image: '/wormhole/tiles/x20261204-v2-2.jpg' },
        { text: 'Fungi.', image: '/wormhole/tiles/x20261204-v2-3.jpg' },
        { text: 'Protozoa.', image: '/wormhole/tiles/x20261204-v2-4.jpg' },
        { text: 'Nematodes.', image: '/wormhole/tiles/x20261204-v2-5.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 w20261206 back to visual v2',
    post: 'w20261206',
    set: {
      slides: [
        { text: 'Not sure where to start?', image: '/wormhole/tiles/w20261206-v2-1.jpg' },
        {
          text: 'Photo only: Dr. Elaine in the garden.',
          image: '/wormhole/tiles/w20261206-v2-2.jpg',
        },
        { text: 'Find your path, link in bio.', image: '/wormhole/tiles/w20261206-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261208 back to visual v2',
    post: 'x20261208',
    set: {
      slides: [
        { text: 'Who eats whom in your soil?', image: '/wormhole/tiles/x20261208-v2-1.jpg' },
        { text: 'Photo only: bacteria.', image: '/wormhole/tiles/x20261208-v2-2.jpg' },
        { text: 'Photo only: protozoa.', image: '/wormhole/tiles/x20261208-v2-3.jpg' },
        { text: 'Photo only: a nematode.', image: '/wormhole/tiles/x20261208-v2-4.jpg' },
        { text: 'And the plant gets fed.', image: '/wormhole/tiles/x20261208-v2-5.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261210 back to visual v2',
    post: 'x20261210',
    set: {
      slides: [
        { text: '131°F (55°C) for three days.', image: '/wormhole/tiles/x20261210-v2-1.jpg' },
        { text: 'Photo only: misting the pile.', image: '/wormhole/tiles/x20261210-v2-2.jpg' },
        { text: 'Then turn it.', image: '/wormhole/tiles/x20261210-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261213 back to visual v2',
    post: 'x20261213',
    set: {
      slides: [
        { text: 'This amoeba built its own house.', image: '/wormhole/tiles/x20261213-v2-1.jpg' },
        { text: 'Photo only: the shell up close.', image: '/wormhole/tiles/x20261213-v2-2.jpg' },
        { text: 'Photo only: bacteria, its food.', image: '/wormhole/tiles/x20261213-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261216 back to visual v2',
    post: 'x20261216',
    set: {
      slides: [
        { text: 'Permaculture zones.', image: '/wormhole/tiles/x20261216-v2-1.jpg' },
        {
          text: 'Zone 1: herbs, salad, the compost bin.',
          image: '/wormhole/tiles/x20261216-v2-2.jpg',
        },
        { text: 'Zone 5: left wild.', image: '/wormhole/tiles/x20261216-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261220 back to visual v2',
    post: 'x20261220',
    set: {
      slides: [
        {
          text: 'Congratulations to our Permaculture Design Certificate class of 2026.',
          image: '/wormhole/tiles/x20261220-v2-1.jpg',
        },
        { text: 'Photo only: food forest.', image: '/wormhole/tiles/x20261220-v2-2.jpg' },
        { text: 'Go build it.', image: '/wormhole/tiles/x20261220-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261224 back to visual v2',
    post: 'x20261224',
    set: {
      slides: [
        {
          text: 'Your Christmas tree has one more job.',
          image: '/wormhole/tiles/x20261224-v2-1.jpg',
        },
        { text: 'Chip it. Mulch it.', image: '/wormhole/tiles/x20261224-v2-2.jpg' },
        { text: 'Photo only: the fungi it feeds.', image: '/wormhole/tiles/x20261224-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261227 back to visual v2',
    post: 'x20261227',
    set: {
      slides: [
        { text: 'Chop and drop.', image: '/wormhole/tiles/x20261227-v2-1.jpg' },
        {
          text: 'Photo only: leaves left where they fall.',
          image: '/wormhole/tiles/x20261227-v2-2.jpg',
        },
        { text: 'Photo only: the fungi underneath.', image: '/wormhole/tiles/x20261227-v2-3.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261229 back to visual v2',
    post: 'x20261229',
    set: {
      slides: [
        { text: '2026 in soil science.', image: '/wormhole/tiles/x20261229-v2-1.jpg' },
        { text: 'Photo only: bacteria.', image: '/wormhole/tiles/x20261229-v2-2.jpg' },
        {
          text: 'Photo only: no-till soil after rain.',
          image: '/wormhole/tiles/x20261229-v2-3.jpg',
        },
        { text: "Here's to more in 2027.", image: '/wormhole/tiles/x20261229-v2-4.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-24 x20261231 back to visual v2',
    post: 'x20261231',
    set: {
      slides: [
        { text: 'Happy New Year from the soil.', image: '/wormhole/tiles/x20261231-v2-1.jpg' },
        { text: 'Costa Rica, 18 to 29 January.', image: '/wormhole/tiles/x20261231-v2-2.jpg' },
        { text: 'New Mexico, 3 to 14 May.', image: '/wormhole/tiles/x20261231-v2-3.jpg' },
        { text: 'United Kingdom, September.', image: '/wormhole/tiles/x20261231-v2-4.jpg' },
      ],
    },
    reason: 'Back to the v2 photo-and-tag visual (Linnea, 24 Oct: "i liked what you had").',
  },
  {
    key: '2026-10-26 new wd20270308',
    post: 'wd20270308',
    create: {
      iso_date: '2027-03-08',
      date_tbd: false,
      topic: "International Women's Day: watch Women Seeding Regenerative Futures",
      platform: 'Instagram, Facebook',
      caption:
        'Today is International Women\'s Day. Spend an hour with four women who teach people to work with living soil.\n\n"Women Seeding Regenerative Futures" is an all-woman panel on permaculture, soil and community, recorded live on 2 September 2026 and free to watch.\n\nClea Chandmal brings permaculture science rooted in plant molecular physiology.\n\nKelda Lorax brings 30 years of permaculture education and a deep commitment to justice in land relationships.\n\nDr. Carla Portugal brings research across Brazil and the United States, and years at the Soil Food Web School as an instructor, mentor and translator.\n\nKavi Reddy brings systems thinking across soil fertility, food systems and global partnerships.\n\nAudience questions steered the conversation, so it stays practical: how to design land, food and community around a living soil.\n\nWatch the replay. Link in bio.\n[replay link: Ivan\'s YouTube upload of Video 6]\nhttps://webinar.soilfoodweb.com/webinar-women-seeding-regenerative-futures\n\n@coursesbyclea @keldalorax @carlamacport @kavilovesyou @visionary_permaculture\n\n#InternationalWomensDay #WomenInAg #Permaculture #PermacultureDesign #SoilFoodWeb #LivingSoil #RegenerativeAgriculture',
      slides: [
        {
          text: "International Women's Day. Four women on permaculture, soil and community.",
          image: '/wormhole/tiles/wd20270308-v1-1.jpg',
        },
        {
          text: 'The panel: Clea Chandmal, Kelda Lorax, Dr. Carla Portugal, Kavi Reddy.',
          image: '/wormhole/tiles/wd20270308-v1-2.jpg',
        },
        {
          text: 'Watch the full panel. Link in bio.',
          image: '/wormhole/tiles/wd20270308-v1-3.jpg',
        },
      ],
      cta: 'Watch the replay',
      link: 'https://webinar.soilfoodweb.com/webinar-women-seeding-regenerative-futures',
      sources: [
        'September 2026 Social Media Planning Doc, Sep 2 webinar caption (panelist descriptions)',
        'August 2026 Social Media Planning Doc, Aug 27 promo (handles, panel description)',
        'Drive: Video Editing | Ivan > Video 6: Women Seeding Regenerative Futures (recording)',
      ],
      visual_note:
        'Family: I, portrait. Built with tools/wormhole-visuals/iwd.py (deck: 08-03-2027-iwd-women-seeding-regenerative-futures-v1.pptx). Deep green ground, Montserrat, Pathway Gothic One, Source Sans 3. Real portraits of Carla (website team photo) and Kavi (team photo). Clea and Kelda have labelled PHOTO circles: ask them for a portrait, or crop them from the Sept 2nd Webinar Panel.png graphic on Drive. Optional: a 30-second clip from the replay as a Reel cover.',
      note: 'Pillar: TEACH IT + GROW IT. To do before posting: (1) replay link once Ivan uploads Video 6 to YouTube, with UTM; (2) portraits of Clea and Kelda; (3) send collab invites (Clea, Kelda, Carla, Kavi, Delvin as series co-host). The old graphics say 9am PST; it was 9am PDT. The March planning note asks for Dr. Elaine and women in soil science on IWD, so a second IWD post (Stories) could cover that.',
      status: 'draft',
    },
    reason:
      "New post (Linnea, 26 Oct): International Women's Day post to watch the Women Seeding Regenerative Futures webinar.",
  },
  {
    key: '2026-10-27 new wd20270308b',
    post: 'wd20270308b',
    create: {
      iso_date: '2027-03-08',
      date_tbd: false,
      topic: "International Women's Day: Dr. Elaine Ingham and women in soil science",
      platform: 'Instagram, Facebook',
      caption:
        'Today is International Women\'s Day, and we\'re remembering the scientist who started all of this.\n\nDr. Elaine Ingham trained in microbiology at Texas A&M and earned her doctorate at Colorado State University. At Oregon State University from 1986, her research developed the concept of the soil food web: the bacteria, fungi, protozoa, nematodes and micro-arthropods that feed plants and build soil.\n\nShe wrote the Soil Biology Primer for the USDA Natural Resources Conservation Service, then spent decades teaching microscopy, compost and compost tea to growers around the world.\n\nWomen carry her science on today. Loida Vasquez, our Director of Advanced Education, tells students: "The most is learned from failed piles."\n\nWho is the woman who taught you about soil? Tag her below.\n\nStart learning the soil food web. Link in bio.\nhttps://school.soilfoodweb.com/collections\n\n#InternationalWomensDay #WomenInScience #ElaineIngham #SoilFoodWeb #SoilBiology #LivingSoil',
      slides: [
        {
          text: "International Women's Day. Dr. Elaine Ingham developed the concept of the soil food web.",
          image: '/wormhole/tiles/wd20270308b-v1-1.jpg',
        },
        {
          text: 'A scientist first: St. Olaf College, Texas A&M, Colorado State, Oregon State University from 1986.',
          image: '/wormhole/tiles/wd20270308b-v1-2.jpg',
        },
        {
          text: 'Then she taught it: the Soil Biology Primer, microscopy, compost and compost tea.',
          image: '/wormhole/tiles/wd20270308b-v1-3.jpg',
        },
        {
          text: 'The women teaching it now: Loida Vasquez, Director of Advanced Education.',
          image: '/wormhole/tiles/wd20270308b-v1-4.jpg',
        },
        {
          text: 'Start learning the soil food web. Link in bio.',
          image: '/wormhole/tiles/wd20270308b-v1-5.jpg',
        },
      ],
      cta: 'Start learning',
      link: 'https://school.soilfoodweb.com/collections',
      sources: [
        'Obituary for Dr. Elaine Ingham, soilfoodweb.com/obituary-for-dr-elaine-ingham (education, Oregon State 1986 to 2002, Soil Biology Primer, "developed the concept of the soil food web")',
        "CLAUDE.md section 10: Loida Vasquez's line and title (India workshop course page)",
        'Website copy deck: the five organism groups of the soil food web',
      ],
      visual_note:
        "Family: D, full-bleed photo. Built with tools/wormhole-visuals/iwd.py (deck: 08-03-2027-iwd-dr-elaine-women-in-soil-science-v1.pptx). Our own photos of Dr. Elaine (microscope portrait, garden, Costa Rica workshop, nematode extraction) and Loida's team photo, edge to edge, with a cream strip and a thin Legacy Mulberry bar (Dr. Elaine content only). Montserrat, Pathway Gothic One, Source Sans 3. Same day as wd20270308 (Family I, deep green), so the two look different side by side in the grid.",
      note: "Pillar: PROVE IT + TEACH IT. Second International Women's Day post (Linnea, 27 Oct: two posts that day is fine), answering the March planning note: highlight Dr. Elaine Ingham and women in soil science. Post it after the panel post, or in the evening window. Add a UTM to the link before posting. Optional: check with Loida that she's happy to be quoted.",
      status: 'draft',
    },
    reason:
      "New post (Linnea, 27 Oct): second International Women's Day post on Dr. Elaine Ingham and women in soil science.",
  },
  {
    key: '2026-10-27 wd20270308b v2 no loida',
    post: 'wd20270308b',
    set: {
      slides: [
        {
          text: "International Women's Day. Dr. Elaine Ingham developed the concept of the soil food web.",
          image: '/wormhole/tiles/wd20270308b-v2-1.jpg',
        },
        {
          text: 'A scientist first: St. Olaf College, Texas A&M, Colorado State, Oregon State University from 1986.',
          image: '/wormhole/tiles/wd20270308b-v2-2.jpg',
        },
        {
          text: 'Then she taught it: the Soil Biology Primer, microscopy, compost and compost tea.',
          image: '/wormhole/tiles/wd20270308b-v2-3.jpg',
        },
        {
          text: 'Start learning the soil food web. Link in bio.',
          image: '/wormhole/tiles/wd20270308b-v2-4.jpg',
        },
      ],
      sources: [
        'Obituary for Dr. Elaine Ingham, soilfoodweb.com/obituary-for-dr-elaine-ingham (education, Oregon State 1986 to 2002, Soil Biology Primer, "developed the concept of the soil food web")',
        'Website copy deck: the five organism groups of the soil food web',
        'CLAUDE.md Foundation facts: 10,000+ people enrolled across 100+ countries',
      ],
      visual_note:
        'Family: D, full-bleed photo. Built with tools/wormhole-visuals/iwd.py (deck: 08-03-2027-iwd-dr-elaine-ingham-v2.pptx). Four slides, all Dr. Elaine: our own photos (microscope portrait, garden, Costa Rica workshop, nematode extraction) edge to edge, with a cream strip and a thin Legacy Mulberry bar (Dr. Elaine content only). Montserrat, Pathway Gothic One, Source Sans 3. Same day as wd20270308 (Family I, deep green).',
    },
    caption: [
      [
        'Women carry her science on today. Loida Vasquez, our Director of Advanced Education, tells students: "The most is learned from failed piles."',
        'Her students now carry the science on in more than 100 countries.',
      ],
    ],
    reason:
      'Linnea, 27 Oct: Loida out of the Elaine post and the "failed piles" quote removed. Now four slides, all Dr. Elaine (v2 tiles). Ignore the older note about checking the quote with Loida.',
  },
  {
    key: '2026-10-27 cr20261116 drop failed piles quote',
    post: 'cr20261116',
    set: {
      slides: [
        { text: 'Some piles are built to fail.', image: '/wormhole/tiles/cr20261116-v1-1.jpg' },
        { text: 'On purpose.', image: '/wormhole/tiles/cr20261116-v1-2.jpg' },
        {
          text: 'Students build several piles at once, some designed to go wrong.',
          image: '/wormhole/tiles/cr20261116-v1-3.jpg',
        },
        {
          text: 'Then they diagnose them and turn them around.',
          image: '/wormhole/tiles/cr20261116-v1-4.jpg',
        },
        {
          text: 'Costa Rica, 18 to 29 January 2027.',
          image: '/wormhole/tiles/cr20261116-v1-6.jpg',
        },
      ],
    },
    caption: [[' As Loida Vasquez says, the most is learned from failed piles.', '']],
    reason:
      'Linnea, 27 Oct: never use the "failed piles" quote. Dropped the quote slide (was slide 5) and the line in the caption.',
  },
  {
    key: '2026-10-27 p18 single image',
    post: 'p18',
    set: {
      slides: [{ text: 'Vampire amoeba.', image: '/wormhole/tiles/p18-v5-1.jpg' }],
      visual_note:
        'Family: F, specimen. Single image: the title, two real micrographs of Vampyrella lateritia in round lenses on deep green, a moon, and the credit (Hess, Sausen & Melkonian 2012, PLoS ONE, CC BY 4.0).',
    },
    reason:
      "One image, not a carousel (Linnea, 27 Oct): only the cover. The caption already points to Wes's blog post. The three other slides stay in the post's history.",
  },
  {
    key: '2026-10-27 p18 v6 white logo no credit',
    post: 'p18',
    set: {
      slides: [{ text: 'Vampire amoeba.', image: '/wormhole/tiles/p18-v6-1.jpg' }],
      visual_note:
        'Family: F, specimen. Single image: the title, two real micrographs of Vampyrella lateritia in round lenses on deep green, a moon, and the white SFW logo. No credit on the image; the CC BY 4.0 credit (Hess, Sausen & Melkonian 2012, PLoS ONE) is in the caption, which satisfies the licence.',
    },
    reason:
      'Linnea, 27 Oct: one image, without the licence line, and with the white logo. v6 is the v5 cover with the credit line removed (background filled, root lines rejoined) and the white logo in place of the colour logo in its circle. The credit stays in the caption.',
  },
  {
    key: '2026-10-27 j20270101 variety v5',
    post: 'j20270101',
    set: {
      slides: [
        {
          text: 'HAPPY NEW YEAR Welcome to 2027. Costa Rica JANUARY New Mexico MAY United Kingdom SEPTEMBER',
          image: '/wormhole/tiles/j20270101-v5-1.jpg',
        },
        {
          text: 'OUR 2027 WORKSHOPS See you in the field. All 2027 workshops, link in bio.',
          image: '/wormhole/tiles/j20270101-v5-2.jpg',
        },
      ],
      visual_note:
        'Family: G, type only. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Real SFW workshop photos: group under the bunting (cy-workshop-8), a workshop group in a barn (IMG_1942), building piles at Wild Ken Hill, a workshop group around a fresh pile.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: G, type only), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270102 variety v5',
    post: 'j20270102',
    set: {
      slides: [
        {
          text: 'DO THIS WEEKEND Stay off wet beds. Wet soil under a boot: pores pressed shut. A board spreads the weight: the crumb stays open. Walk on boards or a mulched path instead.',
          image: '/wormhole/tiles/j20270102-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: H, diagram. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Aerial view of mulched beds and a path (Rancho Cacachilas), then mushrooms in mulched soil under grape vines.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: H, diagram), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270103 variety v5',
    post: 'j20270103',
    set: {
      slides: [
        {
          text: 'COMPOST INTENSIVE COURSE The January cohort starts this month. Link in bio.',
          image: '/wormhole/tiles/j20270103-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: K, framed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: A student squeezing compost to test it, a student lifting finished compost while a pile is hosed, sample tubes at the microscope.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: K, framed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270104 variety v5',
    post: 'j20270104',
    set: {
      slides: [
        {
          text: 'READ THE DROP Meet the naked amoeba. NAKED AMOEBA, 40X OBJECTIVE',
          image: '/wormhole/tiles/j20270104-v5-1.jpg',
        },
        {
          text: 'It eats bacteria and releases ammonium by the roots.',
          image: '/wormhole/tiles/j20270104-v5-2.jpg',
        },
      ],
      visual_note:
        'Family: F, specimen. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Reel, 15 to 20 seconds. Cover and second frame: the naked amoeba microscopy cutout from the science page, on white and on cream. Swap in a live microscope clip of a moving amoeba if the library has one.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: F, specimen), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270105 variety v5',
    post: 'j20270105',
    set: {
      slides: [
        {
          text: 'MEET THE TEAM Evan Buckman EXECUTIVE DIRECTOR',
          image: '/wormhole/tiles/j20270105-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: I, portrait. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Evan's site portrait (w_evan.jpg) above a Foundation tree-planting photo. The lower photo is a general Foundation field photo; swap in one of Evan's own if he has one.",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: I, portrait), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270106 variety v5',
    post: 'j20270106',
    set: {
      slides: [
        {
          text: 'SOIL REGENERATORS IN THE WILD Roberto Silva and consultant Miles Sorel Piura, Peru',
          image: '/wormhole/tiles/j20270106-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: D, full-bleed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Still from Roberto's case study film (Vimeo 790985081 poster): two men walking the grape rows. Ask Miles or Roberto for a field photo to make it a carousel. Instagram Collab with Miles Sorel / Terraforma [VERIFY handles].",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: D, full-bleed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270107 variety v5',
    post: 'j20270107',
    set: {
      slides: [
        {
          text: 'MYTH VS MECHANISM Myth: soil life sleeps all winter. SNOW',
          image: '/wormhole/tiles/j20270107-v5-1.jpg',
        },
        {
          text: 'THE MECHANISM Under the snow, microbes keep growing. bacteria still dividing around the roots',
          image: '/wormhole/tiles/j20270107-v5-2.jpg',
        },
      ],
      visual_note:
        'Family: H, diagram. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Soil sampling kit, a drop of soil water under the microscope, protozoa in a sample.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: H, diagram), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270108 variety v5',
    post: 'j20270108',
    set: {
      slides: [
        {
          text: 'MEET THE TEAM Stephanie McDaniel Director of Communications',
          image: '/wormhole/tiles/j20270108-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: K, framed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Stephanie's site portrait (w_stephanie.jpg) above workshop graduates holding their certificates (August 2023).",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: K, framed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270109a variety v5',
    post: 'j20270109a',
    set: {
      slides: [
        {
          text: 'DO THIS WEEKEND Plan your cover crops. Legumes add nitrogen. Grasses hold on to it. Mix both.',
          image: '/wormhole/tiles/j20270109a-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: D, full-bleed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Field rows and hoop houses, a tree over a green understory, an aerial view of a regenerating site (Rancho Cacachilas photos from the site).',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: D, full-bleed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270110a variety v5',
    post: 'j20270110a',
    set: {
      slides: [
        {
          text: 'PERMACULTURE PRINCIPLE 1 Observe and interact. Watch first, then design.',
          image: '/wormhole/tiles/j20270110a-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: K, framed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: A mandala garden from above (Panchamana), then people planting trees.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: K, framed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270110c variety v5',
    post: 'j20270110c',
    set: {
      slides: [
        {
          text: 'COMPOST INTENSIVE COURSE Last call. The January cohort starts the week of 18 January. Link in bio.',
          image: '/wormhole/tiles/j20270110c-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: G, type only. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: A workshop group with their finished pile in the Wild Ken Hill barn (IMG_1497), then an organism cutout on cream with the start date. [CONFIRM: enrollment close date for the January cohort]',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: G, type only), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270111 variety v5',
    post: 'j20270111',
    set: {
      slides: [
        {
          text: 'One week to go. Accelerator Workshop, Costa Rica, 18 to 29 January at Armonía.',
          image: '/wormhole/tiles/j20270111-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: L, photo grid. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Real 2025 Costa Rica photos: students and mentors at the microscopes, mentor Gerald Ramirez demonstrating liquid amendments. Instagram Collab with Armonía (@armoniaagriculturaorganica).',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: L, photo grid), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270112 variety v5',
    post: 'j20270112',
    set: {
      slides: [
        {
          text: 'SOIL IN NUMBERS 1,000,000 protozoa can live in one teaspoon of highly fertile soil. Poor soil holds about 1,000.',
          image: '/wormhole/tiles/j20270112-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: B, big number. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Protozoa under the microscope (science page image), then an instructor teaching soil biology.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: B, big number), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270113 variety v5',
    post: 'j20270113',
    set: {
      slides: [
        {
          text: 'MEET THE TEAM Sammie Bass MARKETING ASSOCIATE',
          image: '/wormhole/tiles/j20270113-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: I, portrait. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Sammie's site portrait with her chicken (w_sammie.jpg) above workshop participants at Wild Ken Hill.",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: I, portrait), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270114 variety v5',
    post: 'j20270114',
    set: {
      slides: [
        {
          text: 'FREE WEBINARS New Year Series JAN TO MAR 2027 One live hour online, free. Ask your questions live. LINK IN BIO',
          image: '/wormhole/tiles/j20270114-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: M, event card. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Community members planting together in a garden, a hand holding soil with roots (webinar preview photos). Add the speaker's headshot as slide 2 once the January webinar is confirmed.",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: M, event card), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270115 variety v5',
    post: 'j20270115',
    set: {
      slides: [
        {
          text: 'MEET THE TEAM Alex Andreou IT Manager',
          image: '/wormhole/tiles/j20270115-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: K, framed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Alex's site portrait (w_alex.jpg, a 320 px selfie with two family members) above students in a workshop classroom. Ask Alex for a larger solo portrait before this goes out.",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: K, framed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270115b variety v5',
    post: 'j20270115b',
    set: {
      slides: [
        {
          text: '15 JANUARY Happy Pongal to every farmer in Tamil Nadu, and to the soil that feeds the harvest.',
          image: '/wormhole/tiles/j20270115b-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: G, type only. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Swap in a real Coimbatore workshop photo from Kavi Reddy when the October footage arrives.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: G, type only), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270116 variety v5',
    post: 'j20270116',
    set: {
      slides: [
        {
          text: '1 Sow 100 radish or cress seeds in moist compost.',
          image: '/wormhole/tiles/j20270116-v5-1.jpg',
        },
        {
          text: '2 Keep it moist and in the light for 5 to 10 days.',
          image: '/wormhole/tiles/j20270116-v5-2.jpg',
        },
        {
          text: '3 80 or more sprouts: the compost is likely mature.',
          image: '/wormhole/tiles/j20270116-v5-3.jpg',
        },
      ],
      visual_note:
        'Family: J, numbered steps. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Hands holding compost and soil (photos from the new SFW site).',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: J, numbered steps), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270117 variety v5',
    post: 'j20270117',
    set: {
      slides: [
        {
          text: 'ACCELERATOR WORKSHOP, COSTA RICA Tomorrow we start. Week one: compost. Week two: biological liquid amendments.',
          image: '/wormhole/tiles/j20270117-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: D, full-bleed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Real 2025 Costa Rica photos from the Costa Rica decks: students cheering over a finished pile, students with buckets outdoors. No prices.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: D, full-bleed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270118b variety v5',
    post: 'j20270118b',
    set: {
      slides: [
        {
          text: 'FOUNDATION COURSES Learn to identify the four groups. BACTERIA (DRAWN) FUNGI PROTOZOA NEMATODES Start any time. Link in bio.',
          image: '/wormhole/tiles/j20270118b-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: F, specimen. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Dr. Elaine Ingham at her microscope (green tag, no purple), then a testate amoeba at 40x (Photo: Joy Kaluf, a different frame from the one on j20270110b).',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: F, specimen), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270119 variety v5',
    post: 'j20270119',
    set: {
      slides: [
        {
          text: 'MEET THE TEAM Leslie W. Lewis, Ph.D. EXECUTIVE COMMITTEE',
          image: '/wormhole/tiles/j20270119-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: I, portrait. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Leslie's site portrait (w_leslie.jpg).",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: I, portrait), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270119b variety v5',
    post: 'j20270119b',
    set: {
      slides: [
        {
          text: 'NEW COURSE Intro to Permaculture opens 1 February.',
          image: '/wormhole/tiles/j20270119b-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: K, framed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Volunteers planting trees between tall eucalyptus at Panchamana (ERC). [CONFIRM: course page link and details before this goes out]',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: K, framed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270120 variety v5',
    post: 'j20270120',
    set: {
      slides: [
        {
          text: 'SOIL REGENERATORS IN THE WILD TrashIt, Pakistan Soil Health Week 2025',
          image: '/wormhole/tiles/j20270120-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: C, article card. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Top: the Soil Health Week 2025 group photo with Nick Padwick (site file Screenshot-2025-10-22-212600.jpg, Nick still to confirm who is in it and permission, per docs/image-decisions.md). Bottom: SFW sample tubes. Instagram Collab with TrashIt (trashit.pk) and Wild Soils UK [VERIFY handles].',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: C, article card), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270121 variety v5',
    post: 'j20270121',
    set: {
      slides: [
        {
          text: 'MYTH VS MECHANISM Myth: add sand to loosen clay soil. Sand in clay packs tight and can set hard.',
          image: '/wormhole/tiles/j20270121-v5-1.jpg',
        },
        {
          text: 'THE MECHANISM Add organic matter and let soil life build the crumb. Fungal threads and microbial glues hold crumbs together, with air and water between.',
          image: '/wormhole/tiles/j20270121-v5-2.jpg',
        },
      ],
      visual_note:
        "Family: H, diagram. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Field photos of residue and earthworms in crumb soil at York Farms (Harrington's Organic Land Care; written permission still open per docs/handoff-alex.md).",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: H, diagram), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270121b variety v5',
    post: 'j20270121b',
    set: {
      slides: [
        {
          text: 'ACCELERATOR WORKSHOP, NEW MEXICO 3 to 14 May 2027 Register your interest. Link in bio.',
          image: '/wormhole/tiles/j20270121b-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: G, type only. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: No New Mexico photos exist in the photo set or the repo, so both slides are organism cutouts on cream and white (a nematode, a testate amoeba) that show no place. Swap in real Synergia Ranch photos (the event page hero IMG_3426) when Evan sends them. [CONFIRM: New Mexico photos from Evan; whether a school enrollment page exists yet]',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: G, type only), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270122 variety v5',
    post: 'j20270122',
    set: {
      slides: [
        {
          text: 'LIVE FROM COSTA RICA Building the piles.',
          image: '/wormhole/tiles/j20270122-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: D, full-bleed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Real 2025 Costa Rica photos: building a pile in a wire cage, hydrating a pile with a hose. Swap in live photos from Kavi or the mentors on the day.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: D, full-bleed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270123b variety v5',
    post: 'j20270123b',
    set: {
      slides: [
        {
          text: '1 Reach into the pile and squeeze a handful tight.',
          image: '/wormhole/tiles/j20270123b-v5-1.jpg',
        },
        {
          text: '2 A wet sheen and no drips: right where you want it.',
          image: '/wormhole/tiles/j20270123b-v5-2.jpg',
        },
        {
          text: '3 Drips mean too wet. Dry and dusty means too dry.',
          image: '/wormhole/tiles/j20270123b-v5-3.jpg',
        },
      ],
      visual_note:
        'Family: J, numbered steps. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: A student squeezing compost at an SFW workshop (site photo ctpfw-student-squeezing-compost-1.jpg).',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: J, numbered steps), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270124 variety v5',
    post: 'j20270124',
    set: {
      slides: [
        {
          text: "FIELD NOTES No. 03 Trial name, place and season. PHOTO: the graduate's own trial photo",
          image: '/wormhole/tiles/j20270124-v5-1.jpg',
        },
        {
          text: "FIELD NOTES No. 03 The question they tested. PHOTO: the graduate's own trial photo",
          image: '/wormhole/tiles/j20270124-v5-2.jpg',
        },
        {
          text: "FIELD NOTES No. 03 The method in 3 lines. PHOTO: the graduate's own trial photo",
          image: '/wormhole/tiles/j20270124-v5-3.jpg',
        },
        {
          text: "FIELD NOTES No. 03 The result, one big number. PHOTO: the graduate's own trial photo",
          image: '/wormhole/tiles/j20270124-v5-4.jpg',
        },
        {
          text: "FIELD NOTES No. 03 What surprised them, including what didn't work. PHOTO: the graduate's own trial photo",
          image: '/wormhole/tiles/j20270124-v5-5.jpg',
        },
        {
          text: "FIELD NOTES No. 03 Who ran it. PHOTO: the graduate's own trial photo",
          image: '/wormhole/tiles/j20270124-v5-6.jpg',
        },
      ],
      visual_note:
        "Family: N, field notebook. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Carousel, 6 slides, same layout as Field Notes #1 and #2, with v2 stand-in photos (soil sampling, sample tube, Foundation sampling kit, field planting, York Farms residue, hands planting). Graduate trial still to pick: swap every slide for the graduate's own trial photos.",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: N, field notebook), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270125 variety v5',
    post: 'j20270125',
    set: {
      slides: [
        {
          text: 'READ THE DROP Spores or hyphae? SPORES: FUNGI ON PAUSE HYPHAE: FUNGI AT WORK',
          image: '/wormhole/tiles/j20270125-v5-1.jpg',
        },
        {
          text: 'Hyphae on your slide mean fungi growing and working now.',
          image: '/wormhole/tiles/j20270125-v5-2.jpg',
        },
      ],
      visual_note:
        'Family: F, specimen. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Reel, 15 to 20 seconds, 3 v2 frames: fungal spores in suspension under the microscope (Foundation micrograph), a soil crumb held together by roots and fungal strands, fungi fruiting under vines.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: F, specimen), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270125b variety v5',
    post: 'j20270125b',
    set: {
      slides: [
        {
          text: 'FOUNDATION COURSES 10,000+ people in more than 100 countries started here.',
          image: '/wormhole/tiles/j20270125b-v5-1.jpg',
        },
        {
          text: 'FOUNDATION COURSES Start any time, at your own pace. Link in bio.',
          image: '/wormhole/tiles/j20270125b-v5-2.jpg',
        },
      ],
      visual_note:
        'Family: B, big number. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: A big workshop group around their pile under a shed roof (uploads_mar-group-photo-2, tag at the top so no faces are covered), then crop rows and hoop houses at Rancho Cacachilas.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: B, big number), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270126 variety v5',
    post: 'j20270126',
    set: {
      slides: [
        {
          text: 'LIVE FROM COSTA RICA At the microscope. PHOTO: live, from the microscopes on the day (Kavi or the mentors)',
          image: '/wormhole/tiles/j20270126-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: K, framed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Real 2025 Costa Rica photos: students and mentors at the microscopes, a liquid amendments demonstration. Swap in live photos from Kavi or the mentors on the day.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: K, framed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270127 variety v5',
    post: 'j20270127',
    set: {
      slides: [
        {
          text: 'PERMACULTURE PRINCIPLE 6 Produce no waste. PRUNINGS MULCH LIVING SOIL PLANTS Prunings become mulch, scraps become compost.',
          image: '/wormhole/tiles/j20270127-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: H, diagram. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: A finished compost pile topped with flowers at an SFW workshop, gloved hands in a bucket of woody mulch.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: H, diagram), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270128 variety v5',
    post: 'j20270128',
    set: {
      slides: [
        {
          text: 'SOIL IN NUMBERS 95% of our food is produced in soil.',
          image: '/wormhole/tiles/j20270128-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: B, big number. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Corn residue and crumb soil at York Farms (Harrington's Organic Land Care), an aerial view of the Rancho Cacachilas agroforest restoration (Ecosystem Restoration Camps).",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: B, big number), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270128b variety v5',
    post: 'j20270128b',
    set: {
      slides: [
        {
          text: '1 Build, monitor and maintain your piles with a mentor. NEW MEXICO, 3 TO 14 MAY 2027',
          image: '/wormhole/tiles/j20270128b-v5-1.jpg',
        },
        {
          text: '2 Brew a variety of liquid amendments. NEW MEXICO, 3 TO 14 MAY 2027',
          image: '/wormhole/tiles/j20270128b-v5-2.jpg',
        },
        {
          text: '3 Microscopy sessions for beginner and advanced practitioners. NEW MEXICO, 3 TO 14 MAY 2027',
          image: '/wormhole/tiles/j20270128b-v5-3.jpg',
        },
      ],
      visual_note:
        'Family: J, numbered steps. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: A hand holding finished compost, a ciliate cutout on white, protozoa in soil water under the microscope. No New Mexico photos exist yet, so nothing shows a place. Swap in Synergia Ranch photos when Evan sends them. [CONFIRM: New Mexico photos from Evan]',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: J, numbered steps), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270129 variety v5',
    post: 'j20270129',
    set: {
      slides: [
        {
          text: 'COSTA RICA, JANUARY 2027 Thank you, Costa Rica, and thank you, Armonía.',
          image: '/wormhole/tiles/j20270129-v5-1.jpg',
        },
      ],
      visual_note:
        'Family: D, full-bleed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Real 2025 Costa Rica photos: graduates with a certificate, the whole group around their pile. Swap in live photos from Kavi or the mentors on the day. Instagram Collab with Armonía (@armoniaagriculturaorganica), like cr20261102.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: D, full-bleed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270130 variety v5',
    post: 'j20270130',
    set: {
      slides: [
        {
          text: 'FUN SOIL NEWS January 2027. Three good stories from the soil this month.',
          image: '/wormhole/tiles/j20270130-v5-1.jpg',
        },
        {
          text: 'BRAZIL R$250 million to turn 4,000 hectares of degraded land into cocoa agroforests.',
          image: '/wormhole/tiles/j20270130-v5-2.jpg',
        },
        {
          text: "UNITED STATES USDA's Regenerative Pilot Program grows to $1 billion.",
          image: '/wormhole/tiles/j20270130-v5-3.jpg',
        },
        {
          text: 'GERMANY Forest soils took up about 3% more methane each year.',
          image: '/wormhole/tiles/j20270130-v5-4.jpg',
        },
      ],
      visual_note:
        'Family: G, type only. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Hands in soil photos from the new SFW site. Three verified stories; add a fourth or fifth in December only if it can be verified.',
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: G, type only), no photo used twice.',
  },
  {
    key: '2026-10-27 j20270131 variety v5',
    post: 'j20270131',
    set: {
      slides: [
        {
          text: 'MEET THE TEAM Ib Borup Pedersen Farmer, Soil Food Web Consultant and mentor',
          image: '/wormhole/tiles/j20270131-v5-1.jpg',
        },
      ],
      visual_note:
        "Family: K, framed photo. Built with tools/wormhole-visuals/jan_varied.py (27 Oct variety rebuild; replaces the photo-and-tag v2 tiles). Every photo checked with photo_check.py: used on no other post. Earlier note: Ib's site portrait (w_ib.jpg).",
    },
    reason:
      'Linnea, 27 Oct: no more one template across the feed. January rebuilt with a different family per post (Family: K, framed photo), no photo used twice.',
  },
  {
    key: '2026-10-27 p18 v7 real white logo',
    post: 'p18',
    set: {
      slides: [{ text: 'Vampire amoeba.', image: '/wormhole/tiles/p18-v7-1.jpg' }],
      visual_note:
        'Family: F, specimen. Single image: the title, two real micrographs of Vampyrella lateritia in round lenses on deep green, a moon, and the official white SFW Foundation logo (wormhole/brand/sfw-foundation-logo-white.png) on plain green. No credit on the image; the CC BY 4.0 credit (Hess, Sausen & Melkonian 2012, PLoS ONE) is in the caption.',
    },
    reason:
      'Linnea, 27 Oct: the official white logo file, with no root lines behind it, and no licence line on the image.',
  },
  {
    key: '2026-10-28 cr20261116 no built to fail',
    post: 'cr20261116',
    set: {
      topic: 'Costa Rica: several piles, different recipes',
      slides: [
        { text: 'Several piles, different recipes.', image: '/wormhole/tiles/cr20261116-v2-1.jpg' },
        { text: 'Every pile behaves differently.', image: '/wormhole/tiles/cr20261116-v2-2.jpg' },
        {
          text: 'Students build several piles at once. Each team picks its feedstocks and works out its own recipe.',
          image: '/wormhole/tiles/cr20261116-v2-3.jpg',
        },
        {
          text: 'Then you read each pile and adjust it. With a mentor beside you.',
          image: '/wormhole/tiles/cr20261116-v2-4.jpg',
        },
        {
          text: 'Costa Rica, 18 to 29 January 2027.',
          image: '/wormhole/tiles/cr20261116-v1-6.jpg',
        },
      ],
      visual_note:
        'Carousel, real photos from past Costa Rica workshops. Deck: /wormhole/decks/16-11-2026-costa-rica-pile-recipes.pptx. No prices.',
    },
    captionText:
      'At our Costa Rica workshop, students build several thermal compost piles at the same time, each with a different recipe. 🔥\nEvery day you check the temperature and moisture of each pile, compare how they change, and learn what to adjust and when to turn, with a mentor beside you.\nAccelerator Workshop, 18 to 29 January 2027. Register now, link in bio.\n#SoilFoodWeb #CostaRica #Compost #Workshop',
    reason:
      'Linnea, 28 Oct: never use the term "built to fail". Pile posts now say several piles, different recipes.',
  },
  {
    key: '2026-10-28 st20261116 no built to fail',
    post: 'st20261116',
    set: {
      topic: 'Costa Rica stories · Several piles, different recipes',
      slides: [
        {
          text: 'Story frame 5 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261116-v2-1.jpg',
        },
      ],
      visual_note:
        'Frame 5 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027-v2.pptx. Post around 8:00am Pacific. No prices.',
    },
    reason:
      'Linnea, 28 Oct: never use the term "built to fail". Pile posts now say several piles, different recipes.',
  },
  {
    key: '2026-10-28 st20261029 no built to fail',
    post: 'st20261029',
    set: {
      slides: [
        {
          text: 'Story frame 4 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261029-v1-1.jpg',
        },
        {
          text: 'Story frame 5 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261029-v2-2.jpg',
        },
        {
          text: 'Story frame 7 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261029-v1-3.jpg',
        },
        {
          text: 'Story frame 8 of the Costa Rica set (9:16, shown smaller here).',
          image: '/wormhole/tiles/st20261029-v1-4.jpg',
        },
      ],
      visual_note:
        'Frames 4, 5, 7, 8 from /wormhole/decks/26-10-2026-ig-stories-costa-rica-2027-v2.pptx. Post around 8:00am Pacific. No prices.',
    },
    caption: [['Would you rescue a failing pile?', 'Which recipe would you try first?']],
    reason:
      'Linnea, 28 Oct: never use the term "built to fail". Pile posts now say several piles, different recipes.',
  },
  {
    key: '2026-10-28 j20270122 no built to fail',
    post: 'j20270122',
    caption: [
      [
        'Some piles are built to go wrong, so you learn to read a struggling pile and rescue it with a mentor beside you.',
        "Each team's recipe behaves differently, so you learn to read a pile and adjust it with a mentor beside you.",
      ],
    ],
    reason:
      'Linnea, 28 Oct: never use the term "built to fail". Pile posts now say several piles, different recipes.',
  },
  {
    key: '2026-10-28 web20261030 Matt Drane visual',
    post: 'web20261030',
    set: {
      slides: [
        {
          text: 'Version 1: FREE WEBINAR, Fall 2026 series. 15 years of regenerative transformation in broad-acre corn and soy, with Matt Drane, AgriBio Systems. Wednesday, November 4, 9am Pacific, 11am Central, Noon Eastern. Register free, link in bio.',
          image: '/wormhole/tiles/web20261030-v1-1.jpg',
        },
        {
          text: 'Version 2: FREE WEBINAR, Fall 2026 series. 15 years of regenerative transformation in broad-acre corn and soy farming, with Matt Drane, AgriBio Systems. Wednesday, November 4. Register free, link in bio.',
          image: '/wormhole/tiles/web20261030-v1-2.jpg',
        },
        {
          text: 'Version 3: same text, photo top right and a dark green text block.',
          image: '/wormhole/tiles/web20261030-v1-3.jpg',
        },
      ],
      visual_note:
        'Three versions to pick one from, single image post. Matt Drane photo with corn and soy leaf graphics. Deck: /wormhole/decks/30-10-2026-webinar-preview-matt-drane-3-versions.pptx (one version per slide, editable in Canva).',
    },
    reason: 'Linnea, 28 Oct: webinar visual with Matt Drane photo, three versions.',
  },
  {
    key: '2026-10-30 d13 single image with portrait',
    post: 'd13',
    set: {
      slides: [
        {
          text: 'Meet our mentors: Tommy Tepper, Director of Education',
          image: '/wormhole/tiles/d13-v2-1.jpg',
        },
      ],
      visual_note:
        "Family: I, portrait. Single image (Linnea, 30 Oct: not a carousel). Slide 1 of Linnea's deck Meet-our-mentors-Tommy-Tepper.pptx: Food Web Green, MEET OUR MENTORS label, Tommy's photo in a circle, name and role.",
    },
    reason:
      "Linnea, 30 Oct: one image with Tommy's photo (the old tile had no picture of him). From slide 1 of her deck.",
  },
  {
    key: '2026-10-30 p02 flower frame',
    post: 'p02',
    set: {
      slides: [
        { text: 'Meet our mentors Casey Williams', image: '/wormhole/tiles/p02-ff-1.jpg' },
        {
          text: '\u201cI am deeply grateful that I get to learn from my students as well as teach them.\u201d A bacterial-feeding nematode at 40x, photographed by Casey.',
          image: '/wormhole/tiles/p02-2.jpg',
        },
        {
          text: 'His advice: put your hands in the soil. We learn best by doing. Thank you, Casey!',
          image: '/wormhole/tiles/p02-3.jpg',
        },
      ],
    },
    reason:
      "Linnea, 30 Oct: cover in her flower frame (Canva deck Mentor-Profile-Images) with Casey Williams's photo and name. Deck: mentor-profiles-flower-frame.pptx.",
  },
  {
    key: '2026-10-30 d11 flower frame',
    post: 'd11',
    set: {
      slides: [
        { text: 'Meet our mentors: Brian Daubenspeck', image: '/wormhole/tiles/d11-ff-1.jpg' },
      ],
    },
    reason:
      "Linnea, 30 Oct: cover in her flower frame (Canva deck Mentor-Profile-Images) with Brian Daubenspeck's photo and name. Deck: mentor-profiles-flower-frame.pptx.",
  },
  {
    key: '2026-10-30 d12 flower frame',
    post: 'd12',
    set: {
      slides: [
        {
          text: 'Meet our mentors: Delvin Solkinson, Permaculture Lead',
          image: '/wormhole/tiles/d12-ff-1.jpg',
        },
      ],
    },
    reason:
      "Linnea, 30 Oct: cover in her flower frame (Canva deck Mentor-Profile-Images) with Delvin Solkinson's photo and name. Deck: mentor-profiles-flower-frame.pptx.",
  },
  {
    key: '2026-10-30 d13 flower frame',
    post: 'd13',
    set: {
      slides: [
        {
          text: 'Meet our mentors: Tommy Tepper, Director of Education',
          image: '/wormhole/tiles/d13-ff-1.jpg',
        },
      ],
    },
    reason:
      "Linnea, 30 Oct: cover in her flower frame (Canva deck Mentor-Profile-Images) with Tommy Tepper's photo and name. Deck: mentor-profiles-flower-frame.pptx.",
  },
  {
    key: '2026-10-30 p09 flower frame',
    post: 'p09',
    set: {
      slides: [
        { text: 'Meet our mentors Dora Tkalec', image: '/wormhole/tiles/p09-ff-1.jpg' },
        {
          text: 'Her favourite microbe: the naked amoeba. \u201cA slimy splotch that changes shape, and every species keeps its own.\u201d',
          image: '/wormhole/tiles/p09-2.jpg',
        },
        {
          text: '\u201cI have seen plants treated with BioComplete\u2122 compost extract being more resistant to bacterial disease.\u201d Thank you, Dora!',
          image: '/wormhole/tiles/p09-3.jpg',
        },
      ],
    },
    reason:
      "Linnea, 30 Oct: cover in her flower frame (Canva deck Mentor-Profile-Images) with Dora Tkalec's photo and name. Deck: mentor-profiles-flower-frame.pptx.",
  },
  {
    key: '2026-10-30 d13 linnea final',
    post: 'd13',
    set: {
      slides: [
        {
          text: 'Tommy Tepper, Soil Food Web Mentor',
          image: '/wormhole/tiles/d13-linnea-1.jpg',
        },
      ],
      visual_note:
        "Family: I, portrait. Linnea's finished design (30 Oct): Tommy's photo in her flower frame, his name and Soil Food Web Mentor below, logo bottom right. Single image.",
    },
    reason: 'Linnea, 30 Oct: her finished Tommy Tepper design.',
  },
  {
    key: '2026-10-30 p06 mentor design',
    post: 'p06',
    set: {
      slides: [
        { text: 'Gerald Ramirez, Soil Food Web Mentor', image: '/wormhole/tiles/p06-mf-1.jpg' },
        {
          text: 'Gerald teaches students to make compost extracts and teas. Costa Rica, March 2025',
          image: '/wormhole/tiles/p06-2.jpg',
        },
        {
          text: 'They carry living biology from the compost out onto the fields. Thank you, Gerald!',
          image: '/wormhole/tiles/p06-3.jpg',
        },
      ],
    },
    reason:
      'Linnea, 30 Oct: cover in her final mentor design (flower frame, name, Soil Food Web Mentor, logo bottom right), like her Tommy Tepper. Deck: mentor-profiles.pptx.',
  },
  {
    key: '2026-10-30 p03 mentor design',
    post: 'p03',
    set: {
      slides: [
        { text: 'Nick Padwick, Soil Food Web Mentor', image: '/wormhole/tiles/p03-mf-1.jpg' },
        {
          text: 'More than 40 years farming at scale, in the UK, Italy, Spain and Argentina.',
          image: '/wormhole/tiles/p03-2.jpg',
        },
        {
          text: 'Today he makes around 750 tons of compost a year. Thank you, Nick, for showing our students what this looks like at scale.',
          image: '/wormhole/tiles/p03-3.jpg',
        },
      ],
    },
    reason:
      'Linnea, 30 Oct: cover in her final mentor design (flower frame, name, Soil Food Web Mentor, logo bottom right), like her Tommy Tepper. Deck: mentor-profiles.pptx.',
  },
  {
    key: '2026-10-30 p09 mentor design',
    post: 'p09',
    set: {
      slides: [
        { text: 'Dora Tkalec, Soil Food Web Mentor', image: '/wormhole/tiles/p09-mf-1.jpg' },
        {
          text: 'Her favourite microbe: the naked amoeba. “A slimy splotch that changes shape, and every species keeps its own.”',
          image: '/wormhole/tiles/p09-2.jpg',
        },
        {
          text: '“I have seen plants treated with BioComplete™ compost extract being more resistant to bacterial disease.” Thank you, Dora!',
          image: '/wormhole/tiles/p09-3.jpg',
        },
      ],
    },
    reason:
      'Linnea, 30 Oct: cover in her final mentor design (flower frame, name, Soil Food Web Mentor, logo bottom right), like her Tommy Tepper. Deck: mentor-profiles.pptx.',
  },
  {
    key: '2026-10-30 d05 mentor design',
    post: 'd05',
    set: {
      slides: [
        { text: 'Dr. Carla Portugal, Soil Food Web Mentor', image: '/wormhole/tiles/d05-mf-1.jpg' },
      ],
    },
    reason:
      'Linnea, 30 Oct: cover in her final mentor design (flower frame, name, Soil Food Web Mentor, logo bottom right), like her Tommy Tepper. Deck: mentor-profiles.pptx.',
  },
  {
    key: '2026-10-30 p04 mentor design',
    post: 'p04',
    set: {
      slides: [
        { text: 'Wes Sander, Soil Food Web Mentor', image: '/wormhole/tiles/p04-mf-1.jpg' },
        {
          text: "His favourite organism: the Arcella amoeba. “There's just something about that large test that you can almost see inside of, with the amoeba squished up against the wall. So cool.” Arcella at 40x, photographed by student Mark Horton.",
          image: '/wormhole/tiles/p04-2.jpg',
        },
        {
          text: "“It depends,” as Dr. Elaine loved to say. Wes's advice: success hinges on reading the signs. Thank you, Wes!",
          image: '/wormhole/tiles/p04-3.jpg',
        },
      ],
    },
    reason:
      'Linnea, 30 Oct: cover in her final mentor design (flower frame, name, Soil Food Web Mentor, logo bottom right), like her Tommy Tepper. Deck: mentor-profiles.pptx.',
  },
  {
    key: '2026-10-30 d11 mentor design',
    post: 'd11',
    set: {
      slides: [
        { text: 'Brian Daubenspeck, Soil Food Web Mentor', image: '/wormhole/tiles/d11-mf-1.jpg' },
      ],
    },
    reason:
      'Linnea, 30 Oct: cover in her final mentor design (flower frame, name, Soil Food Web Mentor, logo bottom right), like her Tommy Tepper. Deck: mentor-profiles.pptx.',
  },
  {
    key: '2026-10-30 p02 mentor design',
    post: 'p02',
    set: {
      slides: [
        { text: 'Casey Williams, Soil Food Web Mentor', image: '/wormhole/tiles/p02-mf-1.jpg' },
        {
          text: '“I am deeply grateful that I get to learn from my students as well as teach them.” A bacterial-feeding nematode at 40x, photographed by Casey.',
          image: '/wormhole/tiles/p02-2.jpg',
        },
        {
          text: 'His advice: put your hands in the soil. We learn best by doing. Thank you, Casey!',
          image: '/wormhole/tiles/p02-3.jpg',
        },
      ],
    },
    reason:
      'Linnea, 30 Oct: cover in her final mentor design (flower frame, name, Soil Food Web Mentor, logo bottom right), like her Tommy Tepper. Deck: mentor-profiles.pptx.',
  },
  {
    key: '2026-10-30 d12 mentor design',
    post: 'd12',
    set: {
      slides: [
        { text: 'Delvin Solkinson, Soil Food Web Mentor', image: '/wormhole/tiles/d12-mf-1.jpg' },
      ],
    },
    reason:
      'Linnea, 30 Oct: cover in her final mentor design (flower frame, name, Soil Food Web Mentor, logo bottom right), like her Tommy Tepper. Deck: mentor-profiles.pptx.',
  },
  {
    key: '2026-10-30 p06 moved to 2026-11-04',
    post: 'p06',
    set: { iso_date: '2026-11-04', date_tbd: false },
    reason:
      'Linnea, 30 Oct: all mentors go out in the first two weeks of November, one every day or two from Mon 2 Nov. Gerald Ramirez on 2026-11-04. Decks for Canva: /wormhole/decks/mentors-november.zip.',
  },
  {
    key: '2026-10-30 p03 moved to 2026-11-06',
    post: 'p03',
    set: { iso_date: '2026-11-06', date_tbd: false },
    reason:
      'Linnea, 30 Oct: all mentors go out in the first two weeks of November, one every day or two from Mon 2 Nov. Nick Padwick on 2026-11-06. Decks for Canva: /wormhole/decks/mentors-november.zip.',
  },
  {
    key: '2026-10-30 p09 moved to 2026-11-08',
    post: 'p09',
    set: { iso_date: '2026-11-08', date_tbd: false },
    reason:
      'Linnea, 30 Oct: all mentors go out in the first two weeks of November, one every day or two from Mon 2 Nov. Dora Tkalec on 2026-11-08. Decks for Canva: /wormhole/decks/mentors-november.zip.',
  },
  {
    key: '2026-10-30 d05 moved to 2026-11-09',
    post: 'd05',
    set: { iso_date: '2026-11-09', date_tbd: false },
    reason:
      'Linnea, 30 Oct: all mentors go out in the first two weeks of November, one every day or two from Mon 2 Nov. Dr. Carla Portugal on 2026-11-09. Decks for Canva: /wormhole/decks/mentors-november.zip.',
  },
  {
    key: '2026-10-30 p04 moved to 2026-11-10',
    post: 'p04',
    set: { iso_date: '2026-11-10', date_tbd: false },
    reason:
      'Linnea, 30 Oct: all mentors go out in the first two weeks of November, one every day or two from Mon 2 Nov. Wes Sander on 2026-11-10. Decks for Canva: /wormhole/decks/mentors-november.zip.',
  },
  {
    key: '2026-10-30 d11 moved to 2026-11-12',
    post: 'd11',
    set: { iso_date: '2026-11-12', date_tbd: false },
    reason:
      'Linnea, 30 Oct: all mentors go out in the first two weeks of November, one every day or two from Mon 2 Nov. Brian Daubenspeck on 2026-11-12. Decks for Canva: /wormhole/decks/mentors-november.zip.',
  },
  {
    key: '2026-10-30 p02 moved to 2026-11-14',
    post: 'p02',
    set: { iso_date: '2026-11-14', date_tbd: false },
    reason:
      'Linnea, 30 Oct: all mentors go out in the first two weeks of November, one every day or two from Mon 2 Nov. Casey Williams on 2026-11-14. Decks for Canva: /wormhole/decks/mentors-november.zip.',
  },
  {
    key: '2026-10-30 d12 moved to 2026-11-15',
    post: 'd12',
    set: { iso_date: '2026-11-15', date_tbd: false },
    reason:
      'Linnea, 30 Oct: all mentors go out in the first two weeks of November, one every day or two from Mon 2 Nov. Delvin Solkinson on 2026-11-15. Decks for Canva: /wormhole/decks/mentors-november.zip.',
  },
];

CHANGES.push(...GAP_CHANGES, ...JAN_CHANGES, ...OCT27_CHANGES);

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
    if (c.remove) {
      // Deleting is safe to repeat, so it runs on every start; versions cascade.
      await db().query(`delete from wormhole_posts where id = $1`, [c.post]);
      continue;
    }
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
    let caption = c.captionText ?? current.caption;
    for (const [from, to] of c.caption ?? []) caption = caption.split(from).join(to);
    const note = current.note ? `${c.reason}\n${current.note}` : c.reason;
    await savePost(
      c.post,
      { ...c.set, ...(c.caption || c.captionText ? { caption } : {}), note },
      editorOf(c),
    );
  }
  done = true;
}
