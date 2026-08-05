---
id: design.ai-agent-access-plan
title: AIエージェント向けアクセス設計
description: AIエージェントからK8sプラットフォームドキュメントを検索・取得できるようにするための設計プラン。
type: overview
owner: platform-team
status: draft
review_cycle: quarterly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - platform-team
tags:
  - ai
  - mcp
  - rag
canonical_url: /design/ai-agent-access-plan/
---

# AIエージェント向けアクセス設計

## 目的

AIエージェントが、K8sプラットフォームドキュメントを安全かつ安定して検索・取得できるようにします。

人間向けサイトとAI向けMCP endpointはBlumeに統一します。AIエージェントはBlume MCPの検索・取得toolを使い、必要なpageを検索・取得します。

## 外部事例からの確認

Googleの公開Agent Skills repositoryでは、skillごとに `SKILL.md` を置き、`name`、`description`、`WHEN` で使う場面を明示しています。詳細知識は `references/` に分離し、入口となるskill fileからtrigger keywordに応じて参照先を選ぶ構成です。

GKE skillの例では、`SKILL.md` にQuick StartとReference Directoryを置き、networking、security、scaling、cost、observability、MCP serverなどのtopicを個別referenceへ誘導しています。また、見つからないproduct informationはMCP serverの `search_documents` toolを使う、というfallbackも明示されています。

この構成から、今回のドキュメントサイトでも次の方針を採用します。

- AI向け入口を薄く保ち、詳細知識は既存Markdown pageへ分離する。
- trigger keyword、page metadata、heading、link構造を明示する。
- agentが最初に読む軽量indexとして `llms.txt` を提供する。
- agentが必要なpageだけを検索・取得できるMCP toolsを提供する。
- RAG検索品質はMarkdownのfrontmatter、heading、link構造を直すことで改善する。

## 採用方針

AI向けアクセスはBlume内蔵MCP serverを採用します。独自Python server、別検索server、静的 `/ai` artifact生成は使いません。

```text
Markdown docs
  -> Blume content preparation
  -> Blume strict build
  -> Blume Node server
  -> Site users / AI agents
```

MCP serverはBlumeのbuild outputに含まれます。これにより、AI用の検索・取得ロジックはsite buildと同じ正本から再現可能になります。

## 境界

Blume、MCP、Skillの責務は分けます。

| 境界 | 責務 | 配布方法 |
| --- | --- | --- |
| Blume site | 人間向けHTML、検索UI、`llms.txt` を提供する | Blume Node server |
| MCP | agent向けの検索・取得APIを提供する | Blume Node serverの `/mcp` |
| Skill | agentに「いつ、どのMCP toolを使うか」を教える薄い入口 | client側または別repoで静的配布 |

このサンプルリポジトリではSkill配布物を持ちません。agentが読む本文はMCP経由でpage単位に取得します。

## MCP tools

MCP toolsは、agentが「探す」「読む」ために使います。

| tool | 入力 | 出力 |
| --- | --- | --- |
| `search_docs` | `query`, optional `limit` | page候補、route、title、excerpt、URL |
| `get_page` | `route` | Markdown本文 |

検索はBlumeの検索providerを使います。日本語検索のため、`blume.config.ts` で `i18n.defaultLocale: "ja"` を設定します。

## 日本語検索の検証

`make test-mcp-search` はコンテナbuild内でBlume serverを起動し、MCP endpoint `/mcp` に対して日本語queryを送ります。

検証対象:

| query | 期待するroute |
| --- | --- |
| `本番` | `/environments/production` |
| `デプロイ` | `/procedures/deploy-application` |
| `命名` | `/constraints/naming-conventions` |
| `ロールバック` | `/procedures/rollback` |

## container構成

構成は単一コンテナです。

```text
blume-docs
  - Blume siteを配信する。
  - /mcp でBlume内蔵MCP serverを公開する。
  - /llms.txt を配信する。
```

local developmentとcluster deploymentのどちらでも、同じHTTP endpointを使います。

## 実装ステップ

1. `blume.config.ts` でMCPと `llms.txt` を有効化する。
2. `i18n.defaultLocale: "ja"` を設定する。
3. `Dockerfile` でBlume buildとNode runtimeを定義する。
4. `make validate` でstrict buildを実行する。
5. `make test-mcp-search` でMCP日本語検索を検証する。
6. 必要になった場合だけ、追加toolやpromptsを検討する。

## 非目標

初期実装では以下を行いません。

- embedding/vector DBの導入。
- agentがKubernetes APIを直接操作するtoolの提供。
- 外部SaaS検索への依存。
- HTMLをparseしてRAG sourceにすること。
- Python MCP serverの保守。

## 判断

最初に作るべきものは、Blume MCPを有効化した単一ドキュメントサイトです。agentが読む入口は小さく、詳細知識は既存Markdown pageへ分離します。

この方針なら、人間向けサイト、MCP tool response、`llms.txt` がすべて同じMarkdown正本から生成されます。
