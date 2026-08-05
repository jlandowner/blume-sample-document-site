---
id: app-checklists.deployment-review
title: デプロイレビュー
description: production deployの変更内容を確認するためのチェックリスト。
type: checklist
owner: platform-team
status: reviewed
review_cycle: monthly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - app-team
tags:
  - checklist
  - deploy
canonical_url: /app-checklists/deployment-review/
---

# デプロイレビュー

## デプロイ前

| チェック | 参照 |
| --- | --- |
| change requestが承認済み | [アプリケーションのデプロイ](/procedures/deploy-application) |
| image tagがrelease noteと一致している | [アプリケーションのデプロイ](/procedures/deploy-application) |
| manifest validationが成功している | [プラットフォーム上限](/constraints/platform-limits) |
| Secret変更がreview済み | [Secret管理](/procedures/secrets) |

## デプロイ後

| チェック | 参照 |
| --- | --- |
| Deployment statusがhealthy | [アプリケーションのデプロイ](/procedures/deploy-application) |
| error rateが通常範囲内 | [よくある失敗](/runbooks/common-failures) |
| rollback経路が利用可能 | [ロールバック](/procedures/rollback) |
