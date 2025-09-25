targetScope='subscription'

param enableSoftDelete bool
param envConfig string
param region string
param storageAccountRGName string
param storageAccountName string
param appShortName string

var hubMap = {
  dev:                  'dev'
  int:                  'dev'
  review:               'dev'
  nft:                  'dev'
  preprod:              'prod'
  prd:                  'prod'
}
var privateEndpointRGName = 'rg-hub-${envConfig}-uks-hub-private-endpoints'
var privateDNSZoneRGName = 'rg-hub-${hubMap[envConfig]}-uks-private-dns-zones'
var managedIdentityRGName = 'rg-mi-${envConfig}-uks'
var infraResourceGroupName = 'rg-lungcs-${envConfig}-infra'
var keyVaultName = 'kv-lungcs-${envConfig}-inf'

var miADOtoAZname = 'mi-${appShortName}-${envConfig}-adotoaz-uks'
var miGHtoADOname = 'mi-${appShortName}-${envConfig}-ghtoado-uks'

// See: https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
var roleID = {
  CDNContributor: 'ec156ff8-a8d1-4d15-830c-5b80698ca432'
  kvSecretsUser: '4633458b-17de-408a-b874-0445c86b69e6'
  networkContributor: '4d97b98b-1d4f-4787-a291-c67834d212e7'
  rbacAdmin: 'f58310d9-a9f6-439a-9e8d-f62e7b41a168'
  reader: 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
}

// Retrieve existing terraform state resource group
resource storageAccountRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: storageAccountRGName
}
// Retrieve existing private endpoint resource group
resource privateEndpointResourceGroup 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: privateEndpointRGName
}
// Retrieve existing private DNS zone resource group
resource privateDNSZoneRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: privateDNSZoneRGName
}
// Retrieve existing managed identity resource group
resource managedIdentityRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: managedIdentityRGName
}

// Create the managed identity assumed by Azure devops to connect to Azure
module managedIdentiyADOtoAZ 'managedIdentity.bicep' = {
  scope: managedIdentityRG
  params: {
    name: miADOtoAZname
    region: region
  }
}

// Create the managed identity assumed by Github actions to trigger Azure devops pipelines
module managedIdentiyGHtoADO 'managedIdentity.bicep' = {
  scope: managedIdentityRG
  params: {
    name: miGHtoADOname
    fedCredProperties: {
      audiences: [ 'api://AzureADTokenExchange' ]
      issuer: 'https://token.actions.githubusercontent.com'
      subject: 'repo:NHSDigital/lung_cancer_screening:environment:${envConfig}'
    }
    region: region
  }
}

// Let the GHtoADO managed identity access a subscription
resource readerAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, envConfig, 'reader')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.reader)
    principalId: managedIdentiyGHtoADO.outputs.miPrincipalID
    description: '${miGHtoADOname} Reader access to subscription'
  }
}

// Create the storage account, blob service and container
module terraformStateStorageAccount 'storage.bicep' = {
  scope: storageAccountRG
  params: {
    storageLocation: region
    storageName: storageAccountName
    enableSoftDelete: enableSoftDelete
    miPrincipalID: managedIdentiyADOtoAZ.outputs.miPrincipalID
    miName: miADOtoAZname
  }
}

// Retrieve storage private DNS zone
module storagePrivateDNSZone 'dns.bicep' = {
  scope: privateDNSZoneRG
  params: {
    resourceServiceType: 'storage'
  }
}

// Retrieve key vault private DNS zone
module keyVaultPrivateDNSZone 'dns.bicep' = {
  scope: privateDNSZoneRG
  params: {
    resourceServiceType: 'keyVault'
  }
}

// Create private endpoint and register DNS
module storageAccountPrivateEndpoint 'privateEndpoint.bicep' = {
  scope: privateEndpointResourceGroup
  params: {
    hub: hubMap[envConfig]
    region: region
    name: storageAccountName
    resourceServiceType: 'storage'
    resourceID: terraformStateStorageAccount.outputs.storageAccountID
    privateDNSZoneID: storagePrivateDNSZone.outputs.privateDNSZoneID
  }
}

// Let the managed identity configure vnet peering and DNS records
resource networkContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, envConfig, 'networkContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.networkContributor)
    principalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    description: '${miADOtoAZname} Network Contributor access to subscription'
  }
}

// Create infra resource group
resource infraRG 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: infraResourceGroupName
  location: region
}

// Private endpoint for infra key vault
module kvPrivateEndpoint 'privateEndpoint.bicep' = {
  scope: resourceGroup(infraResourceGroupName)
  params: {
    hub: hubMap[envConfig]
    region: region
    name: keyVaultName
    resourceServiceType: 'keyVault'
    resourceID: keyVaultModule.outputs.keyVaultID
    privateDNSZoneID: keyVaultPrivateDNSZone.outputs.privateDNSZoneID
  }
}

// Use a module to deploy Key Vault into the infra RG
module keyVaultModule 'keyVault.bicep' = {
  name: 'keyVaultDeployment'
  scope: resourceGroup(infraResourceGroupName)
  params: {
    enableSoftDelete : enableSoftDelete
    keyVaultName: keyVaultName
    miName: miADOtoAZname
    miPrincipalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    region: region
  }
}

// Let the managed identity configure Front door and its resources
resource CDNContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, envConfig, 'CDNContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.CDNContributor)
    principalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    description: '${miADOtoAZname} CDN Contributor access to subscription'
  }
}

// Let the managed identity assign the Key Vault Secrets User role to the container app managed identity
resource rbacAdminAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, envConfig, 'rbacAdmin')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.rbacAdmin)
    principalId: managedIdentiyADOtoAZ.outputs.miPrincipalID
    condition: '((!(ActionMatches{\'Microsoft.Authorization/roleAssignments/write\'})) OR (@Request[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals {${roleID.kvSecretsUser}})) AND ((!(ActionMatches{\'Microsoft.Authorization/roleAssignments/delete\'})) OR (@Resource[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals {${roleID.kvSecretsUser}}))'
    conditionVersion: '2.0'
    description: '${miADOtoAZname} Role Based Access Control Administrator access to subscription. Only allows assigning the Key Vault Secrets User role.'
  }
}

output miPrincipalID string = managedIdentiyADOtoAZ.outputs.miPrincipalID
output miName string = miADOtoAZname
output keyVaultPrivateDNSZone string = keyVaultPrivateDNSZone.outputs.privateDNSZoneID
output storagePrivateDNSZone string = storagePrivateDNSZone.outputs.privateDNSZoneID
