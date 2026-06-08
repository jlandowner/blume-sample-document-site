---
id: api-reference.platform-api
title: プラットフォームAPI
description: デプロイと状態確認のためにplatform toolが利用するHTTP API。
type: api-reference
owner: platform-team
status: draft
review_cycle: monthly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
  - platform-team
tags:
  - api
  - deploy
canonical_url: /api-reference/platform-api/
---

# プラットフォームAPI

## Base URL

| 環境 | Base URL |
| --- | --- |
| dev | `https://platform-api.dev.example.internal` |
| production | `https://platform-api.prod.example.internal` |

## 認証

クライアントはCIが発行するOIDC tokenで認証します。tokenにはservice、repository、environmentのclaimが必要です。

## Deploymentを作成する

```http
POST /v1/deployments
Authorization: Bearer <token>
Content-Type: application/json
```

リクエスト:

```json
{
  "service": "invoice-api",
  "environment": "production",
  "image": "registry.example.com/payments/invoice-api:2026.06.07.1",
  "chartPath": "./chart",
  "changeRequest": "CHG-12345"
}
```

レスポンス:

```json
{
  "deploymentId": "dep_01JZ0000000000000000000000",
  "status": "accepted",
  "statusUrl": "/v1/deployments/dep_01JZ0000000000000000000000"
}
```

## Deployment状態を取得する

```http
GET /v1/deployments/{deploymentId}
Authorization: Bearer <token>
```

## エラーコード

| Code | 意味 | 対応 |
| --- | --- | --- |
| `POLICY_VIOLATION` | manifestがplatform制約に違反している | manifestを修正してvalidationを再実行する |
| `CHANGE_REQUIRED` | production deployにchange requestが必要 | 承認済みchange requestを指定する |
| `QUOTA_EXCEEDED` | 要求resourceがnamespace quotaを超えている | request値を下げるかquota変更を依頼する |
