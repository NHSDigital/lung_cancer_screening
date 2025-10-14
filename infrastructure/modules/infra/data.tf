data "azuread_service_principal" "github-mi" {
  display_name = var.github_mi_name
}

data "azuread_group" "kv_officers" {
  for_each = toset(var.key_vault_secrets_officer_groups)

  display_name = each.value
}
