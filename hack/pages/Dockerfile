# syntax=docker/dockerfile:1

# -----------------------------------------------------------------------------
# 依存関係ステージ
# -----------------------------------------------------------------------------
# Cloudflare Pages 用の静的ビルドはこの Dockerfile 内で完結させる。
# ホストには node_modules、Blume の dist、Wrangler を作成・インストールしない。
FROM node:22-slim AS deps

WORKDIR /workspace

COPY package.json .
RUN npm install --cache /tmp/npm-cache --no-audit --no-fund \
  && rm -rf /tmp/npm-cache /root/.npm

# -----------------------------------------------------------------------------
# 静的ビルドターゲット
# -----------------------------------------------------------------------------
# root の blume.config.ts はサーバ/MCP 用なので使わない。
# hack/pages/blume.config.js をビルド時に root config として配置する。
FROM deps AS pages-build

COPY hack/pages/blume.config.js ./blume.config.js
COPY theme.css .
COPY docs ./docs
COPY public ./public
COPY scripts ./scripts
RUN node scripts/prepare-content.mjs
RUN npx blume build --strict

# -----------------------------------------------------------------------------
# Cloudflare Pages デプロイターゲット
# -----------------------------------------------------------------------------
# `make pages-deploy` から利用する。
# CLOUDFLARE_API_TOKEN と CLOUDFLARE_ACCOUNT_ID は実行時に環境変数で渡す。
FROM pages-build AS pages-deploy

ARG WRANGLER_VERSION=latest
ENV CLOUDFLARE_PAGES_PROJECT=sample-document-site
ENV CLOUDFLARE_PAGES_BRANCH=main

RUN npm install --global wrangler@${WRANGLER_VERSION} \
  && npm cache clean --force

CMD ["sh", "-c", "wrangler pages deploy dist/client --project-name \"$CLOUDFLARE_PAGES_PROJECT\" --branch \"$CLOUDFLARE_PAGES_BRANCH\""]
