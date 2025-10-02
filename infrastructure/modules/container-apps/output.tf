output "internal_url" {
  value = module.webapp.url
}

output "external_url" {
  value = var.features.front_door ? "https://${module.frontdoor_endpoint[0].custom_domains["${var.environment}-domain"].host_name}/" : null
}
