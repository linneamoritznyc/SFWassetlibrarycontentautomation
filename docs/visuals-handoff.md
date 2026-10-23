# Adding finished visuals to Wormhole

How a separate Claude session hands its designs to Wormhole so they show up on
https://wormholelinnea.vercel.app. This covers the logistics only. The design
brief is whatever Linnea gives you.

## Where things live

- Repository: `linneamoritznyc/SFWassetlibrarycontentautomation`
- Branch: `claude/zealous-shannon-g3u56z`. Work on this branch only. Run
  `git pull` before you start and again before you push. Merge, never rebase or
  force-push: another session pushes to it too.
- Slide images: `apps/web/public/wormhole/tiles/`
- The list of changes Wormhole applies to posts: `apps/web/lib/wormhole-changes.ts`

## 1. Find the post

Every post has an id (`p12`, `d27`, `n20261023a`). The ids, dates and current slide
text are in the live data. To read them, log in with the shared Wormhole password
and fetch the posts:

```bash
curl -s -c /tmp/wh.jar -H 'content-type: application/json' \
  -d '{"password":"<Wormhole password>","name":"Claude"}' https://wormholelinnea.vercel.app/api/wormhole/login
curl -s -b /tmp/wh.jar https://wormholelinnea.vercel.app/api/wormhole/posts > /tmp/posts.json
```

Each post has `id`, `iso_date`, `date_tbd`, `topic`, `platform`, `caption`,
`slides` (`[{text, image}]`), `visual_note` and `note`. Read the caption and the
visual note before you design.

## 2. Save the images

- JPG, 1080 x 1350 (4:5), around 150 to 350 KB each.
- Name them `<post id>-<version>-<slide number>.jpg`, lowercase, for example
  `p12-v2-1.jpg`, `p12-v2-2.jpg`. Always use a new version name: never overwrite
  a file that is already in `tiles/`, because the live site and browsers cache by name.
- Only letters, numbers, dots, dashes and underscores. Wormhole rejects any
  other image path.
- LinkedIn-only posts (`d16`, `d17`): one image, 1200 x 627.

## 3. Attach them to the post

Add one entry per post at the end of the `CHANGES` list in
`apps/web/lib/wormhole-changes.ts`, just before the closing `];`:

```ts
  {
    key: '2026-10-23 p12 slides v2',          // unique; never reuse a key
    post: 'p12',
    set: {
      slides: [
        { text: 'Leave the leaves.', image: '/wormhole/tiles/p12-v2-1.jpg' },
        { text: 'Leaf litter is rich in carbon and lignin.', image: '/wormhole/tiles/p12-v2-2.jpg' },
      ],
    },
    reason: 'New slides (23 Oct): <one line on the idea>. Deck: 24-10-2026-leave-the-leaves.pptx.',
  },
```

- `text` is the words on that slide, in order. Keep them true to the caption.
- The `reason` line goes on top of the post's note in Wormhole, so say what changed.
- Wormhole applies each entry once, the next time anyone opens it, through the
  normal edit path. The post's earlier slides stay in its history.
- Change only the posts you were asked to change. Don't edit or delete other entries.
- Don't write to the database directly. Supabase asks for an approval on every
  write and times out.

Then check that it builds:

```bash
cd apps/web && npx prettier --write lib/wormhole-changes.ts && npx tsc --noEmit -p .
```

## 4. Editable PowerPoint (if you make one)

Put it at `apps/web/public/wormhole/decks/DD-MM-YYYY-<slug>.pptx`, using the post
date, and name it in the `reason` line. Every picture and text box should be its
own layer.

## 5. Commit, push, make it live

```bash
git add apps/web/public/wormhole/tiles apps/web/public/wormhole/decks apps/web/lib/wormhole-changes.ts
git commit -m "Wormhole: new visuals for <ids>"
git pull --no-rebase origin claude/zealous-shannon-g3u56z
git push origin claude/zealous-shannon-g3u56z
```

Pushing makes a preview build only. The live site updates after a production
deploy of that commit:

- With the Vercel connector: `create_deployment` on project
  `prj_ruL59w8Y3otzgSC2j5HxHPB5SmA5`, team `team_QBwxqOKJ30FfutqRbb5qkHIr`,
  `target: "production"`, `gitSource` `{type: "github", org: "linneamoritznyc",
  repo: "SFWassetlibrarycontentautomation", ref: "claude/zealous-shannon-g3u56z",
  sha: "<your commit>"}`.
- Without it: tell Linnea the commit is pushed, so she can ask the Wormhole
  session to put it live.

## 6. Check

After the deploy is ready (2 to 4 minutes), log in as in step 1, fetch the posts
again, and confirm that each post's `slides[].image` shows your new file names.
Open one image directly, for example https://wormholelinnea.vercel.app/wormhole/tiles/p12-v2-1.jpg.
Then tell Linnea which posts changed.
