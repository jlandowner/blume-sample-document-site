FROM node:22-slim AS deps

WORKDIR /workspace

COPY package.json .
RUN npm install --cache /tmp/npm-cache --no-audit --no-fund \
  && rm -rf /tmp/npm-cache /root/.npm

FROM deps AS builder

COPY blume.config.ts .
COPY docs ./docs
COPY public ./public
COPY tools/blume-poc ./tools/blume-poc
RUN npm run blume:build

FROM builder AS mcp-search-test

RUN npm run blume:test:mcp-search

FROM builder AS validator

RUN npm run blume:validate-links

FROM node:22-slim

WORKDIR /app

ENV HOST=0.0.0.0
ENV PORT=4321

COPY --from=deps /workspace/package.json ./package.json
COPY --from=deps /workspace/node_modules ./node_modules
COPY --from=builder /workspace/dist ./dist

EXPOSE 4321

CMD ["node", "dist/server/entry.mjs"]
