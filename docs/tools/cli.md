---
id: tools.cli
title: プラットフォームCLI
description: platformctlコマンドラインツールの仕様。
type: tool-reference
owner: developer-experience
status: reviewed
review_cycle: monthly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - app-team
tags:
  - cli
  - platformctl
canonical_url: /tools/cli/
---

# プラットフォームCLI

## インストール

CI imageには `platformctl` が含まれています。ローカルインストールは任意です。

```bash
platformctl version
```

## コマンド

| コマンド | 用途 |
| --- | --- |
| `platformctl validate manifests` | Kubernetes manifestをplatform policyに照らして検証する |
| `platformctl deploy` | アプリケーションをデプロイする |
| `platformctl status` | 実行状態を表示する |
| `platformctl rollback` | releaseをロールバックする |
| `platformctl secret` | アプリケーションSecretを管理する |

## Manifestを検証する

```bash
platformctl validate manifests ./k8s
```

## デプロイする

```bash
platformctl deploy --service invoice-api --env dev --image registry.example.com/payments/invoice-api:2026.06.07.1 --chart ./chart
```

## Exit code

| Code | 意味 |
| --- | --- |
| 0 | 成功 |
| 2 | 検証失敗 |
| 3 | 認証失敗 |
| 4 | プラットフォームAPI request失敗 |
