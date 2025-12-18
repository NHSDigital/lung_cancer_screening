/*
  Root Bicep file for deploying Hub subscription bootstrap resources needed for Terraform to continue:
    - Private VNet
    - Managed DevOps Pool (for VNet-integrated ADO build agents)
    - Managed Identity for Terraform
    - Blob Storage Account with Container, Private Endpoint, and public access disabled
    - Private DNS for Storage Account Private Endpoint

  Subscription pre-requisites:
    - az provider register --namespace 'Microsoft.DevOpsInfrastructure'
    - az provider register --namespace 'Microsoft.DevCenter'

  Run once, deployment of the Managed DevOps Pool will fail.
  Manually Grant 'Reader' and 'Network Contributor' RBAC roles to the Service Principal 'DevopsInfrastructure' on the VNet resource.
  Re-run, it will succeed. This cannot be automated in Bicep, the object ID (which needs to be resolved from the appId) will be considered invalid, even though it's fine using az cli.
*/

targetScope = 'subscription'

param devopsSubnetAddressPrefix string
// param enableSoftDelete bool
param hubType string // live / nonlive
param region string = 'uksouth'
param regionShortName string = 'uks'
param vnetAddressPrefixes array

// var keyVaultName = 'kv-lungcs-${envConfig}-inf'

var devopsSubnetName = 'sn-hub-${hubType}-${regionShortName}-devops'
var devCenterName = 'devc-hub-${hubType}-${regionShortName}'
var devCenterProjectName = 'prj-hub-${hubType}-${regionShortName}'
var poolName = 'private-pool-hub-${hubType}-${regionShortName}'
var resourceGroupName = 'rg-hub-${hubType}-${regionShortName}-bootstrap'
var virtualNetworkName = 'vnet-hub-${hubType}-${regionShortName}'

// var miADOtoAZname = 'mi-${appShortName}-${envConfig}-adotoaz-uks'
// var miGHtoADOname = 'mi-${appShortName}-${envConfig}-ghtoado-uks'

resource bootstrapRG 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: resourceGroupName
  location: region
}

@description('Virtual Network Deployment')
module virtualNetwork 'modules/virtualNetwork.bicep' = {
  scope: bootstrapRG
  params: {
    name: virtualNetworkName
    addressPrefixes: vnetAddressPrefixes
  }
}

@description('Managed DevOps Pool Deployment')
module managedDevopsPool 'modules/managedDevopsPool.bicep' = {
  scope: bootstrapRG
  params: {
    adoOrg: 'nhse-pps-1'
    agentProfileMaxAgentLifetime: '00.04:00:00'
    devCenterName: devCenterName
    devCenterProjectName: devCenterProjectName
    devopsSubnetName: devopsSubnetName
    devopsSubnetAddressPrefix: devopsSubnetAddressPrefix
    poolName: poolName
    virtualNetworkName: virtualNetwork.outputs.name
  }
}
