output "pages_project_name" {
  description = "Cloudflare Pages project name."
  value       = cloudflare_pages_project.docs.name
}

output "pages_url" {
  description = "Cloudflare Pages production URL protected by Access."
  value       = "https://${local.pages_domain}"
}

output "pages_preview_url_pattern" {
  description = "Cloudflare Pages preview URL pattern protected by Access."
  value       = "https://${local.pages_preview_domain}"
}

output "access_application_id" {
  description = "Cloudflare Access application ID."
  value       = cloudflare_zero_trust_access_application.pages.id
}
