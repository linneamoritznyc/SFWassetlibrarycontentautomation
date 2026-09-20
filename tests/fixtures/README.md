# fixtures

Not in git (see `.gitignore`). Put the following here before running the phase
acceptance tests.

| File | What | Used by |
| --- | --- | --- |
| `photos/*.jpg` | 30 real SFW workshop photos, any size | Phase 2 |
| `video-short.mp4` | ~3 minutes, one speaker, clear speech | Phase 3 |
| `video-long.mp4` | over 3 minutes, so `find_clips` triggers | Phase 3 |
| `sample.pdf` | any SFW report or trial write-up | Phase 2, Phase 4 |

Anything with a real person in it needs a release on file before it is used in a
post; the `release_status` field tracks that.
