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
    [module.azure_queue_storage_identity.id],
    var.deploy_database_as_container ? [] : [module.db_connect_identity[0].id]
  ])
  environment_variables = merge(
    local.common_env,
    var.deploy_database_as_container ? local.container_db_env : local.azure_db_env
  )
  depends_on = [
    module.queue_storage_role_assignment,
    module.blob_storage_role_assignment
  ]

}

module "flush_database" {
  source = "../dtos-devops-templates/infrastructure/modules/container-app-job"
  # We need to be able to flush the db on a daily basis in POC to ensure
  # We can test the service in a clean state. DO NOT ADD THIS TO OTHER ENVIRONMENTS.
  count = var.environment == "poc" ? 1 : 0

  name                         = "${var.app_short_name}-flush-db-${var.environment}"
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = azurerm_resource_group.main.name

  container_command = ["/bin/sh", "-c"]

  container_args = [
    "python manage.py flush"
  ]
  cron_expression  = "0 6 * * *" # Run at 6am every day
  secret_variables = var.deploy_database_as_container ? { DATABASE_PASSWORD = resource.random_password.admin_password[0].result } : {}
  docker_image     = var.docker_image
  user_assigned_identity_ids = flatten([
    [module.azure_blob_storage_identity.id],
    [module.azure_queue_storage_identity.id],
    var.deploy_database_as_container ? [] : [module.db_connect_identity[0].id]
  ])
  environment_variables = merge(
    local.common_env,
    var.deploy_database_as_container ? local.container_db_env : local.azure_db_env
  )
  depends_on = [
    module.queue_storage_role_assignment,
    module.blob_storage_role_assignment
  ]

}
