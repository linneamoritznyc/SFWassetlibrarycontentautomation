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
  // --- Nov-Dec C (promo calendar and dates, 26 Oct) ---
  {
    key: '2026-10-26 k20261115 create',
    post: 'k20261115',
    create: {
      iso_date: '2026-11-15',
      date_tbd: false,
      topic: 'Practicum promo: what the Soil Food Web Complete Practicum is, and who it is for',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'Ready to take the soil food web from the screen to your own land? 🔬\n\nThe Soil Food Web Complete Practicum is our hands-on path for farmers, growers, consultants and anyone moving away from synthetic inputs. It brings four Advanced Programs together: Soil Microscopy, BioComplete™ Compost Production, Biological Liquid Amendments and a Field Trial, where you apply the methods over a full growing season on your own land.\n\nYou have support the whole way: your own one-on-one mentor, matched by time zone and language, and regular office hours with our whole mentorship team. Mentor access lasts 42 months, so life can happen along the way.\n\nPass all four courses and you earn the title Soil Food Web Consultant.\n\nYou start after the Foundation Courses, with a microscope and a camera setup. Link in bio.\n\n#SoilFoodWeb #LivingSoil #SoilHealth #SoilMicroscopy #Compost #RegenerativeAgriculture #SoilFoodWebSchool',
      slides: [
        {
          text: 'The Soil Food Web Complete Practicum.',
          image: '/wormhole/tiles/k20261115-v2-1.jpg',
        },
        {
          text: 'Photo only: building a BioComplete™ compost pile.',
          image: '/wormhole/tiles/k20261115-v2-2.jpg',
        },
        {
          text: 'Photo only: samples ready for the microscope.',
          image: '/wormhole/tiles/k20261115-v2-3.jpg',
        },
        {
          text: 'The Field Trial runs a full growing season on your own land. Link in bio.',
          image: '/wormhole/tiles/k20261115-v2-4.jpg',
        },
      ],
      cta: 'Enroll, link in bio',
      link: 'https://school.soilfoodweb.com/bundles/complete-practicum',
      sources: [
        'Complete Practicum page (four courses, who it is for, prerequisites, 1-1 mentor, office hours, 42 months mentor access, Consultant title): https://school.soilfoodweb.com/bundles/complete-practicum',
        'Site export, learn.json (Complete Practicum, Consultant title): final-sfwsite-linnea/content/learn.json',
      ],
      visual_note:
        'Carousel, 4 slides, v2 photo and tag. Real SFW photos: a student with a microscopy binder in the Cyprus classroom (cy-classes-3), watering a compost pile at a workshop (ctpfw-student-moving-compost-1), sample tubes (test-tubes-with-sample), a planting day in the field (hvdb-inplanten-002). Built with tools/wormhole-visuals/round2_novdec.py. No prices.',
      note: '',
      status: 'draft',
    },
    reason:
      'New post (26 Oct, round 2): first of three Complete Practicum promo posts (promo period Nov 8 to Dec 27). Facts from the practicum page only. Sunday 15 Nov has only the earthworm Reel. [CONFIRM: the hvdb-inplanten photo is a field planting day; swap for a real practicum field trial photo if one exists.]',
  },
  {
    key: '2026-10-26 k20261201 create',
    post: 'k20261201',
    create: {
      iso_date: '2026-12-01',
      date_tbd: false,
      topic: 'Acres U.S.A. Eco-Ag Conference, Coralville, Iowa: we are following it',
      platform: 'LinkedIn',
      caption:
        'The 51st Acres U.S.A. Eco-Ag Conference and Trade Show opens today in Coralville, Iowa, and runs to 4 December.\n\nThe program has tracks on livestock, fruits and vegetables, row crops, agronomy, farm business and marketing, and human health, with speakers including Gabe Brown, Ray Archuleta, Gary Zimmer, Neal Kinsey, John Kempf and Dan Kittredge. Eco-Ag University workshops run on 1 and 2 December.\n\nWe will be following the agronomy and row crop sessions closely. Biology is where many growers say the next gains are, and it is also where on-farm measurement is hardest.\n\nIf you are in Coralville this week: which session are you most looking forward to, and what are you hoping to bring home to your own fields?\n\nhttps://www.conference.acresusa.com/\n\n#EcoAg #AcresUSA #SoilHealth #RegenerativeAgriculture #SoilBiology #SoilFoodWeb',
      slides: [
        {
          text: 'Eco-Ag Conference, Coralville, Iowa, 1 to 4 December.',
          image: '/wormhole/tiles/k20261201-v2-1.jpg',
        },
      ],
      cta: 'Answer in the comments',
      link: 'https://www.conference.acresusa.com/',
      sources: [
        'Acres U.S.A. Eco-Ag Conference page (51st conference, 1 to 4 Dec 2026, Hyatt Regency Coralville, tracks, speakers, Eco-Ag University 1 to 2 Dec): https://www.conference.acresusa.com/',
      ],
      visual_note:
        'LinkedIn single image, 1200 x 627, v2 photo and tag: a hand holding finished compost (hand-of-compost). No conference logo or photos used. Built with tools/wormhole-visuals/round2_novdec.py.',
      note: '',
      status: 'draft',
    },
    reason:
      'New post (26 Oct, round 2): LinkedIn post for the Acres U.S.A. Eco-Ag Conference opening day. Says we are following it, makes no claim that SFW attends. Shares the LinkedIn day with the GivingTuesday post x20261201; move one to the evening slot. [CONFIRM: if anyone from SFW is attending, Stephanie may want to add it.]',
  },
  {
    key: '2026-10-26 k20261205 create',
    post: 'k20261205',
    create: {
      iso_date: '2026-12-05',
      date_tbd: false,
      topic: 'Stories · International Volunteer Day: thank you to our volunteers',
      platform: 'Instagram Stories',
      caption:
        'No caption (Stories). Frame 1 text sticker: "Today is International Volunteer Day, in the UN International Year of Volunteers for Sustainable Development. Thank you to everyone who gives their time to living soil: the mentors who stay after office hours, the graduates who host school groups on their farms, and everyone who shares what they learn with a neighbour." Frame 2: link sticker https://soilfoodweb.com/volunteer. Post after the World Soil Day feed post (pl20261205), around 6:00pm Pacific.',
      slides: [
        {
          text: 'Story frame 1: International Volunteer Day. Thank you.',
          image: '/wormhole/tiles/k20261205-v2-1.jpg',
        },
        {
          text: 'Story frame 2: volunteer with us. Link sticker.',
          image: '/wormhole/tiles/k20261205-v2-2.jpg',
        },
      ],
      cta: 'Volunteer, link sticker',
      link: 'https://soilfoodweb.com/volunteer',
      sources: [
        'UNRIC, UN international years 2026 (International Year of Volunteers for Sustainable Development): https://unric.org/en/un-international-years-2026-rangelands-and-pastoralists-volunteers-and-the-woman-farmer/',
        'International Volunteer Day, 5 December, UN General Assembly resolution 40/212 (1985): https://timeanddate.com/holidays/un/international-volunteer-day',
        'Volunteer page in the site export: final-sfwsite-linnea/volunteer.html',
        'Graduate who hosts school groups as a volunteer: Angela Viner post d19 (impact story sheet)',
      ],
      visual_note:
        'Stories, 2 frames as 1080 x 1350 tiles like the other st posts: a workshop group around their compost pile (workshop-group-around-compost-pile), two soil-covered hands held out (2-dirty-hands). Built with tools/wormhole-visuals/round2_novdec.py. [CONFIRM: the volunteer page URL once the new site is live.]',
      note: '',
      status: 'draft',
    },
    reason:
      'New post (26 Oct, round 2): International Volunteer Day as a short Stories post beside World Soil Day. The thank-you stays general because the site does not say which mentors volunteer. [CONFIRM: soilfoodweb.com/volunteer URL with Alex; whether to name specific volunteer mentors.]',
  },
  {
    key: '2026-10-26 k20261207 create',
    post: 'k20261207',
    create: {
      iso_date: '2026-12-07',
      date_tbd: false,
      topic: 'Practicum promo: field trials, with graduate Daniel Tyrkiel',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        'What happens when a graduate takes the microscope out into the field? 🌾\n\nMeet Daniel Tyrkiel, a Soil Food Web School graduate who runs his consultancy, the Soil Ecology Laboratory, in Hampshire, UK. Daniel runs microbiology field trials with University of Manchester researcher Dr. Janice Lake, comparing biology-treated crops with control crops. In August 2025, The Guardian featured that work, alongside our mentor Nick Padwick.\n\nThis is the skill the Field Trial course teaches: plan a trial on real land, sample it, read it under the microscope and let the results speak, including the disappointing ones.\n\nThe Field Trial is the last of the four courses in the Soil Food Web Complete Practicum, after Soil Microscopy, BioComplete™ Compost Production and Biological Liquid Amendments. Link in bio.\n\n#SoilFoodWeb #FieldTrials #SoilBiology #SoilHealth #RegenerativeAgriculture #SoilMicroscopy #SoilFoodWebSchool',
      slides: [
        {
          text: 'Field trials: where the practicum meets your land.',
          image: '/wormhole/tiles/k20261207-v2-1.jpg',
        },
        {
          text: 'Photo only: a soil sample going into a tube.',
          image: '/wormhole/tiles/k20261207-v2-2.jpg',
        },
        {
          text: 'Treated plots against control plots.',
          image: '/wormhole/tiles/k20261207-v2-3.jpg',
        },
      ],
      cta: 'Enroll, link in bio',
      link: 'https://school.soilfoodweb.com/bundles/complete-practicum',
      sources: [
        'Site export, community.json "Nick Padwick and Daniel Tyrkiel in The Guardian" (graduate, microbiology field trials with Dr. Janice Lake, University of Manchester): final-sfwsite-linnea/content/community.json',
        'SFW October 2025 newsletter (Soil Ecology Laboratory in Hampshire; biology-treated crops outperforming control crops): final-sfwsite-linnea/docs/staging-export/content/posts/october-2025-newsletter.md',
        'The Guardian, 29 Aug 2025: https://www.theguardian.com/environment/2025/aug/29/down-and-dirty-how-regenerative-farming-is-digging-into-microscopic-soil-life',
        'Complete Practicum page (four courses, Field Trial over a full growing season): https://school.soilfoodweb.com/bundles/complete-practicum',
      ],
      visual_note:
        "Carousel, 3 slides, v2 photo and tag: gloved hands sampling soil into a bag (soil-sample-shovel-and-bag), a sample going into a tube (soil-sample-close-up-test-tube), sample tubes by a microscope (Sampling_equipment). Stand-ins: swap in Daniel's own trial photos and tag him as a collab once he agrees. Built with tools/wormhole-visuals/round2_novdec.py.",
      note: '',
      status: 'draft',
    },
    reason:
      'New post (26 Oct, round 2): second Complete Practicum promo, built on the only named graduate field trial in the site export (Daniel Tyrkiel). No trial numbers are used because none are published. [CONFIRM: with Daniel that he is happy to be featured, his handle, and whether his trials ran as his practicum Field Trial; the caption only says he is a graduate who runs field trials.]',
  },
  {
    key: '2026-10-26 k20261218 create',
    post: 'k20261218',
    create: {
      iso_date: '2026-12-18',
      date_tbd: false,
      topic: 'International Year of the Woman Farmer: women who teach living soil',
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        '2026 is the UN International Year of the Woman Farmer, and before it ends we want to thank some of the women who teach living soil in our community. 💚\n\nDora Tkalec, a Soil Food Web Consultant and mentor in Tampere, Finland, developed a composting process for the dairy farm of the agricultural school where she teaches, and runs composting trials with farms.\n\nLoida Vasquez, our Director of Advanced Education, worked with Dr. Elaine Ingham for decades and has designed and led dozens of workshops on compost and soil biology.\n\nIsadora Shmidt found her way from market gardening to permaculture to the soil food web, and now helps others discover the wonders of soil as a Soil Food Web Consultant and mentor.\n\nThank you, Dora, Loida and Isadora. Tag a woman farmer who taught you something about soil.\n\n#YearOfTheWomanFarmer #WomenInAgriculture #SoilFoodWeb #LivingSoil #SoilHealth #Compost',
      slides: [
        {
          text: '2026 is the International Year of the Woman Farmer. Dora Tkalec, Finland.',
          image: '/wormhole/tiles/k20261218-v2-1.jpg',
        },
        {
          text: 'Loida Vasquez, Director of Advanced Education.',
          image: '/wormhole/tiles/k20261218-v2-2.jpg',
        },
        {
          text: 'Isadora Shmidt, Soil Food Web Consultant and mentor.',
          image: '/wormhole/tiles/k20261218-v2-3.jpg',
        },
      ],
      cta: 'Tag a woman farmer',
      link: 'Collab with Dora, Loida and Isadora [VERIFY handles]',
      sources: [
        'UNRIC, UN international years 2026 (International Year of the Woman Farmer): https://unric.org/en/un-international-years-2026-rangelands-and-pastoralists-volunteers-and-the-woman-farmer/',
        'SFW team page bios, Dora Tkalec, Loida Vasquez, Isadora Shmidt: final-sfwsite-linnea/about-team.html',
      ],
      visual_note:
        'Carousel, 3 slides, v2 photo and tag, one woman per slide: Dora with a compost pile (w_dora), Loida teaching at a compost bay (uploads_Loida_Teaching_3), Isadora in a vineyard (w_isadora). Tags sit away from faces. Built with tools/wormhole-visuals/round2_novdec.py. Purple not used.',
      note: '',
      status: 'draft',
    },
    reason:
      "New post (26 Oct, round 2): UN International Year of the Woman Farmer spotlight, Friday 18 Dec, using only published team bios. Dr. Carla Portugal left out because d05 already featured her in October. [CONFIRM: each woman's handle and that she is happy to be in it; Loida's photo was also used on j20270112, more than 7 days away.]",
  },
  {
    key: '2026-10-26 k20261221 create',
    post: 'k20261221',
    create: {
      iso_date: '2026-12-21',
      date_tbd: false,
      topic: 'Practicum promo: last call before the year ends',
      platform: 'Instagram, Facebook',
      caption:
        'If 2027 is the year you become a Soil Food Web Consultant, start now. 🌱\n\nThe Soil Food Web Complete Practicum takes you through Soil Microscopy, BioComplete™ Compost Production, Biological Liquid Amendments and a Field Trial on your own land. Enroll before the year ends and you can spend the quiet weeks of winter at the microscope, ready to build your first piles and plan your trial when spring comes.\n\nYour own mentor works with you one-on-one the whole way, with office hours from our full mentorship team.\n\nFinished the Foundation Courses? This is your next step. Link in bio.\n\n#SoilFoodWeb #SoilFoodWebSchool #LivingSoil #SoilHealth #SoilMicroscopy #NewYearGoals',
      slides: [
        {
          text: 'Start the Complete Practicum before 2027.',
          image: '/wormhole/tiles/k20261221-v2-1.jpg',
        },
        {
          text: 'Your own mentor, from the first slide to the last trial. Link in bio.',
          image: '/wormhole/tiles/k20261221-v2-2.jpg',
        },
      ],
      cta: 'Enroll, link in bio',
      link: 'https://school.soilfoodweb.com/bundles/complete-practicum',
      sources: [
        'Complete Practicum page (four courses, 1-1 mentor, office hours, prerequisites): https://school.soilfoodweb.com/bundles/complete-practicum',
        'SFW 2027 Promotions sheet: Practicum promo Nov 8 to Dec 27',
      ],
      visual_note:
        'Two slides, v2 photo and tag: a workshop group with their pile (uploads_MAR25_Group_Photo), tag at the top so it clears every face; fungal spores in suspension under the microscope. Built with tools/wormhole-visuals/round2_novdec.py. No prices, no deadline on the slide.',
      note: '',
      status: 'draft',
    },
    reason:
      'New post (26 Oct, round 2): third Complete Practicum promo, last call before the promo period ends on 27 Dec. Monday 21 Dec has only the hyphae Reel. Instagram and Facebook for enrollment. [CONFIRM: whether any year-end offer applies; the caption names none.]',
  },
  {
    key: '2026-10-26 k20261223 create',
    post: 'k20261223',
    create: {
      iso_date: '2026-12-23',
      date_tbd: false,
      topic: "Kisan Diwas: thank you to India's farmers",
      platform: 'Instagram, Facebook, LinkedIn',
      caption:
        "Happy Kisan Diwas! 🌾\n\nToday India celebrates National Farmers' Day, on the birth anniversary of Chaudhary Charan Singh, the farmer leader and former Prime Minister who fought for peasants' rights to their land and their harvest.\n\nThis year we held our first workshop in India: the Accelerator Workshop in Coimbatore, Tamil Nadu, from 19 to 30 October, in collaboration with Isha Outreach. It ran with the Isha Foundation and the Conscious Planet Save Soil movement, at the Save Soil Regenerative Revolution Farm, which serves farmers across Tamil Nadu and Puducherry. For two weeks, students built thermophilic compost piles and brewed compost extracts and teas, with the microscope every day.\n\nTo every farmer in India who feeds the soil so the soil can feed us: thank you. Link in bio.\n\n#KisanDiwas #NationalFarmersDay #SaveSoil #SoilFoodWeb #LivingSoil #SoilHealth #India",
      slides: [
        {
          text: 'Happy Kisan Diwas.',
          image: '/wormhole/tiles/k20261223-v2-1.jpg',
        },
        {
          text: 'Thank you to every farmer in India.',
          image: '/wormhole/tiles/k20261223-v2-2.jpg',
        },
      ],
      cta: 'See the India workshop, link in bio',
      link: 'https://school.soilfoodweb.com/courses/india-workshop-2026',
      sources: [
        'Vikaspedia, National Farmers Day (Kisan Diwas, 23 December): https://vikaspedia.in/agriculture/agri-directory/important-days/national-farmers-day',
        "Drishti IAS, Birth anniversary of Chaudhary Charan Singh and National Farmers' Day (born 1902, 5th Prime Minister, farmer reforms): https://www.drishtiias.com/daily-updates/daily-news-analysis/birth-anniversary-of-chaudhary-charan-singh-and-national-farmers-day-2024/print_manually",
        'India Accelerator Workshop 2026 page and CLAUDE.md section 9 (dates, place, farm, curriculum): https://school.soilfoodweb.com/courses/india-workshop-2026',
        'Partner naming: CLAUDE.md section 4',
      ],
      visual_note:
        'Two slides, v2 photo and tag: a hand in red soil (red-soil-hand), hands holding a plant and its roots (2-hands-clasped-holding-plant-roots). No India workshop photos are in the photo folder or existing tiles yet; swap slide 1 for a real Coimbatore workshop photo from Kavi Reddy when it arrives. Built with tools/wormhole-visuals/round2_novdec.py.',
      note: '',
      status: 'draft',
    },
    reason:
      "New post (26 Oct, round 2): Kisan Diwas, India's National Farmers' Day, thanking India's farmers and pointing to the October Accelerator Workshop with the CLAUDE.md partner naming. Shares 23 Dec with the partner-share placeholder pl20261223. [CONFIRM: the workshop ran as planned; a recap page or news post to link instead of the course page; real Coimbatore photos from Kavi.]",
  },
  // --- end Nov-Dec C ---
];
