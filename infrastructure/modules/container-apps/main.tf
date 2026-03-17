resource "azurerm_resource_group" "main" {
  name     = local.resource_group_name
  location = var.region
}

module "webapp" {
  source = "../dtos-devops-templates/infrastructure/modules/container-app"

  providers = {
    azurerm     = azurerm
    azurerm.hub = azurerm.hub
  }

  name                             = "${var.app_short_name}-web-${var.environment}"
  container_app_environment_id     = var.container_app_environment_id

  # alerts
  action_group_id        = var.action_group_id
  enable_alerting        = var.enable_alerting
  alert_memory_threshold = 80
  alert_cpu_threshold    = 90

  resource_group_name              = azurerm_resource_group.main.name
  fetch_secrets_from_app_key_vault = var.fetch_secrets_from_app_key_vault
  infra_key_vault_name             = "kv-${var.app_short_name}-${var.env_config}-inf"
  infra_key_vault_rg               = "rg-${var.app_short_name}-${var.env_config}-infra"
  enable_entra_id_authentication   = var.enable_entra_id_authentication
  app_key_vault_id                 = var.app_key_vault_id
  docker_image                     = var.docker_image
  user_assigned_identity_ids       = var.deploy_database_as_container ? [] : [module.db_connect_identity[0].id]
  environment_variables = merge(
    local.common_env,
    {
      ALLOWED_HOSTS        = "${local.hostname}",
      CSRF_TRUSTED_ORIGINS = "https://${local.hostname}"
    },
    var.deploy_database_as_container ? local.container_db_env : local.azure_db_env
  )
  secret_variables = var.deploy_database_as_container ? { DATABASE_PASSWORD = resource.random_password.admin_password[0].result } : {}
  is_web_app       = true
  port             = 8000
  probe_path       = "/healthcheck"
  min_replicas     = var.min_replicas
  memory           = var.container_memory
}

module "azurerm_application_insights_standard_web_test" {
  count = var.enable_alerting ? 1 : 0

  source                  = "../dtos-devops-templates/infrastructure/modules/application-insights-availability-test"
  name                    = "${var.app_short_name}-web-${var.environment}"
  resource_group_name     = var.resource_group_name_infra
  location                = var.region
  action_group_id         = var.action_group_id
  application_insights_id = var.app_insights_id
  target_url              = var.features.front_door ? "${local.external_url}healthcheck" : null
}
