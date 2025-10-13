deploy_database_as_container = false
features = {
  front_door         = false
  hub_and_spoke      = false
  private_networking = false
}
postgres_backup_retention_days        = 7
postgres_geo_redundant_backup_enabled = false
fetch_secrets_from_app_key_vault      = true
protect_keyvault                      = false
vnet_address_space                    = "10.65.0.0/16"
