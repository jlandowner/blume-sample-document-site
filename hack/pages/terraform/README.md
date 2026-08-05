# Cloudflare Pages Preview

Cloudflare Pages に静的ビルドを配置し、Cloudflare Access の GitHub 認証で閲覧者を制限するための Terraform 構成です。

## 前提

- Cloudflare Zero Trust で GitHub identity provider を作成済みであること。
- GitHub organization は `cosmo-workspace` を使うこと。
- `cosmo-workspace` に所属するユーザーは production URL と preview URL の確認環境へアクセスできます。
- Cloudflare API token には Pages と Zero Trust Access application/policy を管理できる権限が必要です。

## 入力値

- `cloudflare_account_id`: Cloudflare account ID。
- `github_identity_provider_id`: Cloudflare Access の GitHub identity provider ID。
- `pages_project_name`: Cloudflare Pages project 名。デフォルトは `sample-document-site`。
- `production_branch`: production branch。デフォルトは `main`。
- `github_org_name`: 許可する GitHub organization。デフォルトは `cosmo-workspace`。

## 保護対象

- `sample-document-site.pages.dev`
- `*.sample-document-site.pages.dev`

## 確認

ホストに Terraform を入れず、コンテナで確認します。

```sh
tmpdir="$(mktemp -d)"
cp -R hack/pages/terraform/. "$tmpdir/"
docker run --rm -v "$tmpdir:/workspace" -w /workspace hashicorp/terraform:1.10 init -backend=false
docker run --rm -v "$tmpdir:/workspace" -w /workspace hashicorp/terraform:1.10 fmt -check
docker run --rm -v "$tmpdir:/workspace" -w /workspace hashicorp/terraform:1.10 validate
```

## 適用

```sh
terraform init
terraform apply \
  -var='cloudflare_account_id=...' \
  -var='github_identity_provider_id=...'
```
