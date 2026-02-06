output "internal_url" {
  value = module.webapp.url
}

# Commented out as the front door endpoints is not being used at the moment (awaiting for DNS to be sorted), but this can be re-enabled if front door is added back in.
# output "external_url" {
#   value = var.features.front_door ? "https://${module.frontdoor_endpoint[0].custom_domains["${var.environment}-domain"].host_name}/" : null
# }
