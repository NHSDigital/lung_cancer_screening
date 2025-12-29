REGION=UK South
APP_SHORT_NAME=lungcs

ENVIRONMENT=dev
ENV_CONFIG=dev

AZURE_SUBSCRIPTION="Lung Cancer Risk Check - Dev"
HUB_SUBSCRIPTION="Lung Cancer Risk Check - Non-live hub"
HUB=nonlive
TERRAFORM_MODULES_REF=main
STORAGE_ACCOUNT_RG=rg-hub-nonlive-uks-bootstrap
ENABLE_SOFT_DELETE=false
ADO_MANAGEMENT_POOL=private-pool-hub-nonlive-uks
RUN_NOTIFICATIONS_SMOKE_TEST=true
DOCKER_IMAGE=ghcr.io/nhsdigital/lung_cancer_screening
