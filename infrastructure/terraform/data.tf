# Only do these looks ups if we have already deployed the infra code in a previous run, else don't use it
data "azurerm_container_app_environment" "this" {
  count = var.deploy_infra ? 0 : 1

  name                = "cae-${var.environment}-uks-${var.app_short_name}"
  resource_group_name = local.resource_group_name
}

data "azurerm_key_vault" "app_key_vault" {
  count = var.deploy_infra ? 0 : 1

  name                = "kv-${var.app_short_name}-${var.env_config}-app"
  resource_group_name = local.resource_group_name
}

data "azurerm_log_analytics_workspace" "audit" {
  count = var.deploy_infra ? 0 : 1

  name                = "law-${var.environment}-uks-${var.app_short_name}"
  resource_group_name = local.resource_group_name
}

data "azurerm_subnet" "postgres" {
  count = var.deploy_infra ? 0 : 1

  name                 = "snet-postgres"
  virtual_network_name = "vnet-${var.environment}-uks-${var.app_short_name}"
  resource_group_name  = local.resource_group_name
}

data "azurerm_subnet" "main" {
  count = var.deploy_infra ? 0 : 1

  name                 = "snet-main"
  virtual_network_name = "vnet-${var.environment}-uks-${var.app_short_name}"
  resource_group_name  = local.resource_group_name
}
