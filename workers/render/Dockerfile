# worker-render: Remotion drives a headless Chromium, so the image carries one.
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

# Remotion needs a browser and ffmpeg to stitch the frames. Chromium's own
# shared libraries are the long list; without them it fails to launch with a
# message that does not mention which one is missing.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ffmpeg chromium fonts-dejavu-core curl ca-certificates fontconfig \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Same brand face as the caption burner, same fallback if it cannot be fetched.
RUN mkdir -p /usr/local/share/fonts/montserrat \
 && curl -fsSL -o /usr/local/share/fonts/montserrat/Montserrat-SemiBold.ttf \
      "https://github.com/google/fonts/raw/main/ofl/montserrat/static/Montserrat-SemiBold.ttf" \
    || echo "Montserrat unavailable at build time, falling back to DejaVu" \
 && fc-cache -f

ENV NODE_ENV=production
COPY --from=build /app ./

# Remotion would otherwise download its own Chrome on first render, which
# fails on a read-only or slow container.
ENV REMOTION_CHROME_EXECUTABLE=/usr/bin/chromium
ENV WORKER_TYPES=render_reel
ENV WORKER_CONCURRENCY=1
ENV MEDIA_TMPDIR=/tmp

CMD ["node", "workers/render/dist/index.js"]
