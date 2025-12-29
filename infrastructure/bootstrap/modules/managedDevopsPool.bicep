@minLength(3)
@maxLength(44)
param poolName string

@maxLength(26)
param devCenterName string

param adoOrg string
param agentProfileMaxAgentLifetime string
param devCenterProjectName string
param devopsSubnetName string
param devopsSubnetAddressPrefix string
param virtualNetworkName string

// currently non-live is running on this, will upgrade post pen testers completion
//param fabricProfileSkuName string = 'Standard_D2as_v5'
param fabricProfileSkuName string = 'Standard_D2ads_v5'
param poolSize int = 1
param location string = 'uksouth'


resource devopsSubnet 'Microsoft.Network/virtualNetworks/subnets@2025-01-01' = {
  name: '${virtualNetworkName}/${devopsSubnetName}'
  properties: {
    addressPrefix: devopsSubnetAddressPrefix
    delegations: [
      {
        name: 'Microsoft.DevOpsInfrastructure/pools'
        properties: {
          serviceName: 'Microsoft.DevOpsInfrastructure/pools'
        }
      }
    ]
  }
}

resource devCenter 'Microsoft.DevCenter/devcenters@2025-02-01' = {
  name: devCenterName
  location: location
}

resource devCenterProject 'Microsoft.DevCenter/projects@2025-02-01' = {
  name: devCenterProjectName
  location: location
  properties: {
    devCenterId: devCenter.id
  }
}

// resource pool 'microsoft.devopsinfrastructure/pools@2025-09-20' = {
//   name: poolName
//   location: location
//   properties: {
//     organizationProfile: {
//       organizations: [
//         {
//           url: 'https://dev.azure.com/${adoOrg}'
//           parallelism: 1
//         }
//       ]
//       permissionProfile: {
//         kind: 'CreatorOnly'
//       }
//       kind: 'AzureDevOps'
//     }
//     devCenterProjectResourceId: devCenterProject.id
//     maximumConcurrency: poolSize
//     agentProfile: {
//       kind: 'Stateful' // or 'Stateless' - VM creation for each job, which tends to be too slow
//       maxAgentLifetime: agentProfileMaxAgentLifetime // Only allowed if kind is Stateful
//       // gracePeriodTimeSpan: '00:30:00' // Only allowed if kind is Stateful
//       resourcePredictionsProfile: {
//         kind: 'Automatic' // 'Manual' or 'Automatic'
//         predictionPreference: 'Balanced'
//       }
//     }
//     fabricProfile: {
//       sku: {
//         name: fabricProfileSkuName
//       }
//       images: [
//         {
//           aliases: [
//             'ubuntu-22.04'
//             'ubuntu-22.04/latest'
//           ]
//           wellKnownImageName: 'ubuntu-22.04'
//         }
//       ]
//       osProfile: {
//         logonType: 'Service' // or Interactive
//       }
//       storageProfile: {
//         osDiskStorageAccountType: 'StandardSSD' // StandardSSD, Standard, or Premium
//       }
//       // Remove if you want to use 'Isolated Virtual Network'
//       networkProfile: {
//         subnetId: devopsSubnet.id
//       }
//       kind: 'Vmss'
//     }
//   }
// }
