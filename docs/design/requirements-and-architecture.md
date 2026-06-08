---
id: design.requirements-and-architecture
title: 要件とアーキテクチャ
description: Kubernetesプラットフォームドキュメントサイトの要件とアーキテクチャ。
type: overview
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - platform-team
tags:
  - design
  - architecture
canonical_url: /design/requirements-and-architecture/
---

# 要件とアーキテクチャ

## 目的

このサイトは、社内Kubernetesプラットフォームを人間とAI/MCP clientの両方から読める形で文書化します。

アプリケーションチームが、環境構成、プラットフォーム制約、デプロイ手順、API仕様、提供ツール、アプリ側チェックリストへ素早く到達できることを最優先にします。同じMarkdown正本から、人間向けサイト、`llms.txt`、`docs-index.json`、RAG用chunkを生成します。

## 優先順位

1. 検索性と必要情報への到達性。
2. 安定したドキュメント構造とowner管理。
3. Markdownを正本にすること。
4. AI/RAG向けartifactの自動生成。
5. Helmで導入できるportableなruntime。
6. CIによる検証、build、deploy。
7. 見た目の作り込みより、情報設計の明確さ。

## 推奨stack

初期実装は **MkDocs + Material for MkDocs** を採用します。

理由:

- Markdownを正本として扱いやすい。
- navigationを `mkdocs.yml` で明示でき、reviewしやすい。
- static siteとしてbuildでき、Nginxなど単純なweb serverで配信できる。
- search、tag、目次、admonition、code blockを標準的に扱える。
- `llms.txt`、`docs-index.json`、`chunks.jsonl` の生成scriptを追加しやすい。
- runtimeを1コンテナに閉じやすく、必要に応じてMCP用sidecarを追加できる。

## 人間向け要件

- domain別のglobal navigationを提供する。
- 各pageにpage内目次を提供する。
- full-text searchを提供する。
- 環境、読者、lifecycle、API、運用領域をtagで表現する。
- 各pageに予測可能なURLを持たせる。
- `owner`、`status`、`last_reviewed`、`platform_versions` をfrontmatterに持たせる。
- 正本となる制約・仕様と、例・補足・履歴を区別する。

## AI/MCP向け要件

- Markdown sourceはJavaScript実行なしで読める。
- page metadata、source path、canonical URL、tag、heading、ownerを含むindexを生成する。
- documentation mapとして `llms.txt` を生成する。
- 全文参照用に `llms-full.txt` を生成する。
- heading単位でRAG用 `chunks.jsonl` を生成する。
- page idとheading anchorを安定させ、citationを壊しにくくする。
- まずはstatic artifact配信で始め、必要になったらMCP serverを追加する。

## 情報設計

top-level構成:

```text
docs/
  index.md
  overview/
  environments/
  constraints/
  procedures/
  api-reference/
  tools/
  app-checklists/
  runbooks/
  operations/
  design/
  authoring/
```

この構成では、概念説明、環境差分、制約、作業手順、仕様、提供ツール、チェックリスト、障害時の切り分けを分離します。長いoverviewページに運用手順を埋め込まず、検索結果から目的のpageへ直接到達できる粒度を保ちます。

## ページ種別

| type | 用途 |
| --- | --- |
| `overview` | 全体像、対象範囲、設計方針を説明する |
| `environment` | 環境別の設定、差分、利用ルールを説明する |
| `constraint` | アプリチームが守るべき制約の正本を書く |
| `procedure` | 繰り返し実行する作業手順を書く |
| `api-reference` | API、CRD、webhook、schemaを説明する |
| `tool-reference` | CLI、CI template、dashboardなど提供ツールを説明する |
| `checklist` | release前やreview時の確認項目を列挙する |
| `runbook` | 障害時の症状、確認、原因、対応、エスカレーションを書く |

## 必須frontmatter

```yaml
---
id: procedures.deploy-application
title: アプリケーションのデプロイ
description: Kubernetesプラットフォーム上でアプリケーションをデプロイする標準手順。
type: procedure
owner: platform-team
status: reviewed
review_cycle: monthly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
tags:
  - deploy
  - ci
  - helm
canonical_url: /procedures/deploy-application/
---
```

## 執筆ルール

- 1 pageは1つの主な問いに答える。
- 背景説明より先に答えを書く。
- headingはRAG chunkの境界になるため、安定した名前にする。
- 抽象的な説明だけでなく、具体的な値、command、manifest例を書く。
- 手順ページに制約本文を重複させず、正本となる制約ページへリンクする。
- checklist項目は、根拠となるpageへリンクする。
- 環境差分は表で明示する。
- 必須動作をnoteの中だけに隠さない。
- parameter listや比較は表で書く。

## RAG artifact設計

build時に次を生成します。

```text
ai/
  docs-index.json
  chunks.jsonl
  llms.txt
  llms-full.txt
```

`docs-index.json` はpage単位のmetadataを持ちます。`chunks.jsonl` はheading単位のtext、heading path、tag、source path、canonical URLを持ちます。RAG最適化は手動ファイルで行わず、Markdownの構造とfrontmatterを直すだけで再生成されるようにします。

## MCP access設計

初期状態ではstatic artifactを配信します。interactive retrievalやtool連携が必要になったら、optional containerとしてMCP serverを追加します。

想定resource:

- `docs://index`: `docs-index.json` を返す。
- `docs://page/{id}`: page単位のMarkdownを返す。
- `docs://chunk/{chunk_id}`: chunk単位のtextを返す。
- `docs://search?q=...`: pageまたはchunk検索結果を返す。

## ContainerとHelm設計

default runtime:

```text
docs-web
  - MkDocsのstatic outputを配信する。
  - /ai/docs-index.json、/ai/chunks.jsonl、/ai/llms.txtを配信する。

docs-mcp optional
  - 同じgenerated artifactを読む。
  - MCP resourceを公開する。
```

Helm valuesでimage、replica数、ingress、base URL、認証方式、resource request/limit、cache header、MCP containerの有効化を設定できるようにします。

## CI/CD設計

CI stage:

1. Markdownをlintする。
2. frontmatter schemaを検証する。
3. linkを検証する。
4. navigation coverageを検証する。
5. AI artifactを生成する。
6. static siteをbuildする。
7. HTMLとAI artifactのsmoke testを行う。
8. container imageをbuildする。
9. imageをpushする。
10. Helmでdeployする。

document-only changeでも同じ検証とdeploy pathを通します。

## 初期実装範囲

- MkDocs設定とsample page。
- frontmatter検証script。
- static配信用Dockerfile。
- ドキュメント運用policy。

## 未決事項

- human-facing siteの認証方式。
- MCP serverを初回releaseに含めるか。
- CI providerとcontainer registry。
- deployment namespaceとingress controller。
- AI artifact生成script。
- API仕様を手書き、OpenAPI/CRD生成、または併用のどれにするか。
