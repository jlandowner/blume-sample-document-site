---
id: api-reference.crds
title: CRDs
description: プラットフォームが提供するCustom Resource Definition。
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
  - crd
  - kubernetes
canonical_url: /api-reference/crds/
---

# CRDs

## PlatformApp

`PlatformApp` は、アプリケーションのownerとplatform連携設定を表します。

```yaml
apiVersion: platform.example.com/v1
kind: PlatformApp
metadata:
  name: invoice-api
  namespace: app-payments-invoice-prod
spec:
  owner: payments-team
  tier: backend
  publicIngress: false
  observability:
    dashboard: standard
```

## 必須field

| Field | 必須 | 説明 |
| --- | --- | --- |
| `spec.owner` | yes | workloadの責任team |
| `spec.tier` | yes | `frontend`, `backend`, `worker`, `batch` のいずれか |
| `spec.publicIngress` | yes | public ingressを公開するかどうか |

## 検証方法

```bash
kubectl explain platformapp.spec
platformctl validate manifests ./k8s
```
