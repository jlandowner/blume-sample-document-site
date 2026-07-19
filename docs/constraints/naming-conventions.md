---
id: constraints.naming-conventions
title: 命名規約
description: namespace、release、workload、labelの命名ルール。
type: constraint
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - app-team
tags:
  - naming
  - constraint
canonical_url: /constraints/naming-conventions/
---

# 命名規約

## Namespace

```text
app-{team}-{service}-{env}
```

例:

```text
app-payments-invoice-prod
```

## Labels

必須label:

| label | 例 |
| --- | --- |
| `app.kubernetes.io/name` | `invoice-api` |
| `app.kubernetes.io/part-of` | `payments` |
| `platform.example.com/owner` | `payments-team` |
| `platform.example.com/env` | `production` |

## Release名

Helm release名はservice名と一致させます。

```bash
helm upgrade --install invoice-api ./chart
```
