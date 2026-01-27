
# Output the Firewall details so they can be used in the spoke networks
output "firewall_policy_id" {
  value = { for k, v in module.firewall : k => v.firewall_policy_id }
}

output "firewall_private_ip_addresses" {
  value = { for k, v in module.firewall : k => v.private_ip_address }
}

output "frontdoor_profile" {
  value = module.frontdoor_profile
}

# Output the DNS resolver inbound private ip addresses so they can be used in the private endpoint modules
output "private_dns_resolver_inbound_ips" {
  value = module.private_dns_resolver
}

# Output the private DNS zone IDs so they can be used in private endpoint modules
output "private_dns_zones" {
  value = module.private_dns_zones
}

output "networking_rg_name" {
  value = { for k, v in azurerm_resource_group.rg_hub : k => v.name }
}

output "private_endpoint_rg_name" {
  value = { for k, v in azurerm_resource_group.rg_private_endpoints : k => v.name }
}

output "subnets_hub" {
  value = module.subnets_hub
}
