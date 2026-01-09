using '../../hub.bicep'

param hubType = 'nonlive'
param vnetAddressPrefixes = [
  '10.11.0.0/16'
]
param devopsSubnetAddressPrefix = '10.11.1.0/24'
param privateEndpointSubnetAddressPrefix = '10.11.2.0/24'
param enableSoftDelete = true
// param devopsInfrastructureId = ''
// param devopsInfrastructureId = '31687f79-5e43-4c1e-8c63-d9f4bff5cf8b'
//param devopsInfrastructureId = '602aafe8-ce26-40ef-8729-ebd1ffdb094b'
