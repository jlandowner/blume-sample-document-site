---
id: design.requirements-and-architecture
title: 要件とアーキテクチャ
description: Kubernetesプラットフォームドキュメントサイトの要件とアーキテクチャ。
type: overview
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-07-19
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

アプリケーションチームが、環境構成、プラットフォーム制約、デプロイ手順、API仕様、提供ツール、アプリ側チェックリストへ素早く到達できることを最優先にします。同じMarkdown正本から、人間向けサイト、`llms.txt`、MCP検索・取得APIを生成します。

## 優先順位

1. 検索性と必要情報への到達性。
2. 安定したドキュメント構造とowner管理。
3. Markdownを正本にすること。
4. AI/MCP向けartifactの自動生成。
5. 単一コンテナで動くportableなruntime。
6. CIによる検証、build、deploy。
7. 見た目の作り込みより、情報設計の明確さ。

## 採用stack

実装は **Blume** を採用します。

理由:

- Markdownを正本として扱える。
- navigation、検索、`llms.txt`、MCP endpointを同じbuildから生成できる。
- 人間向けサイトとAI向けMCPを1つのNode serverで配信できる。
- ブラウザ検索とMCP検索を同じ検索providerに寄せられる。
- `i18n.defaultLocale: "ja"` により日本語検索を同じ設定で扱える。
- runtimeを単一コンテナに閉じやすい。

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
- page metadata、source path、canonical URL、tag、heading、ownerを保持する。
- documentation mapとして `llms.txt` を生成する。
- MCP endpointで検索とpage取得を提供する。
- page idとheading anchorを安定させ、citationを壊しにくくする。
- ブラウザ検索とMCP検索の検索結果を同じproviderに揃える。

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
last_reviewed: 2026-07-19
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
- headingは検索とAI取得の手がかりになるため、安定した名前にする。
- 抽象的な説明だけでなく、具体的な値、command、manifest例を書く。
- 手順ページに制約本文を重複させず、正本となる制約ページへリンクする。
- checklist項目は、根拠となるpageへリンクする。
- 環境差分は表で明示する。
- 必須動作をnoteの中だけに隠さない。
- parameter listや比較は表で書く。

## MCP access設計

AIエージェントはBlumeのMCP endpoint `/mcp` を使います。

代表的なtool:

- `search_docs`: queryからpage候補を返す。
- `get_page`: routeからMarkdown本文を返す。

日本語検索は `blume.config.ts` の `i18n.defaultLocale: "ja"` で有効化します。MCP検索のsmoke testは `make test-mcp-search` で実行します。

## Container設計

runtimeは単一コンテナです。

```text
blume-docs
  - Blume siteを配信する。
  - /mcp でBlume内蔵MCP serverを公開する。
  - /llms.txt を配信する。
```

Nginx、Python MCP server、検索専用sidecarは使いません。Helmで導入する場合も、この1つのHTTP serviceを公開します。

## CI/CD設計

CI stage:

1. Blume strict buildを実行する。
2. MCP日本語検索smoke testを実行する。
3. container imageをbuildする。
4. imageをpushする。
5. Helmでdeployする。

document-only changeでも同じ検証とdeploy pathを通します。

## 初期実装範囲

- Blume設定とsample page。
- Blume単一コンテナ用Dockerfile。
- MCP日本語検索smoke test。
- ドキュメント運用policy。

## 未決事項

- human-facing siteの認証方式。
- CI providerとcontainer registry。
- deployment namespaceとingress controller。
- API仕様を手書き、OpenAPI/CRD生成、または併用のどれにするか。
