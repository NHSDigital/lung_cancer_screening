locals {
  deploy_blue_avd = (
    var.virtual_desktop_group_active == "blue" || var.virtual_desktop_group_active == "both-with-blue-primary" || var.virtual_desktop_group_active == "both-with-green-primary" || var.virtual_desktop_group_active == "both-with-blue-primary-but-equal-vms" || var.virtual_desktop_group_active == "both-with-green-primary-but-equal-vms"
  )

  deploy_green_avd = (
    var.virtual_desktop_group_active == "green" || var.virtual_desktop_group_active == "both-with-blue-primary" || var.virtual_desktop_group_active == "both-with-green-primary" || var.virtual_desktop_group_active == "both-with-blue-primary-but-equal-vms" || var.virtual_desktop_group_active == "both-with-green-primary-but-equal-vms"
  )

  green_avd_primary = (
    var.virtual_desktop_group_active == "green" || var.virtual_desktop_group_active == "both-with-green-primary" || var.virtual_desktop_group_active == "both-with-green-primary-but-equal-vms"
  )

  blue_avd_primary = (
    var.virtual_desktop_group_active == "blue" || var.virtual_desktop_group_active == "both-with-blue-primary" || var.virtual_desktop_group_active == "both-with-blue-primary-but-equal-vms"
  )

  equal_vm_counts = (
    var.virtual_desktop_group_active == "both-with-blue-primary-but-equal-vms" || var.virtual_desktop_group_active == "both-with-green-primary-but-equal-vms"
  )
}

# Once issues with the Data Reader is resolved this will be re-added.
# data "azuread_service_principal" "avd" {
#   application_id = local.principal_id
# }

resource "azurerm_resource_group" "avd_blue" {
  for_each = var.regions

  name     = "${module.config[each.key].names.resource-group}-${var.application}-virtual-desktop-blue"
  location = each.key
}

resource "azurerm_role_assignment" "avd_autoscale_blue_hostpool" {
  for_each = local.deploy_blue_avd ? var.regions : {}

  scope                = azurerm_resource_group.avd_blue[each.key].id
  role_definition_name = "Desktop Virtualization Host Pool Contributor"

  principal_id   = var.AVD_APPLICATION_ID
  principal_type = "ServicePrincipal"
}


module "virtual-desktop-blue" {
  for_each = (local.deploy_blue_avd ? var.regions : {})

  source = "../../../../dtos-devops-templates/infrastructure/modules/virtual-desktop"

  custom_rdp_properties = "drivestoredirect:s:*;audiomode:i:0;videoplaybackmode:i:1;redirectclipboard:i:1;redirectprinters:i:1;devicestoredirect:s:*;redirectcomports:i:1;redirectsmartcards:i:1;usbdevicestoredirect:s:*;enablecredsspsupport:i:1;redirectwebauthn:i:1;use multimon:i:1;enablerdsaadauth:i:1;"
  computer_name_prefix  = "lun${var.env_type}"
  dag_name              = module.config[each.key].names.avd-dag
  host_pool_name        = module.config[each.key].names.avd-host-pool
  location              = each.key

  entra_users_group_id = var.ENTRA_USERS_GROUP_ID
  entra_admins_group_id = var.ENTRA_ADMINS_GROUP_ID

  maximum_sessions_allowed  = var.avd_maximum_sessions_allowed
  resource_group_name       = azurerm_resource_group.avd_blue[each.key].name
  resource_group_id         = azurerm_resource_group.avd_blue[each.key].id
  scaling_plan_name         = module.config[each.key].names.avd-scaling-plan

  source_image_id           = var.AVD_SOURCE_IMAGE_ID
  # left as example of source image reference Example 1
  # source_image_reference = {
  #   publisher = "MicrosoftWindowsDesktop"
  #   offer     = "windows-11"
  #   sku       = "win11-23h2-avd"
  #   version   = "latest"
  # }

