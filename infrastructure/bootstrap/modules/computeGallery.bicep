targetScope = 'resourceGroup'

@description('Name of the Azure Compute Gallery')
param galleryName string

@description('Location for the gallery')
param location string

resource computeGallery 'Microsoft.Compute/galleries@2023-07-03' = {
  name: galleryName
  location: location
  properties: {
    description: ''
    softDeletePolicy: {
      isSoftDeleteEnabled: false
    }
  }
}
