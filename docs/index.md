---
id: home
title: K8sプラットフォームドキュメント
description: アプリケーションチーム向けの社内Kubernetesプラットフォームドキュメント。
type: overview
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - app-team
  - platform-team
tags:
  - kubernetes
  - platform
canonical_url: /
---

# K8sプラットフォームドキュメント

このサイトは、アプリケーションチームが社内Kubernetesプラットフォームを安全に使うためのドキュメントです。

## 最初に読むページ

| 目的 | ページ |
| --- | --- |
| プラットフォームの全体像を知る | [プラットフォーム概要](overview/platform-summary.md) |
| 環境差分を確認する | [環境一覧](environments/index.md) |
| アプリが守るべき制約を確認する | [制約一覧](constraints/index.md) |
| アプリをデプロイする | [アプリケーションのデプロイ](procedures/deploy-application.md) |
| 本番リリース前に確認する | [本番準備チェックリスト](app-checklists/production-readiness.md) |
| 失敗時の切り分けを行う | [よくある失敗](runbooks/common-failures.md) |

## ドキュメントの読み方

- 仕様や制約は `制約` と `API仕様` を正とします。
- 作業手順は `作業手順` を正とします。
- チェックリストは該当する制約や手順への入口です。
- 障害調査では `ランブック` から症状で探してください。
