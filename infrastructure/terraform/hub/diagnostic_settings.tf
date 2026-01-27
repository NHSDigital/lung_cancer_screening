locals {
  # APIM
  monitor_diagnostic_setting_apim_enabled_logs = ["GatewayLogs", "WebSocketConnectionLogs", "DeveloperPortalAuditLogs"]
  monitor_diagnostic_setting_apim_metrics      = ["AllMetrics"]

  # FRONTDOOR
  monitor_diagnostic_setting_frontdoor_enabled_logs = ["FrontDoorAccessLog", "FrontDoorHealthProbeLog", "FrontDoorWebApplicationFirewallLog"]
  monitor_diagnostic_setting_frontdoor_metrics      = ["AllMetrics"]

  # KEYVAULT
  monitor_diagnostic_setting_keyvault_enabled_logs = ["AuditEvent", "AzurePolicyEvaluationDetails"]
  monitor_diagnostic_setting_keyvault_metrics      = ["AllMetrics"]

  # LOG ANALYTICS WORKSPACE
  monitor_diagnostic_setting_log_analytics_workspace_enabled_logs = ["SummaryLogs", "Audit"]
  monitor_diagnostic_setting_log_analytics_workspace_metrics      = ["AllMetrics"]

  # STORAGE ACCOUNT
  monitor_diagnostic_setting_storage_account_enabled_logs = ["StorageWrite", "StorageRead", "StorageDelete"]
  monitor_diagnostic_setting_storage_account_metrics      = ["Capacity", "Transaction"]

  # SUBNET
  monitor_diagnostic_setting_network_security_group_enabled_logs = ["NetworkSecurityGroupEvent", "NetworkSecurityGroupRuleCounter"]

  # VNET
  monitor_diagnostic_setting_vnet_hub_enabled_logs = ["VMProtectionAlerts"]
  monitor_diagnostic_setting_vnet_hub_metrics      = ["AllMetrics"]
}
