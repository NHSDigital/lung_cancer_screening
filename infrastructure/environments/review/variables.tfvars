dns_zone_name                    = "non-live.digital-lung-cancer-screening.nhs.uk"
enable_entra_id_authentication   = false
fetch_secrets_from_app_key_vault = true
front_door_profile               = "afd-nonlive-hub-lungcs"
features = {
  front_door         = true
  hub_and_spoke      = true
  private_networking = true
}
# when doing Dev we deploy using
github_mi_name                        = "mi-lungcs-review-adotoaz-uks"
key_vault_secrets_officer_groups      = ["screening_lungcs_review"]
postgres_backup_retention_days        = 7
postgres_geo_redundant_backup_enabled = false
protect_keyvault                      = false
vnet_address_space                    = "10.13.0.0/16"
seed_demo_data                        = true
deploy_database_as_container          = true
