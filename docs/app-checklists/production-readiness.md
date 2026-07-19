---
id: app-checklists.production-readiness
title: 本番準備チェックリスト
description: アプリケーションをproductionで開始するためのチェックリスト。
type: checklist
owner: platform-team
status: reviewed
review_cycle: monthly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - app-team
  - sre-team
tags:
  - checklist
  - production
canonical_url: /app-checklists/production-readiness/
---

# 本番準備チェックリスト

## 必須チェック

| チェック | 必要な証跡 | 参照 |
| --- | --- | --- |
| Namespaceが命名規約に従っている | Namespace名 | [命名規約](../constraints/naming-conventions.md) |
| replica数が2以上である | Deployment manifest | [本番環境](../environments/production.md) |
| readiness probeがある | Deployment manifest | [本番環境](../environments/production.md) |
| resource requestsとlimitsが設定されている | Deployment manifest | [プラットフォーム上限](../constraints/platform-limits.md) |
| image tagがimmutableである | Image URL | [プラットフォーム上限](../constraints/platform-limits.md) |
| Secret値がGitに含まれていない | repository scan結果 | [セキュリティポリシー](../constraints/security-policy.md) |
| public ingressのsecurity reviewが完了している | review ticket | [セキュリティポリシー](../constraints/security-policy.md) |
| rollback commandを検証済み | CI証跡 | [ロールバック](../procedures/rollback.md) |

## 判定

本番開始前にすべての必須checkを満たしてください。例外はsecurity-teamまたはplatform-teamの承認を記録します。
