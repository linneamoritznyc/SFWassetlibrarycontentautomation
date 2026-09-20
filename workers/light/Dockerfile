# worker-light: Claude calls, DB work, Canva, scout, planner.
FROM node:20-slim AS build
WORKDIR /app
RUN corepack enable
COPY pnpm-workspace.yaml package.json pnpm-lock.yaml* tsconfig.base.json ./
COPY packages ./packages
COPY workers/light ./workers/light
RUN pnpm install --frozen-lockfile=false
RUN pnpm --filter @sfw/worker-light... build

FROM node:20-slim
WORKDIR /app
RUN corepack enable
ENV NODE_ENV=production
COPY --from=build /app ./
ENV WORKER_TYPES=""
ENV WORKER_CONCURRENCY=4
CMD ["node", "workers/light/dist/index.js"]
