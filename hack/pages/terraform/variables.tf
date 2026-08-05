variable "cloudflare_account_id" {
  description = "Cloudflare account ID."
  type        = string
}

variable "pages_project_name" {
  description = "Cloudflare Pages project name."
  type        = string
  default     = "sample-document-site"
}

variable "production_branch" {
  description = "Cloudflare Pages production branch."
  type        = string
  default     = "main"
}

variable "github_identity_provider_id" {
  description = "Cloudflare Access GitHub identity provider ID."
  type        = string
}

variable "github_org_name" {
  description = "GitHub organization allowed to access the Pages preview."
  type        = string
  default     = "cosmo-workspace"
}

variable "access_session_duration" {
  description = "Cloudflare Access session duration."
  type        = string
  default     = "24h"
}
