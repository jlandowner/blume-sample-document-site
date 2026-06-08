---
id: overview.platform-summary
title: プラットフォーム概要
description: 社内Kubernetesプラットフォームとサポート対象workloadの概要。
type: overview
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
  - platform-team
tags:
  - overview
  - kubernetes
canonical_url: /overview/platform-summary/
---

# プラットフォーム概要

社内Kubernetesプラットフォームは、アプリケーションチームが標準化された方法でWeb API、worker、batch workloadを運用するための共通基盤です。

## 提供範囲

| 項目 | 提供内容 |
| --- | --- |
| Kubernetesクラスタ | dev、productionの共有クラスタ |
| Ingress | HTTP/HTTPS ingress、TLS終端 |
| 可観測性 | metrics、logs、標準dashboard |
| デプロイ | CIテンプレート、platform CLI、Helm release |
| セキュリティ | namespace分離、RBAC、Secret管理方針 |

## サポートするworkload

- ステートレスなHTTP API
- バックグラウンドworker
- CronJob
- 社内向けtool

## サポートしないworkload

- Stateful databaseの独自運用
- privileged container
- hostNetworkを必要とするpod
- Node local storageに依存する構成

詳細な禁止事項は [プラットフォーム上限](../constraints/platform-limits.md) を参照してください。

## 関連ページ

- [開発環境](../environments/dev.md)
- [本番環境](../environments/production.md)
- [アプリケーションのデプロイ](../procedures/deploy-application.md)
