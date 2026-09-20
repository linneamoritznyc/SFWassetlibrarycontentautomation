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
# the Debian archive, so it comes from Google Fonts, which publishes it under
# the Open Font License. If the download fails the image still builds and
# fontconfig falls back to DejaVu Sans Bold: the clips are legible but off
# brand, which is better than a broken image. See docs/TODO-LINNEA.md.
RUN mkdir -p /usr/local/share/fonts/montserrat \
 && curl -fsSL -o /usr/local/share/fonts/montserrat/Montserrat-SemiBold.ttf \
      "https://github.com/google/fonts/raw/main/ofl/montserrat/static/Montserrat-SemiBold.ttf" \
    || echo "Montserrat unavailable at build time, falling back to DejaVu" \
 && fc-cache -f

ENV NODE_ENV=production
COPY --from=build /app ./

# FFmpeg is memory hungry on 4K source, and two runs at once finish later than
# two in a row.
ENV WORKER_TYPES=proxy,transcribe,cut_clip
ENV WORKER_CONCURRENCY=1
# Big originals land here. Railway gives the container its own disk.
ENV MEDIA_TMPDIR=/tmp

CMD ["node", "workers/media/dist/index.js"]
