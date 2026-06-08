---
id: runbooks.common-failures
title: よくある失敗
description: platform deployとruntimeでよく起きる失敗の切り分けガイド。
type: runbook
owner: sre-team
status: reviewed
review_cycle: monthly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
  - sre-team
tags:
  - runbook
  - troubleshooting
canonical_url: /runbooks/common-failures/
---

# よくある失敗

## Pod起動失敗

### 症状

- Podが `Pending`、`CrashLoopBackOff`、`ImagePullBackOff` のままになる。
- Deploymentのavailable replicasがdesired replicasに届かない。

### 確認

```bash
kubectl -n app-payments-invoice-prod get pod
kubectl -n app-payments-invoice-prod describe pod <pod-name>
kubectl -n app-payments-invoice-prod logs <pod-name>
```

### よくある原因

| 原因 | 対応 |
| --- | --- |
| image tagが存在しない | image URLとtagを確認する |
| resource quotaを超えている | requestsを下げるかquota変更を依頼する |
| Secret keyが不足している | [Secret管理](../procedures/secrets.md) を確認する |
| probeが失敗している | readiness/liveness probe pathを確認する |

## Ingress不通

### 症状

- ingressからHTTP 404が返る。
- TLS証明書が割り当たっていない。
- hostnameが名前解決できない。

### 確認

```bash
kubectl -n app-payments-invoice-prod get ingress
kubectl -n app-payments-invoice-prod describe ingress invoice-api
```

### 対応

- ingress classが `internal` または承認済み `public` であることを確認する。
- hostnameが環境のdomainと一致していることを確認する。
- service portがingress backendと一致していることを確認する。

## エスカレーション

service名、環境、deployment ID、失敗しているコマンド出力を添えて `#platform-support` にエスカレーションします。
