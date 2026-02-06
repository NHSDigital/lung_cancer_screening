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
param privateEndpointSubnetAddressPrefix string
param hubType string // live / nonlive
param region string = 'uksouth'
param regionShortName string = 'uks'
param vnetAddressPrefixes array
param enableSoftDelete bool


// removed when generalised
var appShortName = 'lungcs'

var devCenterSuffix = substring(uniqueString(subscription().id), 0, 3)
var devCenterName = 'devc-hub-${hubType}-${regionShortName}-${devCenterSuffix}'
var devopsSubnetName = 'sn-hub-${hubType}-${regionShortName}-devops'
var devCenterProjectName = 'prj-hub-${hubType}-${regionShortName}'
var poolName = 'private-pool-hub-${hubType}-${regionShortName}'
var resourceGroupName = 'rg-hub-${hubType}-${regionShortName}-bootstrap'
var virtualNetworkName = 'vnet-hub-${hubType}-${regionShortName}'
var managedIdentityRGName = 'rg-mi-${hubType}-${regionShortName}'
var miHub = 'mi-hub-${hubType}-${regionShortName}'
var privateDNSZoneRGName = 'rg-hub-${hubType}-${regionShortName}-private-dns-zones'
var keyVaultName = 'kv-${appShortName}-${hubType}-inf'
var privateEndpointSubnetName = 'sn-hub-${hubType}-${regionShortName}-private-endpoint'
var storageAccountName = 'sa${appShortName}${regionShortName}state'
var computeGalleryName = '${appShortName}_hub_compute_gallery'

var miADOtoAZname = 'mi-${appShortName}-${hubType}-adotoaz-${regionShortName}'
var miGHtoADOname = 'mi-${appShortName}-${hubType}-ghtoado-${regionShortName}'


// See: https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
var roleID = {
  CDNContributor: 'ec156ff8-a8d1-4d15-830c-5b80698ca432'
  kvSecretsUser: '4633458b-17de-408a-b874-0445c86b69e6'
  networkContributor: '4d97b98b-1d4f-4787-a291-c67834d212e7'
  rbacAdmin: 'f58310d9-a9f6-439a-9e8d-f62e7b41a168'
  reader: 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
  contributor: 'b24988ac-6180-42a0-ab88-20f7382dd24c'
  storageBlobDataContributor: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
}


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
    adoOrg: 'nhse-dtos'
    agentProfileMaxAgentLifetime: '00.04:00:00'
    devCenterName: devCenterName
    devCenterProjectName: devCenterProjectName
    devopsSubnetName: devopsSubnetName
    devopsSubnetAddressPrefix: devopsSubnetAddressPrefix
    poolName: poolName
    virtualNetworkName: virtualNetwork.outputs.name
  }
}

@description('Retrieve existing managed identity resource group')
resource managedIdentityRG 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: managedIdentityRGName
  location: region
}

@description('Retrieve existing private DNS zone resource group')
resource privateDNSZoneRG 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: privateDNSZoneRGName
  location: region
}

@description('Create the managed identity assumed by Azure devops to connect to Azure')
module managedIdentiyHub 'modules/managedIdentity.bicep' = {
  scope: managedIdentityRG
  params: {
    name: miHub
    region: region
  }
}

@description('Storage Deployment')
module terraformStateStorageAccount 'modules/storage.bicep' = {
  scope: bootstrapRG
  params: {
    storageLocation: region
    storageName: storageAccountName
    enableSoftDelete: true
    miPrincipalID: managedIdentiyHub.outputs.miPrincipalID
    miName: miHub
  }
}

@description('Create private endpoint and register DNS')
module storageAccountPrivateEndpoint 'modules/privateEndpoint.bicep' = {
  scope: bootstrapRG
  params: {
    hub: hubType
    region: region
    name: storageAccountName
    vnetName: virtualNetwork.outputs.name
    virtualNetworkName: virtualNetwork.outputs.name
    privateEndpointSubnetName: privateEndpointSubnetName
    privateEndpointSubnetAddressPrefix: privateEndpointSubnetAddressPrefix
    RGName: bootstrapRG.name
    resourceServiceType: 'storage'
    resourceID: terraformStateStorageAccount.outputs.storageAccountID
    privateDNSZoneID: storagePrivateDNSZone.outputs.privateDNSZoneID
  }
}

@description('Retrieve storage private DNS zone')
module storagePrivateDNSZone 'modules/dns.bicep' = {
  scope: privateDNSZoneRG
  params: {
    resourceServiceType: 'storage'
    vnetId: virtualNetwork.outputs.id
    location: region
  }
}

@description('Create the managed identity assumed by Azure devops to connect to Azure')
module managedIdentiyADOtoAZ 'modules/managedIdentity.bicep' = {
  scope: managedIdentityRG
  params: {
    name: miADOtoAZname
    region: region
  }
}

@description('Let the managed identity configure vnet peering and DNS records')
resource networkContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, hubType, 'networkContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.networkContributor)
    principalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    description: '${miADOtoAZname} Network Contributor access to subscription'
  }
}

@description('Let the managed identity assign RBAC roles (required for Azure Virtual Desktop)')
resource userAccessAdministratorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, hubType, 'UserAccessAdministrator')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      roleID.rbacAdmin
    )
    principalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    description: '${miADOtoAZname} User Access Administrator access to subscription'
  }
}

@description('Let the managed identity configure Front door and its resources')
resource CDNContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, hubType, 'CDNContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.CDNContributor)
    principalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    description: '${miADOtoAZname} CDN Contributor access to subscription'
  }
}

@description('Let the managed identity deploy terraform on the subscription')
resource TerraformContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, hubType, 'TerraformContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.contributor)
    principalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    description: '${miADOtoAZname} Terraform Contributor access to subscription'
  }
}

@description('Let the managed identity strore blobs in storage account')
resource StorageAccountBlobContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, hubType, 'StorageAccountBlobContributorAssignment')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.storageBlobDataContributor)
    principalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    description: '${miADOtoAZname} Storage Account Blob Contributor access to subscription'
  }
}

@description('Create the managed identity assumed by Github actions to trigger Azure devops pipelines')
module managedIdentiyGHtoADO 'modules/managedIdentity.bicep' = {
  scope: managedIdentityRG
  params: {
    name: miGHtoADOname
    fedCredProperties: {
      audiences: [ 'api://AzureADTokenExchange' ]
      issuer: 'https://token.actions.githubusercontent.com'
      subject: 'repo:NHSDigital/lung_cancer_screening:environment:${hubType}'
    }
    region: region
  }
}

@description('Let the GHtoADO managed identity access a subscription')
resource readerAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, hubType, 'reader')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.reader)
    principalId: managedIdentiyGHtoADO.outputs.miPrincipalID
    description: '${miGHtoADOname} Reader access to subscription'
  }
}

@description('Deploy the Key Vault for storing secrets')
module keyVaultModule 'modules/keyVault.bicep' = {
  name: 'keyVaultDeployment'
  scope: resourceGroup(resourceGroupName)
  params: {
    enableSoftDelete : enableSoftDelete
    keyVaultName: keyVaultName
    miName: miADOtoAZname
    miPrincipalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    region: region
  }
}

@description('Retrieve key vault private DNS zone')
module keyVaultPrivateDNSZone 'modules/dns.bicep' = {
  scope: privateDNSZoneRG
  params: {
    resourceServiceType: 'keyVault'
    vnetId: virtualNetwork.outputs.id
    location: region
  }
}

module computeGallery 'modules/computeGallery.bicep' = {
  scope: resourceGroup(resourceGroupName)
  params: {
    galleryName: computeGalleryName
    location: region
  }
}
