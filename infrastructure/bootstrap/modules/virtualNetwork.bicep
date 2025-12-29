param location string = 'uksouth'
param name string
param addressPrefixes array


resource virtualNetwork 'Microsoft.Network/virtualNetworks@2025-01-01' = {
  name: name
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: addressPrefixes
    }
  }
}

output name string = virtualNetwork.name
output id string = virtualNetwork.id
