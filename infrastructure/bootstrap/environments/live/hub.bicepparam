using '../../hub.bicep'

param hubType = 'live'
param vnetAddressPrefixes = [
  '10.21.0.0/16'
]
param devopsSubnetAddressPrefix = '10.21.1.0/24'
param devopsInfrastructureId = ''
