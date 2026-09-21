# worker-media: FFmpeg, Whisper's audio prep, and the caption burner.
FROM node:20-slim AS build
WORKDIR /app
RUN corepack enable
COPY pnpm-workspace.yaml package.json pnpm-lock.yaml* tsconfig.base.json ./
COPY packages ./packages
COPY workers/media ./workers/media
RUN pnpm install --frozen-lockfile=false
RUN pnpm --filter @sfw/worker-media... build

FROM node:20-slim
WORKDIR /app
RUN corepack enable

# ffmpeg does the cutting; libass (built into ffmpeg) burns the captions.
# python3 is here for the speaker-tracking crop in Phase 8.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ffmpeg python3 python3-pip curl ca-certificates fontconfig fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# Face detection for the speaker-tracking crop. Pinned below 5 because OpenCV 5
# dropped the bundled Haar cascades, and the DNN replacement needs a model file
# fetched at runtime. Headless: there is no display in a container.
RUN pip3 install --no-cache-dir --break-system-packages 'opencv-python-headless<5'

# Montserrat 600 is the brand caption face (CLAUDE.md section 5). It is not in
# the Debian archive, so the file is checked into the repository under the Open
# Font License and copied into the image. Nothing is fetched at build time.
# libass is also pointed at packages/brand/fonts directly, so the captions come
# out in Montserrat whether or not fontconfig knows about it.
COPY packages/brand/fonts/Montserrat-SemiBold.ttf /usr/local/share/fonts/montserrat/
RUN fc-cache -f

ENV NODE_ENV=production
COPY --from=build /app ./

# FFmpeg is memory hungry on 4K source, and two runs at once finish later than
# two in a row.
ENV WORKER_TYPES=proxy,transcribe,cut_clip
ENV WORKER_CONCURRENCY=1
# Big originals land here. Railway gives the container its own disk.
ENV MEDIA_TMPDIR=/tmp

CMD ["node", "workers/media/dist/index.js"]
