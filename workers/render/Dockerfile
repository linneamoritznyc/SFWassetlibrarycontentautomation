# worker-render: Remotion needs a Chromium and its shared libraries.
FROM node:20-slim AS build
WORKDIR /app
RUN corepack enable
COPY pnpm-workspace.yaml package.json pnpm-lock.yaml* tsconfig.base.json ./
COPY packages ./packages
COPY workers/render ./workers/render
RUN pnpm install --frozen-lockfile=false
RUN pnpm --filter @sfw/worker-render... build

FROM node:20-slim
WORKDIR /app
RUN corepack enable
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ffmpeg chromium fonts-dejavu-core libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2 \
 && rm -rf /var/lib/apt/lists/*
ENV NODE_ENV=production
ENV REMOTION_CHROME_EXECUTABLE=/usr/bin/chromium
COPY --from=build /app ./
ENV WORKER_TYPES=""
ENV WORKER_CONCURRENCY=1
CMD ["node", "workers/render/dist/index.js"]
