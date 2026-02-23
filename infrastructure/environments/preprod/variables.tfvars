dns_zone_name                    = "digital-lung-cancer-screening.nhs.uk"
enable_entra_id_authentication   = false
fetch_secrets_from_app_key_vault = true
front_door_profile               = "afd-live-hub-lungcs"
features = {
  front_door         = true
  hub_and_spoke      = true
  private_networking = true
}
# when doing Dev we deploy using
github_mi_name                        = "mi-lungcs-preprod-adotoaz-uks"
key_vault_secrets_officer_groups      = ["screening_lungcs_preprod"]
postgres_backup_retention_days        = 7
postgres_geo_redundant_backup_enabled = false
protect_keyvault                      = true
vnet_address_space                    = "10.14.0.0/16"
seed_demo_data                        = true
