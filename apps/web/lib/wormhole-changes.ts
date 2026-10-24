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
