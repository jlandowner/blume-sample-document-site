---
id: constraints.platform-limits
title: プラットフォーム上限
description: プラットフォームの上限値とサポートしないKubernetes構成。
type: constraint
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
tags:
  - constraint
  - limit
canonical_url: /constraints/platform-limits/
---

# プラットフォーム上限

## Workload上限

| 項目 | dev | production |
| --- | --- | --- |
| Deployment replicas | 1-5 | 2-20 |
| CronJob concurrency | `Forbid` 推奨 | `Forbid` 必須 |
| Container memory limit | 2Giまで | 8Giまで |
| Container CPU limit | 2 coresまで | 4 coresまで |

## サポートしない構成

以下の構成は禁止です。

- privileged container
- hostPath volume
- hostNetwork
- NodePort Service
- 独自DBをStatefulSetで運用する構成
- `latest` image tag

## 検証方法

CIテンプレートはmanifestに対して次の検査を行います。

```bash
platformctl validate manifests ./k8s
```

違反した場合は、該当する制約名とmanifest pathが出力されます。
