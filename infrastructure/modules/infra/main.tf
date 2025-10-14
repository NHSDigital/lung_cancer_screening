locals {
  key_vault_secrets_officers = toset([
    "mi-lungcs-poc-ghtoaz-uks",
    "Azure-Lung-Cancer-Screening---Dev-Owner"
  ])
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.region
}

module "app-key-vault" {
  source = "../dtos-devops-templates/infrastructure/modules/key-vault"

  name                                             = "kv-${var.app_short_name}-${var.environment}-app"
  resource_group_name                              = azurerm_resource_group.main.name
  enable_rbac_authorization                        = true
  location                                         = var.region
  log_analytics_workspace_id                       = module.log_analytics_workspace_audit.id
  monitor_diagnostic_setting_keyvault_enabled_logs = ["AuditEvent", "AzurePolicyEvaluationDetails"]
  monitor_diagnostic_setting_keyvault_metrics      = ["AllMetrics"]
  private_endpoint_properties = var.features.private_networking ? {
    private_dns_zone_ids_keyvault        = [data.azurerm_private_dns_zone.key-vault[0].id]
    private_endpoint_enabled             = true
    private_endpoint_subnet_id           = module.main_subnet.id
    private_endpoint_resource_group_name = azurerm_resource_group.main.name
    private_service_connection_is_manual = false
  } : null
  public_network_access_enabled = !var.features.private_networking
  purge_protection_enabled      = var.protect_keyvault
}

data "azuread_service_principal" "identity" {
  for_each = local.key_vault_secrets_officers

  display_name = each.value
}

module "key_vault_rbac_assignments" {
  for_each = data.azuread_service_principal.identity

  source = "../dtos-devops-templates/infrastructure/modules/rbac-assignment"

  principal_id         = each.value.object_id
  role_definition_name = "Key Vault Secrets Officer"
  scope                = module.app-key-vault.key_vault_id
}

module "log_analytics_workspace_audit" {
  source = "../dtos-devops-templates/infrastructure/modules/log-analytics-workspace"

  name     = "law-${var.environment}-uks-${var.app_short_name}"
  location = var.region

  law_sku        = "PerGB2018"
  retention_days = 30

  monitor_diagnostic_setting_log_analytics_workspace_enabled_logs = ["SummaryLogs", "Audit"]
  monitor_diagnostic_setting_log_analytics_workspace_metrics      = ["AllMetrics"]

  resource_group_name = azurerm_resource_group.main.name
}

module "container-app-environment" {
  source = "../dtos-devops-templates/infrastructure/modules/container-app-environment"

  providers = {
    azurerm     = azurerm
    azurerm.dns = azurerm.hub
  }

  name                           = "cae-${var.environment}-uks-${var.app_short_name}"
  resource_group_name            = azurerm_resource_group.main.name
  internal_load_balancer_enabled = var.features.private_networking
  log_analytics_workspace_id     = module.log_analytics_workspace_audit.id
  vnet_integration_subnet_id     = module.container_app_subnet.id
  private_dns_zone_rg_name       = var.features.private_networking ? "rg-hub-${var.hub}-uks-private-dns-zones" : null
}
