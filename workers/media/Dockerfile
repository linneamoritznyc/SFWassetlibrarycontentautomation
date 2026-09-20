# worker-media: needs FFmpeg and Python (Whisper helpers, face crop).
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
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg python3 python3-pip fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*
ENV NODE_ENV=production
COPY --from=build /app ./
ENV WORKER_TYPES=""
ENV WORKER_CONCURRENCY=1
CMD ["node", "workers/media/dist/index.js"]
