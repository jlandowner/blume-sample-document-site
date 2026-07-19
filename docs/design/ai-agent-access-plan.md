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

人間向けのMkDocsサイトはそのまま維持し、同じMarkdown正本からAI向けartifactを生成します。AIエージェントはMCP server経由でartifactを読み、必要なpageを検索・取得します。

## 外部事例からの確認

Googleの公開Agent Skills repositoryでは、skillごとに `SKILL.md` を置き、`name`、`description`、`WHEN` で使う場面を明示しています。詳細知識は `references/` に分離し、入口となるskill fileからtrigger keywordに応じて参照先を選ぶ構成です。

GKE skillの例では、`SKILL.md` にQuick StartとReference Directoryを置き、networking、security、scaling、cost、observability、MCP serverなどのtopicを個別referenceへ誘導しています。また、見つからないproduct informationはMCP serverの `search_documents` toolを使う、というfallbackも明示されています。

この構成から、今回のドキュメントサイトでも次の方針を採用します。

- AI向け入口を薄く保ち、詳細知識は既存Markdown pageへ分離する。
- trigger keyword、page metadata、chunk metadataを明示する。
- agentが最初に読むindexを生成する。
- agentが必要なpageだけを検索・取得できるMCP tools/resourcesを提供する。
- RAG検索品質はMarkdownのfrontmatter、heading、link構造を直すことで改善する。

## 採用方針

案2の **MCP Docs Server** を先に作ります。内部実装は案1のstatic artifactを読む形にします。

```text
Markdown docs
  -> validator
  -> ai artifact generator
  -> MkDocs site
  -> docs-web container
  -> docs-mcp container
  -> AI agent
```

MCP serverはMarkdownを直接parseしません。build時に生成されたartifactを読みます。これにより、AI用の検索・取得ロジックはsite buildと同じ正本から再現可能になります。

## 境界

`/ai`、MCP、Skillの責務は分けます。

| 境界 | 責務 | 配布方法 |
| --- | --- | --- |
| `/ai` | build済みの機械向けartifactを配信する | docs-webのstatic path |
| MCP | `/ai` artifactを読み、agent向けの検索・取得APIを提供する | docs-mcp container |
| Skill | agentに「いつ、どのMCP toolを使うか」を教える薄い入口 | `/ai/skills/k8s-platform/SKILL.md` |

Skillには全文を詰め込みません。検索結果のmatched sectionsで当たりを付け、本文はMCP経由でpage単位に取得します。

## 生成artifact

`ai/` 配下に次を生成します。

| file | 用途 |
| --- | --- |
| `docs-index.json` | page単位のmetadata、source path、canonical URL、heading一覧 |
| `chunks.jsonl` | heading単位の検索・引用用chunk |
| `llms.txt` | agentが最初に読む軽量index |
| `llms-full.txt` | 全文をまとめたfallback artifact |
| `source/docs/**/*.md` | `docs/` のMarkdown正本をそのまま配信するraw source |
| `skills/k8s-platform/SKILL.md` | 静的に管理するagent skill形式の入口 |
| `skills/k8s-platform/references/*.md` | 静的に管理するtopic別のagent向け短い参照ガイド |

`SKILL.md` は生成せず、repo内の静的ファイルとして管理します。Googleのskills構成に寄せ、次の情報を持たせます。

```text
name k8s-platform-docs
description K8sプラットフォームの環境、制約、手順、API、ツール、チェックリスト、runbookを調べる。
WHEN: deploy, rollback, secret, ingress, quota, production readiness, platform API, platformctl, troubleshooting.
```

## MCP resources

MCP resourcesは、agentが「読む」ための安定URIとして提供します。

| resource | 内容 |
| --- | --- |
| `docs://index` | `docs-index.json` |
| `docs://llms` | `llms.txt` |
| `docs://page/{id}` | `source/docs/**/*.md` から読んだpage単位のMarkdown正本 |
| `docs://skill/k8s-platform` | 静的に管理された `SKILL.md` |

## MCP tools

MCP toolsは、agentが「探す」ために使います。

| tool | 入力 | 出力 |
| --- | --- | --- |
| `docs.search` | `query`, optional `type`, `tags`, `audience` | score付きpage候補とmatched sections |
| `docs.get_page` | `id` | Markdown本文、metadata、canonical URL |

初期検索は軽量なkeyword searchで実装します。vector searchやembeddingは第2段階にします。

## MCP prompts

agent向けのprompt templateも用意します。

| prompt | 用途 |
| --- | --- |
| `prepare_deployment_review` | production deploy前に必要なdoc/checklistを集める |
| `investigate_failure` | 症状からrunbookと関連手順を集める |
| `explain_platform_constraint` | 制約の正本、影響、確認方法をまとめる |

## container構成

初期構成:

```text
docs-web
  - MkDocs static siteを配信する。
  - /ai/* artifactを配信する。

docs-mcp
  - /app/ai artifactを読み込む。
  - Streamable HTTPまたはstdioでMCP serverを公開する。
```

local developmentではstdio、cluster deploymentではStreamable HTTPを優先します。

## 実装ステップ

1. `tools/ai-artifacts/generate_ai_artifacts.py` を追加する。
2. `docs-index.json`、`chunks.jsonl`、`llms.txt`、`llms-full.txt` を生成する。
3. 静的な `tools/ai-artifacts/skills/k8s-platform/SKILL.md` を `/ai/skills` にコピーする。
4. `docs-web` imageに `/ai/*` を含める。
5. `docs-mcp` serverを追加し、artifactを読む。
6. `docs.search`、`docs.get_page` を先に実装する。
7. 必要になった場合だけ、追加toolやpromptsを検討する。
8. 生成artifactとMCP tool responseをvalidatorで検証する。

## 非目標

初期実装では以下を行いません。

- embedding/vector DBの導入。
- agentがKubernetes APIを直接操作するtoolの提供。
- 外部SaaS検索への依存。
- HTMLをparseしてRAG sourceにすること。

## 判断

最初に作るべきものは、artifact generatorとMCP Docs Serverです。GoogleのAgent Skills構成と同じく、agentが読む入口は小さく、詳細知識はtopic別referenceや既存Markdown pageへ分離します。

この方針なら、人間向けサイト、agent skill、MCP resource、RAG chunkがすべて同じMarkdown正本から生成されます。
