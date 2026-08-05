# syntax=docker/dockerfile:1

# -----------------------------------------------------------------------------
# 依存関係ステージ
# -----------------------------------------------------------------------------
# 依存ライブラリはコンテナ内で npm install する。
# ホストには node_modules やビルド成果物を作らない。
FROM node:22-slim AS deps

WORKDIR /workspace

COPY package.json .
RUN npm install --cache /tmp/npm-cache --no-audit --no-fund \
  && rm -rf /tmp/npm-cache /root/.npm

# -----------------------------------------------------------------------------
# ビルドステージ
# -----------------------------------------------------------------------------
# Blume の静的アセット、Node server、MCP、llms.txt などを生成する。
FROM deps AS builder

COPY blume.config.ts .
COPY theme.css .
COPY docs ./docs
COPY public ./public
COPY scripts ./scripts
RUN npm run blume:build

# -----------------------------------------------------------------------------
# 確認ターゲット: MCP 日本語検索
# -----------------------------------------------------------------------------
# `make test-mcp-search` から利用する。
# Blume の MCP search が日本語クエリで期待ルートを返せることを確認する。
FROM builder AS mcp-search-test

RUN npm run blume:test:mcp-search

# -----------------------------------------------------------------------------
# 確認ターゲット: ドキュメント検証
# -----------------------------------------------------------------------------
# `make validate` から利用する。
# strict build 済み成果物に対して、内部リンクなどの運用ルールを確認する。
FROM builder AS validator

RUN npm run blume:validate-links

# -----------------------------------------------------------------------------
# 実行ステージ
# -----------------------------------------------------------------------------
# 本番実行に必要な node_modules と Blume の dist だけを含める。
FROM node:22-slim

WORKDIR /app

ENV HOST=0.0.0.0
ENV PORT=4321

COPY --from=deps /workspace/package.json ./package.json
COPY --from=deps /workspace/node_modules ./node_modules
COPY --from=builder /workspace/dist ./dist

EXPOSE 4321

CMD ["node", "dist/server/entry.mjs"]
