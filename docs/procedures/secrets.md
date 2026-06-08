---
id: procedures.secrets
title: Secret管理
description: アプリケーションSecretを管理する手順。
type: procedure
owner: security-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
tags:
  - secret
  - security
canonical_url: /procedures/secrets/
---

# Secret管理

## 概要

Secret値はGitに保存せず、環境ごとのSecret管理フローで登録します。

## devでSecretを作成する

```bash
platformctl secret set \
  --service invoice-api \
  --env dev \
  --name database-url \
  --from-literal value="$DATABASE_URL"
```

## productionでSecretを更新する

```bash
platformctl secret set \
  --service invoice-api \
  --env production \
  --name database-url \
  --from-literal value="$DATABASE_URL" \
  --change-request CHG-12345
```

## 確認

```bash
platformctl secret list --service invoice-api --env production
```

Secret値そのものは表示されません。存在、更新時刻、参照workloadのみ確認できます。
