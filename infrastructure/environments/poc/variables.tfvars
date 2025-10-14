deploy_database_as_container = false
features = {
  front_door         = false
  hub_and_spoke      = false
  private_networking = false
}
fetch_secrets_from_app_key_vault      = true
github_mi_name                        = "mi-lungcs-poc-ghtoaz-uks"
key_vault_secrets_officer_groups      = ["Azure-Lung-Cancer-Screening---Dev-Owner"]
postgres_backup_retention_days        = 7
postgres_geo_redundant_backup_enabled = false
protect_keyvault                      = false
vnet_address_space                    = "10.65.0.0/16"
