param storageLocation string
param storageName string
param enableSoftDelete bool
param miPrincipalID string
param miName string

// Optional parameters
@description('Optional Entra ID group object ID')
param userGroupPrincipalID string = ''

@description('Optional Entra ID group name')
param userGroupName string = ''

var enableGroupRbac = !empty(userGroupPrincipalID) && !empty(userGroupName)

// Create storage account without public access
resource storageAccount 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: storageName
  location: storageLocation
  sku: {
    name: 'Standard_RAGRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    encryption: {
      requireInfrastructureEncryption: true
    }
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: 'Disabled'
  }
}


// Create the blob service
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    containerDeleteRetentionPolicy: {
      days: enableSoftDelete ? 15 : null
      enabled: enableSoftDelete
    }
    deleteRetentionPolicy: {
      days: enableSoftDelete ? 15 : null
      enabled: enableSoftDelete
    }
    isVersioningEnabled: true
  }
}

// Create the blob container
resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2024-01-01' = {
  parent: blobService
  name: 'terraform-state'
  properties: {
    publicAccess: 'None'
    defaultEncryptionScope: '$account-encryption-key'
    denyEncryptionScopeOverride: false
  }
}

// See: https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
var roleID = {
  blobContributor: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
}

// Define role assignments array
var roleAssignments = [
  {
    roleName: 'blobContributor'
    roleId: roleID.blobContributor
    description: 'Blob Contributor access to subscription'
  }
]

// Let the managed identity edit the terraform state
resource blobContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, miPrincipalID, 'blobContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleID.blobContributor)
    principalId: miPrincipalID
    description: '${miName} Network Contributor access to subscription'
  }
}

// Entra ID Group RBAC assignments (ONLY created if params are provided)
resource groupRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [
  for role in roleAssignments: if (enableGroupRbac) {
    name: guid(subscription().subscriptionId, userGroupPrincipalID, role.roleName)
    properties: {
      roleDefinitionId: subscriptionResourceId(
        'Microsoft.Authorization/roleDefinitions',
        role.roleId
      )
      principalId: userGroupPrincipalID
      principalType: 'Group'
      description: '${userGroupName} ${role.description}'
    }
  }
]

// Output the storage account ID so it can be used to create the private endpoint
output storageAccountID string = storageAccount.id
