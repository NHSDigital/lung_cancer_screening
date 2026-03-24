module "monitor_action_group" {
  for_each = var.regions

  source = "../../../../dtos-devops-templates/infrastructure/modules/monitor-action-group"

  name                = "ag-${var.environment}-${each.key}-uks"
  resource_group_name = azurerm_resource_group.rg_hub[each.key].name
  location            = each.key
  short_name          = "ag-${each.key}"
  email_receiver = {
    email = {
      name          = "email"
      email_address = data.azurerm_key_vault_secret.infra.value
    }
  }
}
