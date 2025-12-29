param hub string
param region string
param privateDNSZoneID string
param name string
param resourceID string
param resourceServiceType string
param RGName string
param vnetName string
param privateEndpointSubnetName string
param virtualNetworkName string
param privateEndpointSubnetAddressPrefix string

//var RGName = 'rg-hub-${hub}-uks-hub-networking'
//var vnetName = 'VNET-${toUpper(hub)}-UKS-HUB'

var groupID = {
  storage: 'blob'
  keyVault: 'vault'
}

// Retrieve the existing vnet resource group
resource vnetRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: RGName
  scope: subscription()
}

// Retrieve the existing vnet
resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' existing = {
  name: vnetName
  scope: vnetRG
}

// Retrieve the existing Subnet within the vnet
// resource subnet 'Microsoft.Network/virtualNetworks/subnets@2024-01-01' = {
//   parent: vnet
//   name: subnetName
//   region: region
// }

resource privateEndpointSubnet 'Microsoft.Network/virtualNetworks/subnets@2025-01-01' = {
  name: '${virtualNetworkName}/${privateEndpointSubnetName}'
  properties: {
    addressPrefix: privateEndpointSubnetAddressPrefix
    privateEndpointNetworkPolicies: 'Disabled'
  }
}


// Create the private endpoint for the storage account
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2024-01-01' = {
  name: '${name}-pep'
  location: region
  properties: {
    subnet: {
      id: privateEndpointSubnet.id
    }
    privateLinkServiceConnections: [
      {
        name: '${name}-connection'
        properties: {
          privateLinkServiceId: resourceID
          groupIds: [
            groupID[resourceServiceType]
          ]
        }
      }
    ]
  }
}

// Register the private endpoint in the private DNS zone
resource dnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: privateEndpoint
  name: '${name}-dns'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: '${name}-dns-zone-config'
        properties: {
          privateDnsZoneId: privateDNSZoneID
        }
      }
    ]
  }
}
