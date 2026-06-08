---
id: environments.production
title: 本番環境
description: 本番用Kubernetes環境の構成と利用ルール。
type: environment
owner: platform-team
status: reviewed
review_cycle: monthly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
  - sre-team
tags:
  - environment
  - production
canonical_url: /environments/production/
---

# 本番環境

## 概要

production環境はユーザー向け本番workloadを運用する環境です。変更はCI経由で行い、手動変更は障害対応時に限定します。

## クラスタ

| 項目 | 値 |
| --- | --- |
| cluster id | `k8s-prod-01` |
| region | `ap-northeast-1` |
| ingress domain | `*.example.com`, `*.prod.example.internal` |
| default namespace pattern | `app-{team}-{service}-prod` |

## 必須条件

- replica数は2以上。
- readiness probeとliveness probeを設定する。
- resource requestsとlimitsを設定する。
- Secret更新は承認済みchange requestに紐付ける。
- public ingressはsecurity review済みのサービスのみ許可する。

## 変更可能時間

標準の本番変更時間は平日 10:00-17:00 JST です。緊急対応ではincident commanderの承認を記録してください。

## 関連ページ

- [本番準備チェックリスト](../app-checklists/production-readiness.md)
- [セキュリティポリシー](../constraints/security-policy.md)
