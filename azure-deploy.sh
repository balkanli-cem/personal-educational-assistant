#!/bin/bash

# Azure deployment script
echo "Starting Azure deployment..."

# Set variables
RESOURCE_GROUP="personalized-education-rg"
APP_NAME="personalized-educational-assistant"
LOCATION="eastus"
SKU="B1"

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service plan
echo "Creating App Service plan..."
az appservice plan create --name "${APP_NAME}-plan" --resource-group $RESOURCE_GROUP --sku $SKU --is-linux

# Create Web App
echo "Creating Web App..."
az webapp create --resource-group $RESOURCE_GROUP --plan "${APP_NAME}-plan" --name $APP_NAME --deployment-local-git

# Configure app settings
echo "Configuring app settings..."
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME --settings \
  DATABASE_URL="$(az postgres flexible-server show-connection-string --name your-db-server --admin-user postgres --admin-password your-password --database-name personalized_education --query connectionString -o tsv)" \
  OPENAI_API_KEY="your-openai-api-key"

echo "Deployment completed!"