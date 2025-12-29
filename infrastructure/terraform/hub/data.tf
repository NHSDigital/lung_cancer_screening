data "azurerm_client_config" "current" {}

data "azuread_group" "avd_users" {
  display_name = var.avd_users_group_name
}

# Awaiting permission to read group membership via Microsoft Graph API
data "azuread_group" "avd_admins" {
  display_name = var.avd_admins_group_name
}

# This client id is the same for all Azure customers - it is not a secret.
# https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/app_service_certificate
# data "azuread_service_principal" "MicrosoftAzureAppService" {
#   client_id = "abfa0a7c-a6b6-4736-8310-5855508787cd"
# }

# data "azuread_service_principal" "MicrosoftAzureFrontDoorCdn" {
#   client_id = "205478c0-bd83-4e1b-a9d6-db63a3e1e1c8"
# }
