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

# アプリケーションのデプロイ

## 概要

アプリケーションはCIテンプレートから `platformctl deploy` を実行してデプロイします。productionへのデプロイ前には [本番準備チェックリスト](../app-checklists/production-readiness.md) を満たしてください。

## 前提条件

- namespaceが作成済み。
- container imageがapproved registryにpush済み。
- Helm chartがrepositoryに含まれている。
- resource requestsとlimitsが設定済み。
- productionではchange requestが承認済み。

## 入力

| 入力 | 例 |
| --- | --- |
| service | `invoice-api` |
| env | `dev` または `production` |
| image | `registry.example.com/payments/invoice-api:2026.06.07.1` |
| chart | `./chart` |

## devへデプロイする

```bash
platformctl deploy \
  --service invoice-api \
  --env dev \
  --image registry.example.com/payments/invoice-api:2026.06.07.1 \
  --chart ./chart
```

## productionへデプロイする

```bash
platformctl deploy \
  --service invoice-api \
  --env production \
  --image registry.example.com/payments/invoice-api:2026.06.07.1 \
  --chart ./chart \
  --change-request CHG-12345
```

## 確認

```bash
platformctl status --service invoice-api --env production
kubectl -n app-payments-invoice-prod get deploy,po,ingress
```

正常時は次の状態になります。

- Deploymentのavailable replicasがdesired replicasと一致する。
- Podが `Ready` になる。
- Ingressにhostnameが割り当てられる。
- 標準dashboardでerror rateが上昇していない。

## ロールバック

問題がある場合は [ロールバック](rollback.md) に従って直前のreleaseへ戻します。

## トラブルシュート

| 症状 | 確認先 |
| --- | --- |
| Podが起動しない | [よくある失敗](../runbooks/common-failures.md) |
| ingressに到達できない | [ネットワーク](../environments/network.md) |
| CI validationが失敗する | [プラットフォーム上限](../constraints/platform-limits.md) |
