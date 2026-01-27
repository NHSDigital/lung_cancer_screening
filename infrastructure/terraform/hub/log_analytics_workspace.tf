module "log_analytics_workspace_hub" {
  for_each = var.regions

  source = "../../../../dtos-devops-templates/infrastructure/modules/log-analytics-workspace"

  name                = module.config[each.key].names.log-analytics-workspace
  resource_group_name = azurerm_resource_group.rg_base[each.key].name
  location            = each.key

  law_sku        = var.law.law_sku
  retention_days = var.law.retention_days

  monitor_diagnostic_setting_log_analytics_workspace_enabled_logs = local.monitor_diagnostic_setting_log_analytics_workspace_enabled_logs
  monitor_diagnostic_setting_log_analytics_workspace_metrics      = local.monitor_diagnostic_setting_log_analytics_workspace_metrics

  tags = var.tags
}
