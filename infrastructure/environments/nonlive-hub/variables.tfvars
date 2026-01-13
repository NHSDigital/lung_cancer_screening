application = "hub"
environment = "nonlive-hub"
env_type    = "nonlive"

features = {
  private_endpoints_enabled              = true
  private_service_connection_is_manual   = false
  public_network_access_enabled          = true
  log_analytics_data_export_rule_enabled = false
}

virtual_desktop_group_active = "green"

projects = {
  lung-cancer-screening = {
    full_name  = "Lung Cancer Screening"
    short_name = "lungcs"
    tags = {
      Project = "Lung Cancer Screening"
    }
    frontdoor_profile = {
      sku_name = "Premium_AzureFrontDoor"
    }
  }
}

diagnostic_settings = {
  metric_enabled = true
}

private_dns_zones = {
  is_app_services_enabled                    = true
  is_azure_sql_private_dns_zone_enabled      = true
  is_postgres_sql_private_dns_zone_enabled   = true
  is_storage_private_dns_zone_enabled        = true
  is_acr_private_dns_zone_enabled            = false
  is_app_insights_private_dns_zone_enabled   = true
  is_apim_private_dns_zone_enabled           = false
  is_key_vault_private_dns_zone_enabled      = true
  is_event_hub_private_dns_zone_enabled      = false
  is_event_grid_enabled_dns_zone_enabled     = false
  is_container_apps_enabled_dns_zone_enabled = true
}


avd_vm_count                 = 1
avd_maximum_sessions_allowed = 1 # per session host
avd_vm_size                  = "Standard_D4as_v5"
avd_users_group_name         = "DToS-hub-dev-uks-hub-virtual-desktop-User-Login"
avd_admins_group_name        = "DToS-hub-dev-uks-hub-virtual-desktop-User-ADMIN-Login"

avd_source_image_from_gallery = {
  image_name      = "gi_wvd"
  gallery_name    = "rg_hub_dev_uks_compute_gallery"
  gallery_rg_name = "rg-hub-dev-uks-hub-virtual-desktop"
}

law = {
  export_enabled = false
  law_sku        = "PerGB2018"
  retention_days = 30
}

regions = {
  uksouth = {
    address_space     = "10.65.0.0/16"
    is_primary_region = true
    subnets = {
      pep = {
        cidr_newbits = 8
        cidr_offset  = 2
      }
      virtual-desktop = {
        cidr_newbits = 11
        cidr_offset  = 32
      }
      dns-resolver-in = {
        cidr_newbits               = 12
        cidr_offset                = 112
        delegation_name            = "Microsoft.Network/dnsResolvers"
        service_delegation_name    = "Microsoft.Network/dnsResolvers"
        service_delegation_actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
      }
      firewall = {
        name         = "AzureFirewallSubnet"
        cidr_newbits = 10
        cidr_offset  = 192
        create_nsg   = false
      }
    }
  }
    ukwest = {
    address_space     = "10.65.0.0/16"
    is_primary_region = true
    subnets = {
      pep = {
        cidr_newbits = 8
        cidr_offset  = 2
      }
      virtual-desktop = {
        cidr_newbits = 11
        cidr_offset  = 32
      }
      dns-resolver-in = {
        cidr_newbits               = 12
        cidr_offset                = 112
        delegation_name            = "Microsoft.Network/dnsResolvers"
        service_delegation_name    = "Microsoft.Network/dnsResolvers"
        service_delegation_actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
      }
      firewall = {
        name         = "AzureFirewallSubnet"
        cidr_newbits = 10
        cidr_offset  = 192
        create_nsg   = false
      }
    }
  }
}
