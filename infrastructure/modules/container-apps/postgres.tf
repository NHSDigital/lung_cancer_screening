data "azurerm_private_dns_zone" "postgres" {
  count = var.features.private_networking ? 1 : 0

  provider = azurerm.hub

  name                = "privatelink.postgres.database.azure.com"
  resource_group_name = "rg-hub-${var.hub}-uks-private-dns-zones"
}

# Don't deploy if deploy_database_as_container is true
module "postgres" {
  count = var.deploy_database_as_container ? 0 : 1

  source = "../dtos-devops-templates/infrastructure/modules/postgresql-flexible"

  # postgresql Server
  name                = "postgres-${var.app_short_name}-${var.environment}-uks"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.region

  backup_retention_days           = var.postgres_backup_retention_days
  geo_redundant_backup_enabled    = var.postgres_geo_redundant_backup_enabled
  postgresql_admin_object_id      = "" #data.azuread_group.postgres_sql_admin_group.object_id
  postgresql_admin_principal_name = var.postgres_sql_admin_group
  postgresql_admin_principal_type = "Group"
  administrator_login             = local.database_user
  admin_identities                = [module.db_connect_identity[0]]

  # Diagnostic Settings
  log_analytics_workspace_id                                = var.log_analytics_workspace_audit_id
  monitor_diagnostic_setting_postgresql_server_enabled_logs = ["PostgreSQLLogs", "PostgreSQLFlexSessions", "PostgreSQLFlexQueryStoreRuntime", "PostgreSQLFlexQueryStoreWaitStats", "PostgreSQLFlexTableStats", "PostgreSQLFlexDatabaseXacts"]
  monitor_diagnostic_setting_postgresql_server_metrics      = ["AllMetrics"]

  sku_name     = var.postgres_sku_name
  storage_mb   = var.postgres_storage_mb
  storage_tier = var.postgres_storage_tier

  server_version = "16"
  tenant_id      = data.azurerm_client_config.current.tenant_id

  private_endpoint_properties = var.features.private_networking ? {
    private_dns_zone_ids_postgresql      = [data.azurerm_private_dns_zone.postgres[0].id]
    private_endpoint_enabled             = true
    private_endpoint_subnet_id           = var.postgres_subnet_id
    private_endpoint_resource_group_name = azurerm_resource_group.main.name
    private_service_connection_is_manual = false
  } : null

  databases = {
    db1 = {
      collation   = "en_US.utf8"
      charset     = "UTF8"
      max_size_gb = 10
      name        = local.database_name
    }
  }

  tags = {}
}

module "db_connect_identity" {
  count = var.deploy_database_as_container ? 0 : 1

  source              = "../dtos-devops-templates/infrastructure/modules/managed-identity"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.region
  uai_name            = "mi-${var.app_short_name}-${var.environment}-db-connect"
}

resource "random_password" "admin_password" {
  count = var.deploy_database_as_container ? 1 : 0

  length           = 30
  special          = true
  override_special = "!@#$%^&*()-_=+"
}

module "database_container" {
  count = var.deploy_database_as_container ? 1 : 0

  providers = {
    azurerm     = azurerm
    azurerm.hub = azurerm.hub
  }

  source                       = "../dtos-devops-templates/infrastructure/modules/container-app"
  name                         = "${var.app_short_name}-db-${var.environment}"
  container_app_environment_id = var.container_app_environment_id
  docker_image                 = "postgres:16"
  secret_variables             = var.deploy_database_as_container ? { POSTGRES_PASSWORD = resource.random_password.admin_password[0].result } : {}
  environment_variables = {
    POSTGRES_USER = local.database_user
    POSTGRES_DB   = local.database_name
  }
  resource_group_name = azurerm_resource_group.main.name
  is_tcp_app          = true
  # postgres has a port of 5432
  port         = 5432
  exposed_port = local.database_port
}
