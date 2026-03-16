output "internal_url" {
  value = module.webapp.url
}

output "external_url" {
  value = var.features.front_door ? local.external_url : null
}
