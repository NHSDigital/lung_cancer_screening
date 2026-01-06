# Fix POC environment variables for terraform.mk - these differ from new prod like envs
REGION=UK South
APP_SHORT_NAME=lungcs

ENVIRONMENT=poc
ENV_CONFIG=poc
AZURE_SUBSCRIPTION="Lung Cancer Screening - Dev"
HUB_SUBSCRIPTION="Lung Cancer Screening - Dev"
STORAGE_ACCOUNT_RG=rg-tfstate-poc-uks
TERRAFORM_MODULES_REF=main
ENABLE_SOFT_DELETE=false
DOCKER_IMAGE=ghcr.io/nhsdigital/lung_cancer_screening
