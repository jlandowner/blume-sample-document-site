---
id: environments.dev
title: 開発環境
description: 開発用Kubernetes環境の構成と利用ルール。
type: environment
owner: platform-team
status: reviewed
review_cycle: monthly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
tags:
  - environment
  - dev
canonical_url: /environments/dev/
---

# 開発環境

## 概要

dev環境はアプリケーションの開発、結合検証、CIからの自動デプロイに使用します。

## クラスタ

| 項目 | 値 |
| --- | --- |
| cluster id | `k8s-dev-01` |
| region | `ap-northeast-1` |
| ingress domain | `*.dev.example.internal` |
| default namespace pattern | `app-{team}-{service}-dev` |

## 許可される操作

- CIからの自動デプロイ
- 手動rollback
- Secretの作成と更新
- 一時的なreplica数変更

## 制約

- `LoadBalancer` Serviceは作成できません。
- public ingressは作成できません。
- `latest` tagのimageは使用できません。

## 関連ページ

- [アプリケーションのデプロイ](../procedures/deploy-application.md)
- [命名規約](../constraints/naming-conventions.md)
