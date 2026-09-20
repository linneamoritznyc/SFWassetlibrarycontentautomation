# cron: inserts scheduled job rows and nothing else.
FROM node:20-slim AS build
WORKDIR /app
RUN corepack enable
COPY pnpm-workspace.yaml package.json pnpm-lock.yaml* tsconfig.base.json ./
COPY packages ./packages
COPY workers/cron ./workers/cron
RUN pnpm install --frozen-lockfile=false
RUN pnpm --filter @sfw/worker-cron... build

FROM node:20-slim
WORKDIR /app
RUN corepack enable
ENV NODE_ENV=production
COPY --from=build /app ./

# Schedules are written in CET, as the spec does.
ENV CRON_TIMEZONE=Europe/Berlin

# No argument means stay up and fire on the schedule. To use Railway's own cron
# triggers instead, set the trigger's command to
# `node workers/cron/dist/index.js plan_week` and so on, one per schedule.
CMD ["node", "workers/cron/dist/index.js"]
