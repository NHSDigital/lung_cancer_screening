REGION=UK South
APP_SHORT_NAME=lungcs

ENVIRONMENT=preprod
ENV_CONFIG=preprod

AZURE_SUBSCRIPTION="Lung Cancer Risk Check - Preprod"
HUB_SUBSCRIPTION="Lung Cancer Risk Check - Live hub"
HUB=live
TERRAFORM_MODULES_REF=main
STORAGE_ACCOUNT_RG=rg-hub-live-uks-bootstrap
ENABLE_SOFT_DELETE=false
ADO_MANAGEMENT_POOL=private-pool-hub-live-uks
RUN_NOTIFICATIONS_SMOKE_TEST=true
DOCKER_IMAGE=ghcr.io/nhsdigital/lung_cancer_screening
