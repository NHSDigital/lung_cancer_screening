targetScope = 'resourceGroup'

param resourceServiceType string
param vnetId string

// location inside the resource — it just needs to exist so ARM can stamp it onto the nested deployment.
param location string = 'uksouth'

var dnsZoneName = {
  storage: 'privatelink.blob.${environment().suffixes.storage}'
  // Cannot read vault URL from environment() because of https://github.com/Azure/bicep/issues/9839
  keyVault: 'privatelink.vaultcore.azure.net'
}

// Retrieve the private DNS zone for storage accounts
resource privateDNSZone 'Microsoft.Network/privateDnsZones@2024-06-01' = {
  name: dnsZoneName[resourceServiceType]
  location: 'global'
}

resource vnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = {
  name: '${last(split(vnetId, '/'))}-link'
  parent: privateDNSZone
  location: 'global'
  properties: {
    virtualNetwork: {
      id: vnetId
    }
    registrationEnabled: false
  }
}

output privateDNSZoneID string = privateDNSZone.id
