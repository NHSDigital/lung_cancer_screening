data "azurerm_client_config" "current" {}

data "azuread_group" "postgres_sql_admin_group" {
  display_name = var.postgres_sql_admin_group
}

data "azurerm_private_dns_zone" "storage" {
  count = var.features.private_networking ? 1 : 0

  provider = azurerm.hub

  name                = "privatelink.blob.core.windows.net"
  resource_group_name = "rg-hub-${var.hub}-uks-private-dns-zones"
}

data "azurerm_private_dns_zone" "storage-account-blob" {
  count = var.features.private_networking ? 1 : 0

  provider = azurerm.hub

  name                = "privatelink.blob.core.windows.net"
  resource_group_name = "rg-hub-${var.hub}-uks-private-dns-zones"
}

data "azurerm_private_dns_zone" "storage-account-queue" {
  count = var.features.private_networking ? 1 : 0

  provider = azurerm.hub

  name                = "privatelink.queue.core.windows.net"
  resource_group_name = "rg-hub-${var.hub}-uks-private-dns-zones"
}
