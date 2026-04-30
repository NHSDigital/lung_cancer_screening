module "logic_app_slack_alert" {
  count = var.enable_alerting ? 1 : 0

  source = "../dtos-devops-templates/infrastructure/modules/logic-app-slack-alert"

  name                = "logic-${var.app_short_name}-${var.environment}-slack-alerts"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.region
  slack_webhook_url   = var.slack_webhook_url
}

resource "azurerm_monitor_action_group" "slack" {
  count = var.enable_alerting ? 1 : 0

  name                = "ag-slack-${var.app_short_name}-${var.environment}-uks"
  resource_group_name = azurerm_resource_group.main.name
  short_name          = "slack"

  webhook_receiver {
    name                    = "logic-app-slack"
    service_uri             = module.logic_app_slack_alert[0].trigger_callback_url
    use_common_alert_schema = true
  }
}
