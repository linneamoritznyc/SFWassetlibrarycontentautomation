/**
 * Gap fills and cleanup for October to December 2026 (26 Oct finishing pass).
 * Same shape and rules as CHANGES in wormhole-changes.ts.
 */
import type { Change } from './wormhole-changes';

export const GAP_CHANGES: Change[] = [
  {
    key: '2026-10-26 remove p07',
    post: 'p07',
    remove: true,
    reason: 'Removed (Linnea, 26 Oct): Dr. Caterina Capri no longer works with SFW.',
  },
  {
    key: '2026-10-26 remove p27',
    post: 'p27',
    remove: true,
    reason: 'Removed (26 Oct): duplicate of cr20261112 "Costa Rica: a day at the workshop".',
  },
  {
    key: '2026-10-26 gaps p02 caption',
    post: 'p02',
    captionText:
      'This month, we are celebrating our one-year anniversary as a foundation! As we reflect on all the progress our students have made this year, we\'d like you to meet one of our wonderful mentors, Casey Williams!\nCasey is a Soil Food Web Consultant who has worked in agriculture in many roles: managing farms, permaculture design, growing gourmet mushrooms and microgreens, running aquaponics systems, and producing biochar and compost. Today he runs his own business and keeps experimenting with composting and biochar methods at different scales.\nHe took the bacterial-feeding nematode on our second slide himself, at 40x.\n"I am deeply grateful that I get to learn from my students as well as teach them," Casey says. His advice for anyone starting out: put your hands in the soil. We learn best by doing.\nCasey, thank you for the hands-on mentorship you give our students. Share a thank you to Casey in the comments!\n#SoilFoodWeb #LivingSoil #SoilHealth #SoilBiology #Compost #Biochar #Permaculture',
    reason:
      "Caption written (26 Oct) from the slides and Casey's bio on the SFW team page, in the format of the finished mentor posts.",
    set: {
      sources: [
        'October 2026 Social Media Planning Doc',
        'SFW team page bio, Casey Williams (final-sfwsite-linnea/about-team.html)',
      ],
    },
  },
  {
    key: '2026-10-26 gaps p03 caption',
    post: 'p03',
    captionText:
      "This month, we are celebrating our one-year anniversary as a foundation! As we reflect on all the progress our students have made this year, we'd like you to meet one of our wonderful mentors, Nick Padwick!\nNick grew up on a farm in Hampshire, England, and has spent more than 40 years farming at scale, in the UK, Italy, Spain and Argentina. In 2009, Farmers Weekly named him Farm Manager of the Year and Farmer of the Year. Since 2018 he has managed the Ken Hill Estate in Norfolk, home of the Wild Ken Hill nature restoration and regenerative farming project, and through Peddar Farming he oversees farmland in West Norfolk.\nToday he makes around 750 tons of compost a year, and he shows our students what the Soil Food Web Approach looks like on a working farm.\nNick, thank you for showing our students what this looks like at scale. Share a thank you to Nick in the comments!\n#SoilFoodWeb #LivingSoil #SoilHealth #SoilBiology #Compost #RegenerativeAgriculture #Farming",
    reason:
      "Caption written (26 Oct) from the slides and Nick's bio on the SFW team page, in the format of the finished mentor posts.",
    set: {
      sources: [
        'October 2026 Social Media Planning Doc',
        'SFW team page bio, Nick Padwick (final-sfwsite-linnea/about-team.html)',
      ],
    },
  },
  {
    key: '2026-10-26 gaps p04 caption',
    post: 'p04',
    captionText:
      'This month, we are celebrating our one-year anniversary as a foundation! As we reflect on all the progress our students have made this year, we\'d like you to meet one of our wonderful mentors, Wes Sander!\nWes grew up raising chickens, cows and pigs with his family in northern California. He spent a decade as an agriculture journalist, then another managing a small farm in the Sierra Nevada foothills, where he began using Soil Food Web methods. Today he runs his consultancy, Foothill Biological Soil Health Services, and he has mentored our Advanced Programs students since June 2020.\nHis favorite organism is the Arcella amoeba. "There\'s just something about that large test that you can almost see inside of, with the amoeba squished up against the wall. So cool."\nLike Dr. Elaine, Wes knows the answer often starts with "it depends." His advice: success hinges on reading the signs.\nWes, thank you for teaching our students to read what the soil is telling them. Share a thank you to Wes in the comments!\n#SoilFoodWeb #LivingSoil #SoilHealth #SoilBiology #Compost #Microscopy #Protozoa',
    reason:
      "Caption written (26 Oct) from the slides and Wes's bio on the SFW team page, in the format of the finished mentor posts.",
    set: {
      sources: [
        'October 2026 Social Media Planning Doc',
        'SFW team page bio, Wesley Sander (final-sfwsite-linnea/about-team.html)',
      ],
    },
  },
  {
    key: '2026-10-26 gaps p06 caption',
    post: 'p06',
    captionText:
      "This month, we are celebrating our one-year anniversary as a foundation! As we reflect on all the progress our students have made this year, we'd like you to meet one of our wonderful mentors, Gerald Ramírez!\nGerald is an agronomist who graduated from the University of Costa Rica. He joined the Soil Food Web School as a content developer and became an instructor after completing his professional development with the school. He also works as a soil analyst, reading physical and chemical soil indicators to guide management, and his areas of expertise include applied mathematics, research and transitional agriculture.\nAt our workshop in Costa Rica in March 2025, Gerald showed students how to make compost extracts and teas, the biological liquid amendments that carry living biology from the compost out onto the fields.\nGerald, thank you for bringing the science and the practice together for our students. Share a thank you to Gerald in the comments!\n#SoilFoodWeb #LivingSoil #SoilHealth #SoilBiology #Compost #CompostExtract #CompostTea",
    reason:
      "Caption written (26 Oct) from the slides, Gerald's bio on the SFW team page and the Costa Rica 2025 workshop page, in the format of the finished mentor posts.",
    set: {
      sources: [
        'October 2026 Social Media Planning Doc',
        'SFW team page bio, Gerald Ramírez (final-sfwsite-linnea/about-team.html)',
        'SFW community page, Costa Rica 2025 workshop (final-sfwsite-linnea/community.html)',
      ],
    },
  },
  {
    key: '2026-10-26 gaps p09 caption',
    post: 'p09',
    captionText:
      'This month, we are celebrating our one-year anniversary as a foundation! As we reflect on all the progress our students have made this year, we\'d like you to meet one of our wonderful mentors, Dora Tkalec!\nDora is a teacher by training and a gardener at heart, based in Tampere, Finland. Her search for the taste of a ripe tomato from her childhood led her to permaculture, and then to compost. She joined Dr. Elaine\'s school in 2019. Since 2020 she has worked as a project manager, composting expert and educator at an agricultural vocational school, where she developed a composting process for the school\'s dairy farm.\nHer favorite microbe is the naked amoeba: "A slimy splotch that changes shape, and every species keeps its own."\n"I have seen plants treated with BioComplete™ compost extract being more resistant to bacterial disease," she says.\nDora, thank you for teaching so many growers the magic of compost. Share a thank you to Dora in the comments!\n#SoilFoodWeb #LivingSoil #SoilHealth #SoilBiology #Compost #CompostExtract #Protozoa',
    reason:
      "Caption written (26 Oct) from the slides and Dora's bio on the SFW team page, in the format of the finished mentor posts.",
    set: {
      sources: [
        'October 2026 Social Media Planning Doc',
        'SFW team page bio, Dora Tkalec (final-sfwsite-linnea/about-team.html)',
      ],
    },
  },
  {
    key: '2026-10-26 gaps sh-w1-01 caption',
    post: 'sh-w1-01',
    captionText:
      'Can soil heal itself after a fire? 🔥\nIn this clip from our free webinar Wildfire Recovery & Bioremediation with Soil Biology, Ivan explains what soil life does once the flames have passed. Share it with someone rebuilding land after a fire.\n#Shorts #WildfireRecovery #SoilBiology #SoilFoodWeb',
    reason:
      'Caption written (26 Oct): short Shorts caption from the cover title and the Webinar 1 clip.',
    set: {
      sources: ['Webinar 1, "Wildfire Recovery & Bioremediation with Soil Biology" (clip: Ivan)'],
    },
  },
  {
    key: '2026-10-26 gaps sh-w1-02 caption',
    post: 'sh-w1-02',
    captionText:
      'Weeds after a fire? They may be doing the soil a favor. 🌱\nIn this clip from our free webinar Wildfire Recovery & Bioremediation with Soil Biology, Ivan explains why the first plants to come back after a fire deserve a second look.\n#Shorts #WildfireRecovery #Weeds #SoilFoodWeb',
    reason:
      'Caption written (26 Oct): short Shorts caption from the cover title and the Webinar 1 clip.',
    set: {
      sources: ['Webinar 1, "Wildfire Recovery & Bioremediation with Soil Biology" (clip: Ivan)'],
    },
  },
  {
    key: '2026-10-26 gaps sh-w1-03 caption',
    post: 'sh-w1-03',
    captionText:
      'A wildfire came through. The garden made it. 🔥\nIn this clip from our free webinar Wildfire Recovery & Bioremediation with Soil Biology, Ivan tells the story of how their garden survived, and what the soil had to do with it.\n#Shorts #WildfireRecovery #Gardening #SoilFoodWeb',
    reason:
      'Caption written (26 Oct): short Shorts caption from the cover title and the Webinar 1 clip.',
    set: {
      sources: ['Webinar 1, "Wildfire Recovery & Bioremediation with Soil Biology" (clip: Ivan)'],
    },
  },
  {
    key: '2026-10-26 gaps sh-w1-04 caption',
    post: 'sh-w1-04',
    captionText:
      'Where do heavy metals go after a fire? 🔬\nIn this clip from our free webinar Wildfire Recovery & Bioremediation with Soil Biology, Ivan answers that question and explains where soil biology fits into bioremediation.\n#Shorts #Bioremediation #WildfireRecovery #SoilBiology #SoilFoodWeb',
    reason:
      'Caption written (26 Oct): short Shorts caption from the cover title and the Webinar 1 clip.',
    set: {
      sources: ['Webinar 1, "Wildfire Recovery & Bioremediation with Soil Biology" (clip: Ivan)'],
    },
  },
  {
    key: '2026-10-26 gaps promo-fall-bundle caption',
    post: 'promo-fall-bundle',
    captionText:
      "Want to learn the science and then put it to work in your own compost pile? 🍂\nOur Fall 2026 bundle brings together the four Foundation Courses and the Compost Intensive Course. In the Foundation Courses you learn the soil food web science behind Dr. Elaine Ingham's work, how to make BioComplete™ compost and liquid amendments, and how to read your soil under the microscope, all at your own pace. The bundle also includes the Foundation Courses webinars archive.\nThe Compost Intensive Course puts it into practice: ten weeks of building your own thermal compost, tracking its temperature and checking the biology under the microscope, with our mentors guiding you each week. The next cohort starts in January 2027.\nLink in bio.\n#SoilFoodWeb #FoundationCourses #CompostIntensive #Compost #SoilHealth #LivingSoil",
    reason:
      'Caption written (26 Oct) from the promo image (four Foundation Courses, Compost Intensive Course, webinars archive) and the wording of x20261118 and x20261125. No prices.',
    set: {
      link: '[TAG @Stephanie] Fall 2026 bundle sales page',
      sources: [
        'Promo image from Linnea, 20 Oct (promo-fall-bundle-1.jpg)',
        'https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses',
        'https://school.soilfoodweb.com/courses/compost-intensive-program',
      ],
    },
  },
  {
    key: '2026-10-26 gaps d24 slides',
    post: 'd24',
    set: {
      slides: [
        { text: 'Read the drop.', image: '/wormhole/tiles/d24-v2-1.jpg' },
        {
          text: 'Photo only: protozoa in a drop of soil water.',
          image: '/wormhole/tiles/d24-v2-2.jpg',
        },
        { text: 'Photo only: a nematode.', image: '/wormhole/tiles/d24-v2-3.jpg' },
        {
          text: 'Predators turn bacterial nitrogen into ammonium, right at the root.',
          image: '/wormhole/tiles/d24-v2-4.jpg',
        },
      ],
      visual_note:
        'Reel cover and photo slides (26 Oct, v2 photo-and-tag): cover "Read the drop." on a naked amoeba, then protozoa in soil water, a nematode, and roots in soil "Right at the root." Same Read the drop family as pl20261102 and pl20261130. Reel footage: repo microscopy video or a clip from Wes\'s comparison video.',
    },
    reason:
      'Slides built (26 Oct): Reel cover with 3 words, then photo slides, consistent with the other Read the drop reels.',
  },
  {
    key: '2026-10-26 gaps d20 cover',
    post: 'd20',
    set: {
      slides: [
        {
          text: '"Where Julia lives, green waste gets trucked away."',
          image: '/wormhole/tiles/d20-v2-1.jpg',
        },
        { text: '"So she makes her own vermicompost. 🪱"', image: null },
        {
          text: '"Start your own: a box, damp cardboard, red wigglers, kitchen scraps."',
          image: null,
        },
      ],
    },
    reason:
      'Reel cover tile added (26 Oct): a hand holding wet soil with a red worm, "Julia\'s worm bin." Slides 2 and 3 stay on-screen text over Julia\'s own video.',
  },
  {
    key: '2026-10-26 gaps p24 images',
    post: 'p24',
    set: {
      slides: [
        {
          text: '440,000,000,000,000,000,000. Soil nematodes on Earth.',
          image: '/wormhole/tiles/p24-v2-1.jpg',
        },
        { text: 'About 57 billion for every person alive.', image: '/wormhole/tiles/p24-v2-2.jpg' },
        {
          text: 'Most feed on bacteria and fungi, cycling nutrients for plants.',
          image: '/wormhole/tiles/p24-v2-3.jpg',
        },
      ],
    },
    reason:
      'Images added (26 Oct) to the copy Allison approved; slide text unchanged: a nematode on black, soil-covered hands, fungal threads in field soil.',
  },
  {
    key: '2026-10-26 gaps ev-01 tile',
    post: 'ev-01',
    set: {
      slides: [
        {
          text: 'From surviving to thriving: the case for soil health.',
          image: '/wormhole/tiles/ev-01-v2-1.jpg',
        },
      ],
      visual_note:
        'Reshare on LinkedIn with the article\'s own preview card. Tag Ashley McKeon and the Soil Health Institute. Backup tile (26 Oct, 1200 x 627): field rows at Rancho Cacachilas, "From surviving to thriving."',
    },
    reason:
      'LinkedIn tile added (26 Oct), 1200 x 627, for use if the article preview card does not load.',
  },
  {
    key: '2026-10-26 gaps ss-01-li hashtags',
    post: 'ss-01-li',
    caption: [
      [
        '\n\nhttps://consciousplanet.org/en/save-soil/news/save-soil-movement-model-farm-proof-of-concept',
        '\n\nhttps://consciousplanet.org/en/save-soil/news/save-soil-movement-model-farm-proof-of-concept\n\n#SaveSoil #SoilHealth #SoilOrganicMatter #RegenerativeAgriculture #SoilFoodWeb',
      ],
    ],
    reason: 'Hashtags added (26 Oct): the caption had none.',
  },
  {
    key: '2026-10-26 gaps ss-02-li hashtags',
    post: 'ss-02-li',
    caption: [
      [
        '\n\nhttps://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga',
        '\n\nhttps://consciousplanet.org/en/save-soil/news/soil-as-a-lead-indicator-of-the-global-goal-on-adaptation-gga\n\n#SaveSoil #SoilHealth #SoilBiology #ClimateAdaptation #SoilFoodWeb',
      ],
    ],
    reason: 'Hashtags added (26 Oct): the caption had none.',
  },
  {
    key: '2026-10-26 gaps ss-03 hashtags',
    post: 'ss-03',
    caption: [
      [
        '\n\nhttps://consciousplanet.org/en/save-soil/news/cop30-a-turning-point-for-climate-action-but-agriculture-and-soils-left-behind',
        '\n\nhttps://consciousplanet.org/en/save-soil/news/cop30-a-turning-point-for-climate-action-but-agriculture-and-soils-left-behind\n\n#SaveSoil #COP30 #ClimateFinance #SoilHealth #SoilFoodWeb',
      ],
    ],
    reason: 'Hashtags added (26 Oct): the caption had none.',
  },
  {
    key: '2026-10-26 gaps ss-04 hashtags',
    post: 'ss-04',
    caption: [
      [
        '\n\nhttps://consciousplanet.org/en/save-soil/news/mitigating-climate-change-through-soil-revitalization-using-regenerative-ag',
        '\n\nhttps://consciousplanet.org/en/save-soil/news/mitigating-climate-change-through-soil-revitalization-using-regenerative-ag\n\n#SaveSoil #NoTill #SoilCarbon #SoilHealth #SoilFoodWeb',
      ],
    ],
    reason: 'Hashtags added (26 Oct): the caption had none.',
  },
  {
    key: '2026-10-26 gaps ss-05-li hashtags',
    post: 'ss-05-li',
    caption: [
      [
        '\n\nhttps://consciousplanet.org/en/save-soil/news/soil-degradation-and-biodiversity-loss',
        '\n\nhttps://consciousplanet.org/en/save-soil/news/soil-degradation-and-biodiversity-loss\n\n#SaveSoil #SoilBiodiversity #SoilBiology #SoilHealth #SoilFoodWeb',
      ],
    ],
    reason: 'Hashtags added (26 Oct): the caption had none.',
  },
  {
    key: '2026-10-26 gaps ss-06-li hashtags',
    post: 'ss-06-li',
    caption: [
      [
        '\n\nhttps://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans',
        '\n\nhttps://consciousplanet.org/en/save-soil/news/healthy-soil-and-healthy-humans\n\n#SaveSoil #SoilHealth #Microbiome #PublicHealth #SoilFoodWeb',
      ],
    ],
    reason: 'Hashtags added (26 Oct): the caption had none.',
  },
  {
    key: '2026-10-26 gaps ss-07 hashtags',
    post: 'ss-07',
    caption: [
      [
        '\n\nhttps://consciousplanet.org/en/save-soil/news/secure-soil-save-life',
        '\n\nhttps://consciousplanet.org/en/save-soil/news/secure-soil-save-life\n\n#SaveSoil #SoilSecurity #SoilPolicy #SoilHealth #SoilFoodWeb',
      ],
    ],
    reason: 'Hashtags added (26 Oct): the caption had none.',
  },
  {
    key: '2026-10-26 gaps ss-08-li hashtags',
    post: 'ss-08-li',
    caption: [
      [
        '\n\nhttps://consciousplanet.org/en/save-soil/news/the-soil-carbon-sponge',
        '\n\nhttps://consciousplanet.org/en/save-soil/news/the-soil-carbon-sponge\n\n#SaveSoil #SoilCarbonSponge #WaterCycle #SoilHealth #SoilFoodWeb',
      ],
    ],
    reason: 'Hashtags added (26 Oct): the caption had none.',
  },
  {
    key: '2026-10-26 gaps d05 trim',
    post: 'd05',
    caption: [
      [
        "To kick things off, we're celebrating one of the people who makes the Soil Food Web School what it is.\n",
        '',
      ],
      [
        ", and if you've been through our programs, there's a very good chance Carla is part of the reason it clicked for you",
        '',
      ],
      [
        'What makes her exceptional is the way she shows up for every student, at every level, with patience, precision, and genuine care. She meets you where you are and walks you further than you thought you could go.\n',
        '',
      ],
      [
        'Reflecting on a memorable student, Carla noted a, “student who was a K-12 retired teacher joined our Advanced Programs. In our first meeting, she was scared about setting up and using her microscope. She was even considering not taking the course anymore. Over the sessions, we assembled her microscope together. Then, she was scared about the famous Microscope Proficiency Assessments. Guess what!? She faced them and passed on the first time taking them. She called me very excited that she could now open her lab and teach the kids in the neighborhood about soil biology. She really appreciated how our system, teaching team and student support helped her navigate through her fears and conquer the micro world!”',
        'Carla also told us about a student who stays with her: a retired K-12 teacher who joined our Advanced Programs and was so nervous about her microscope that she almost left the course. They assembled the microscope together, session by session. She passed her Microscope Proficiency Assessments on her first try and called Carla to say she could now open her own lab and teach the kids in her neighborhood about soil biology.',
      ],
      ['She is a scientist, a teacher, and a true champion of the living soil.\n', ''],
      [
        'We are so grateful to have her leading our students into the science that changes everything.\n',
        '',
      ],
      ['Thank you, Dr. Carla Portugal. 🙏\n', ''],
      [
        ' Today is a great day to tell the teachers who changed your life what they mean to you.',
        '',
      ],
    ],
    reason:
      "Caption trimmed (26 Oct) from 3,144 to under 2,200 characters, the Instagram limit: shortened the student story and cut repeated thank-you lines. Carla's quote about Dr. Elaine is unchanged.",
  },
];
