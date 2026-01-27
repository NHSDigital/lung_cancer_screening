using '../../hub.bicep'

param hubType = 'nonlive'
param vnetAddressPrefixes = [
  '10.11.0.0/16'
]
param devopsSubnetAddressPrefix = '10.11.1.0/24'
param privateEndpointSubnetAddressPrefix = '10.11.2.0/24'
param enableSoftDelete = true
