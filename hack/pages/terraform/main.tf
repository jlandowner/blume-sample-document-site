locals {
  pages_domain         = "${var.pages_project_name}.pages.dev"
  pages_preview_domain = "*.${var.pages_project_name}.pages.dev"
}

resource "cloudflare_pages_project" "docs" {
  account_id        = var.cloudflare_account_id
  name              = var.pages_project_name
  production_branch = var.production_branch
}

resource "cloudflare_zero_trust_access_application" "pages" {
  account_id = var.cloudflare_account_id
  name       = "${var.pages_project_name} Pages Preview"
  domain     = local.pages_domain
  type       = "self_hosted"
  destinations = [
    {
      type = "public"
      uri  = local.pages_domain
    },
    {
      type = "public"
      uri  = local.pages_preview_domain
    }
  ]
  session_duration           = var.access_session_duration
  allowed_idps               = [var.github_identity_provider_id]
  auto_redirect_to_identity  = true
  app_launcher_visible       = false
  enable_binding_cookie      = true
  http_only_cookie_attribute = true
  same_site_cookie_attribute = "lax"
  service_auth_401_redirect  = true
  skip_interstitial          = true

  policies = [
    {
      name       = "Allow ${var.github_org_name}"
      decision   = "allow"
      precedence = 1
      include = [
        {
          github_organization = {
            identity_provider_id = var.github_identity_provider_id
            name                 = var.github_org_name
          }
        }
      ]
    }
  ]
}
