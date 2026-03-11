data "azuread_service_principal" "github-mi" {
  display_name = var.github_mi_name
}

data "azuread_group" "kv_officers" {
  for_each = toset(var.key_vault_secrets_officer_groups)

  display_name = each.value
}

data "azurerm_key_vault_secret" "infra" {
  name         = "monitoring-email-address"
  key_vault_id = data.azurerm_key_vault.infra.id
}
