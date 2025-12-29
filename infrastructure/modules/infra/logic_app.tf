module "logic_app_slack_alert" {
  # TODO: Add this back in before merging into main
  # count  = var.enable_alerting ? 1 : 0
  source = "../dtos-devops-templates/infrastructure/modules/logic-app-slack-alert"

  name                = "logic-${var.app_short_name}-${var.environment}-slack-alerts"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.region
  slack_webhook_url   = data.azurerm_key_vault_secret.slack_webhook_url.value
}

resource "azurerm_monitor_action_group" "slack" {
  name                = "ag-slack-myapp-dev-uks"
  resource_group_name = azurerm_resource_group.main.name
  short_name          = "slack"

  webhook_receiver {
    name                    = "logic-app-slack"
    service_uri             = module.logic_app_slack_alert.trigger_callback_url
    use_common_alert_schema = true
  }
}
