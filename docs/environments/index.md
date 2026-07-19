---
id: environments.index
title: 環境一覧
description: プラットフォームクラスタの環境一覧と主な差分。
type: environment
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - app-team
tags:
  - environment
  - cluster
canonical_url: /environments/
---

# 環境一覧

## 環境一覧

| 環境 | 用途 | 変更頻度 | 承認 |
| --- | --- | --- | --- |
| dev | 開発、結合検証 | 高 | 不要 |
| production | 本番サービス | 低 | 必須 |

## 主な差分

| 項目 | dev | production |
| --- | --- | --- |
| replica最小数 | 1 | 2 |
| ingress公開 | internalのみ | internalまたはpublic |
| Secret更新 | app-team可 | 承認後 |
| resource quota | 緩い | 厳格 |

詳細は [開発環境](dev.md) と [本番環境](production.md) を参照してください。