  # left as example of source image reference Example 2
  # source_image_reference    = var.avd_source_image_reference
  # source_image_from_gallery = var.avd_source_image_from_gallery

  subnet_id                 = module.subnets_hub["${module.config[each.key].names.subnet}-virtual-desktop"].id
  vm_count                  = local.blue_avd_primary || local.equal_vm_counts ? var.avd_vm_count : 1
  vm_name_prefix            = module.config[each.key].names.avd-host
  vm_storage_account_type   = "StandardSSD_LRS"
  vm_size                   = var.avd_vm_size
  vm_license_type           = "Windows_Client"
  workspace_name            = "lungcs-${each.key}"

  principal_id              = var.AVD_OBJECT_ID

  tags = var.tags

}

resource "azurerm_resource_group" "avd_green" {
  for_each = var.regions

  name     = "${module.config[each.key].names.resource-group}-${var.application}-virtual-desktop-green"
  location = each.key
}


# Green AVD deployment
module "virtual-desktop-green" {
  for_each = (local.deploy_green_avd ? var.regions : {})

  source = "../../../../dtos-devops-templates/infrastructure/modules/virtual-desktop"

  custom_rdp_properties = "drivestoredirect:s:*;audiomode:i:0;videoplaybackmode:i:1;redirectclipboard:i:1;redirectprinters:i:1;devicestoredirect:s:*;redirectcomports:i:1;redirectsmartcards:i:1;usbdevicestoredirect:s:*;enablecredsspsupport:i:1;redirectwebauthn:i:1;use multimon:i:1;enablerdsaadauth:i:1;"
  computer_name_prefix  = "lun${var.env_type}"
  dag_name              = module.config[each.key].names.avd-dag
  host_pool_name        = "${module.config[each.key].names.avd-host-pool}-v2"
  location              = each.key
  entra_users_group_id  = var.ENTRA_USERS_GROUP_ID
  entra_admins_group_id = var.ENTRA_ADMINS_GROUP_ID
  maximum_sessions_allowed  = var.avd_maximum_sessions_allowed
  resource_group_name       = azurerm_resource_group.avd_green[each.key].name
  resource_group_id         = azurerm_resource_group.avd_green[each.key].id
  scaling_plan_name         = module.config[each.key].names.avd-scaling-plan
  source_image_id           = null
  source_image_reference    = null
  source_image_from_gallery = var.avd_source_image_from_gallery
  subnet_id                 = module.subnets_hub["${module.config[each.key].names.subnet}-virtual-desktop"].id
  vm_count                  = local.green_avd_primary || local.equal_vm_counts ? var.avd_vm_count : 1
  vm_name_prefix            = module.config[each.key].names.avd-host
  vm_storage_account_type   = "StandardSSD_LRS"
  vm_size                   = var.avd_vm_size
  vm_license_type           = "Windows_Client"
  workspace_name            = "lungcs-${each.key}"

  principal_id              = var.AVD_OBJECT_ID
  tags = var.tags

}

module "route-table-virtual-desktop" {
  for_each = var.regions

  source = "../../../../dtos-devops-templates/infrastructure/modules/route-table"

  name                = "${module.config[each.key].names.route-table}-virtual-desktop"
  resource_group_name = azurerm_resource_group.rg_hub[each.key].name
  location            = each.key

  bgp_route_propagation_enabled = false

  routes = [
    {
      name           = "AVDSessionHostControl"
      address_prefix = "WindowsVirtualDesktop"
      next_hop_type  = "Internet"
    },
    {
      name           = "EntraAuthTraffic"
      address_prefix = "AzureActiveDirectory"
      next_hop_type  = "Internet"
    },
    {
      name                   = "EgressViaFirewall"
      address_prefix         = "0.0.0.0/0"
      next_hop_type          = "VirtualAppliance"
      next_hop_in_ip_address = module.firewall[each.key].private_ip_address
    }
  ]

  subnet_ids = [module.subnets_hub["${module.config[each.key].names.subnet}-virtual-desktop"].id]

  tags = var.tags
}
