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
      ALLOWED_HOSTS        = "${var.app_short_name}-web-${var.environment}.${var.default_domain}"
      CSRF_TRUSTED_ORIGINS = "https://${var.app_short_name}-web-${var.environment}.${var.default_domain}"
    },
    var.deploy_database_as_container ? local.container_db_env : local.azure_db_env
  )
  secret_variables = var.deploy_database_as_container ? { DATABASE_PASSWORD = resource.random_password.admin_password[0].result } : {}
  is_web_app       = true
  port             = 8000
}
