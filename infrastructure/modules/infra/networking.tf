module "main_vnet" {
  source = "../dtos-devops-templates/infrastructure/modules/vnet"

  name                                         = "vnet-${var.environment}-uks-${var.app_short_name}"
  resource_group_name                          = azurerm_resource_group.main.name
  location                                     = var.region
  dns_servers                                  = var.features.private_networking ? [data.azurerm_private_dns_resolver_inbound_endpoint.this[0].ip_configurations[0].private_ip_address] : []
  log_analytics_workspace_id                   = module.log_analytics_workspace_audit.id
  monitor_diagnostic_setting_vnet_enabled_logs = ["VMProtectionAlerts"]
  monitor_diagnostic_setting_vnet_metrics      = ["AllMetrics"]
  vnet_address_space                           = var.vnet_address_space
}

module "postgres_subnet" {
  source = "../dtos-devops-templates/infrastructure/modules/subnet"

  name                                                           = "snet-postgres"
  resource_group_name                                            = azurerm_resource_group.main.name
  vnet_name                                                      = module.main_vnet.name
  address_prefixes                                               = [cidrsubnet(var.vnet_address_space, 7, 1)]
  create_nsg                                                     = false
  location                                                       = var.region
  monitor_diagnostic_setting_network_security_group_enabled_logs = []
  log_analytics_workspace_id                                     = module.log_analytics_workspace_audit.id
  network_security_group_name                                    = "nsg-postgres"
}


data "azurerm_private_dns_resolver" "this" {
  count = var.features.private_networking ? 1 : 0

  provider = azurerm.hub

  name                = "${var.hub}-uks-hub-private-dns-zone-resolver"
  resource_group_name = "rg-hub-${var.hub}-uks-private-dns-zones"
}

data "azurerm_private_dns_resolver_inbound_endpoint" "this" {
  count = var.features.private_networking ? 1 : 0

  provider = azurerm.hub

  name                    = "private-dns-resolver-inbound-endpoint"
  private_dns_resolver_id = data.azurerm_private_dns_resolver.this[0].id
}

data "azurerm_virtual_network" "hub" {
  count = var.features.hub_and_spoke ? 1 : 0

  provider = azurerm.hub

  name                = module.hub_config.names.virtual-network
  resource_group_name = local.hub_vnet_rg_name
}

module "peering_spoke_hub" {
  count = var.features.hub_and_spoke ? 1 : 0

  source = "../dtos-devops-templates/infrastructure/modules/vnet-peering"

  name                = "${module.main_vnet.name}-to-hub-peering"
  resource_group_name = azurerm_resource_group.main.name
  vnet_name           = module.main_vnet.name
  remote_vnet_id      = data.azurerm_virtual_network.hub[0].id

  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false

  use_remote_gateways = false
}

module "peering_hub_spoke" {
  count = var.features.hub_and_spoke ? 1 : 0

  providers = {
    azurerm = azurerm.hub
  }

  source = "../dtos-devops-templates/infrastructure/modules/vnet-peering"

  name                = "hub-to-${module.main_vnet.name}-peering"
  resource_group_name = local.hub_vnet_rg_name
  vnet_name           = data.azurerm_virtual_network.hub[0].name
  remote_vnet_id      = module.main_vnet.vnet.id

  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false

  use_remote_gateways = false
}


module "container_app_subnet" {
  source = "../dtos-devops-templates/infrastructure/modules/subnet"

  name                                                           = "snet-container-apps"
  resource_group_name                                            = azurerm_resource_group.main.name
  vnet_name                                                      = module.main_vnet.name
  address_prefixes                                               = [cidrsubnet(var.vnet_address_space, 7, 0)]
  create_nsg                                                     = false
  location                                                       = "UK South"
  monitor_diagnostic_setting_network_security_group_enabled_logs = []
  log_analytics_workspace_id                                     = module.log_analytics_workspace_audit.id
  network_security_group_name                                    = "nsg-container-apps"
  delegation_name                                                = "delegation"
  service_delegation_name                                        = "Microsoft.App/environments"
  service_delegation_actions                                     = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
}

module "main_subnet" {
  source = "../dtos-devops-templates/infrastructure/modules/subnet"

  name                                                           = "snet-main"
  resource_group_name                                            = azurerm_resource_group.main.name
  vnet_name                                                      = module.main_vnet.name
  address_prefixes                                               = [cidrsubnet(var.vnet_address_space, 7, 2)]
  create_nsg                                                     = false
  location                                                       = "UK South"
  monitor_diagnostic_setting_network_security_group_enabled_logs = []
  log_analytics_workspace_id                                     = module.log_analytics_workspace_audit.id
  network_security_group_name                                    = "nsg-container-apps"
}

data "azurerm_private_dns_zone" "key-vault" {
  count = var.features.private_networking ? 1 : 0
  
  provider = azurerm.hub

  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = "rg-hub-${var.hub}-uks-private-dns-zones"
}

