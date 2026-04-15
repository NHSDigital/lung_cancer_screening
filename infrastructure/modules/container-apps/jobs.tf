locals {
  scheduled_jobs = {
    collect_metrics = {
      cron_expression = "*/5 * * * *"
      environment_variables = {
        ENVIRONMENT               = var.environment
      }
      job_short_name     = "clm"
      job_container_args = "collect_metrics"
    }
  }
}

module "db_setup" {
  source = "../dtos-devops-templates/infrastructure/modules/container-app-job"

  name                         = "${var.app_short_name}-dbm-${var.environment}"
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = azurerm_resource_group.main.name

  container_command = ["/bin/sh", "-c"]

  container_args = [
    "python manage.py migrate"
  ]
  secret_variables = var.deploy_database_as_container ? { DATABASE_PASSWORD = resource.random_password.admin_password[0].result } : {}
  docker_image     = var.docker_image
  user_assigned_identity_ids = flatten([
    [module.azure_blob_storage_identity.id],
    var.deploy_database_as_container ? [] : [module.db_connect_identity[0].id]
  ])
  environment_variables = merge(
    local.common_env,
    var.deploy_database_as_container ? local.container_db_env : local.azure_db_env
  )
  depends_on = [
    module.blob_storage_role_assignment
  ]

}

module "scheduled_jobs" {
  source = "../dtos-devops-templates/infrastructure/modules/container-app-job"

  for_each = local.scheduled_jobs

  name                         = "${var.app_short_name}-${each.value.job_short_name}-${var.environment}"
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = azurerm_resource_group.main.name

  fetch_secrets_from_app_key_vault = var.fetch_secrets_from_app_key_vault
  app_key_vault_id                 = var.app_key_vault_id

  container_command = ["/bin/sh", "-c"]
  container_args = [
    "python manage.py ${each.value.job_container_args}"
  ]

  docker_image        = var.docker_image
  replica_retry_limit = 0
  user_assigned_identity_ids = flatten([
    [module.azure_blob_storage_identity.id],
    var.deploy_database_as_container ? [] : [module.db_connect_identity[0].id]
  ])

  environment_variables = merge(
    local.common_env,
    {
      "STORAGE_ACCOUNT_NAME" = module.storage.storage_account_name,
      "BLOB_MI_CLIENT_ID"    = module.azure_blob_storage_identity.client_id,
    },
    each.value.environment_variables,
    var.deploy_database_as_container ? local.container_db_env : local.azure_db_env
  )
  secret_variables = merge(
    { APPLICATIONINSIGHTS_CONNECTION_STRING = var.app_insights_connection_string },
    var.deploy_database_as_container ? { DATABASE_PASSWORD = resource.random_password.admin_password[0].result } : {}
  )

  # alerts
  action_group_id            = var.action_group_id
  enable_alerting            = var.enable_alerting
  log_analytics_workspace_id = var.log_analytics_workspace_audit_id

  # Ensure RBAC role assignments are created before the job definition finalizes
  depends_on = [
    module.blob_storage_role_assignment,
  ]

  cron_expression = each.value.cron_expression
}
