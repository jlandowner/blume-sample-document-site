---
id: procedures.rollback
title: ロールバック
description: アプリケーションreleaseをロールバックする手順。
type: procedure
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
  - rollback
  - incident
canonical_url: /procedures/rollback/
---

# ロールバック

## 概要

直近のデプロイで障害や重大な劣化が発生した場合、前回の正常releaseへ戻します。

## 現在のreleaseを確認する

```bash
platformctl releases --service invoice-api --env production
```

## ロールバックを実行する

```bash
platformctl rollback \
  --service invoice-api \
  --env production \
  --to previous \
  --reason "error rate increased after CHG-12345"
```

## 確認

```bash
platformctl status --service invoice-api --env production
```

確認項目:

- Podが前回imageで起動している。
- error rateが通常範囲に戻っている。
- incident timelineにrollback時刻を記録した。
