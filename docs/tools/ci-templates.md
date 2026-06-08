---
id: tools.ci-templates
title: CIテンプレート
description: アプリケーションの検証とデプロイに使う標準CIテンプレート。
type: tool-reference
owner: developer-experience
status: draft
review_cycle: monthly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
tags:
  - ci
  - deploy
canonical_url: /tools/ci-templates/
---

# CIテンプレート

## 必須job

| Job | 必須 | 用途 |
| --- | --- | --- |
| `platform-validate` | yes | manifestとmetadataを検証する |
| `platform-deploy-dev` | yes | merge済み変更をdevへデプロイする |
| `platform-deploy-production` | production appのみ | tag付きreleaseをproductionへデプロイする |

## 例

```yaml
include:
  - project: platform/ci-templates
    file: k8s-app.yml

variables:
  PLATFORM_SERVICE: invoice-api
  PLATFORM_CHART: ./chart
```

## 生成される証跡

テンプレートは、validation結果、deployment ID、release version、dashboard linkをCI artifactとして保存します。
