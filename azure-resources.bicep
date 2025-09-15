@description('The name of the application')
param appName string = 'personalized-educational-assistant'

@description('The location for all resources')
param location string = resourceGroup().location

@description('The SKU for the App Service plan')
param appServicePlanSku string = 'B1'

@description('The admin username for PostgreSQL')
param postgresAdminUsername string = 'postgres'

@description('The admin password for PostgreSQL')
@secure()
param postgresAdminPassword string

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: '${appName}-plan'
  location: location
  sku: {
    name: appServicePlanSku
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      appSettings: [
        {
          name: 'DATABASE_URL'
          value: 'postgresql://${postgresAdminUsername}:${postgresAdminPassword}@${postgresServer.properties.fullyQualifiedDomainName}:5432/personalized_education'
        }
        {
          name: 'OPENAI_API_KEY'
          value: '@Microsoft.KeyVault(SecretUri=${keyVault.properties.vaultUri}secrets/openai-api-key/)'
        }
      ]
    }
  }
}

// PostgreSQL Flexible Server
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: '${appName}-db'
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: postgresAdminUsername
    administratorLoginPassword: postgresAdminPassword
    version: '13'
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
    }
  }
}

// PostgreSQL Database
resource postgresDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  parent: postgresServer
  name: 'personalized_education'
  properties: {
    charset: 'utf8'
    collation: 'en_US.utf8'
  }
}

// Key Vault for secrets
resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: '${appName}-kv'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: 'your-object-id'
        permissions: {
          secrets: ['all']
        }
      }
    ]
  }
}