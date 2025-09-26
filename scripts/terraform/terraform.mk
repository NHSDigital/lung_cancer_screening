DOCKER_IMAGE=
REGION=UK South
APP_SHORT_NAME=lungcs

poc: # Target the poc environment - make poc <action>
	$(eval include infrastructure/environments/poc/variables.sh)

dev: # Target the dev environment - make dev <action>
	$(eval include infrastructure/environments/dev/variables.sh)

preprod: # Target the preprod environment - make preprod <action>
	$(eval include infrastructure/environments/preprod/variables.sh)

review: # Target the review infrastructure, or a review app if PR_NUMBER is used - make review <action> [PR_NUMBER=<pr_number>]
	$(eval include infrastructure/environments/review/variables.sh)
	$(if ${PR_NUMBER}, $(eval export TF_VAR_deploy_infra=false), $(eval export TF_VAR_deploy_container_apps=false))
	$(if ${PR_NUMBER}, $(eval export ENVIRONMENT=pr-${PR_NUMBER}), $(eval export ENVIRONMENT=review))

db-setup:
	$(if ${TF_VAR_deploy_container_apps},, scripts/bash/db_run_job.sh ${ENVIRONMENT} ${PR_NUMBER})

ci: # Skip manual approvals when running in CI - make ci <env> <action>
	$(eval AUTO_APPROVE=-auto-approve)
	$(eval SKIP_AZURE_LOGIN=true)

set-azure-account: # Set the Azure account for the environment - make <env> set-azure-account
	[ "${SKIP_AZURE_LOGIN}" != "true" ] && az account set -s ${AZURE_SUBSCRIPTION} || true

resource-group-init: set-azure-account get-subscription-ids # Initialise the resources required by terraform - make <env> resource-group-init
	$(eval STORAGE_ACCOUNT_NAME=sa${APP_SHORT_NAME}${ENV_CONFIG}tfstate)
	scripts/bash/resource_group_init.sh "${REGION}" "${HUB_SUBSCRIPTION_ID}" "${ENABLE_SOFT_DELETE}" "${ENV_CONFIG}" "${STORAGE_ACCOUNT_RG}" "${STORAGE_ACCOUNT_NAME}" "${APP_SHORT_NAME}" "${ARM_SUBSCRIPTION_ID}"

get-subscription-ids: # Retrieve the hub subscription ID based on the subscription name in ${HUB_SUBSCRIPTION} - make <env> get-subscription-ids
	$(eval HUB_SUBSCRIPTION_ID=$(shell az account show --query id --output tsv --name ${HUB_SUBSCRIPTION}))
	$(if ${ARM_SUBSCRIPTION_ID},,$(eval export ARM_SUBSCRIPTION_ID=$(shell az account show --query id --output tsv)))

terraform-init-no-backend: # Initialise terraform modules only and update terraform lock file - make <env> terraform-init-no-backend
	rm -rf infrastructure/modules/dtos-devops-templates
	git -c advice.detachedHead=false clone --depth=1 --single-branch --branch ${TERRAFORM_MODULES_REF} \
		https://github.com/NHSDigital/dtos-devops-templates.git infrastructure/modules/dtos-devops-templates
	terraform -chdir=infrastructure/terraform init -upgrade -backend=false

terraform-init: set-azure-account get-subscription-ids # Initialise Terraform - make <env> terraform-init
	$(eval STORAGE_ACCOUNT_NAME=sa${APP_SHORT_NAME}${ENV_CONFIG}tfstate)
	$(eval export ARM_USE_AZUREAD=true)

	rm -rf infrastructure/modules/dtos-devops-templates
	git -c advice.detachedHead=false clone --depth=1 --single-branch --branch ${TERRAFORM_MODULES_REF} \
		https://github.com/NHSDigital/dtos-devops-templates.git infrastructure/modules/dtos-devops-templates

	terraform -chdir=infrastructure/terraform init -upgrade -reconfigure \
		-backend-config=subscription_id=${HUB_SUBSCRIPTION_ID} \
		-backend-config=resource_group_name=${STORAGE_ACCOUNT_RG} \
		-backend-config=storage_account_name=${STORAGE_ACCOUNT_NAME} \
		-backend-config=key=${ENVIRONMENT}.tfstate

	$(eval export TF_VAR_app_short_name=${APP_SHORT_NAME})
#	$(eval export TF_VAR_docker_image=${DOCKER_IMAGE}:${DOCKER_IMAGE_TAG})
	$(eval export TF_VAR_environment=${ENVIRONMENT})
#	$(eval export TF_VAR_env_config=${ENV_CONFIG})
#	$(eval export TF_VAR_hub=${HUB})
#	$(eval export TF_VAR_hub_subscription_id=${HUB_SUBSCRIPTION_ID})

terraform-plan: terraform-init # Plan Terraform changes - make <env> terraform-plan DOCKER_IMAGE_TAG=abcd123
	terraform -chdir=infrastructure/terraform plan -var-file ../environments/${ENV_CONFIG}/variables.tfvars

terraform-apply: terraform-init # Apply Terraform changes - make <env> terraform-apply DOCKER_IMAGE_TAG=abcd123
	terraform -chdir=infrastructure/terraform apply -var-file ../environments/${ENV_CONFIG}/variables.tfvars ${AUTO_APPROVE}

terraform-destroy: terraform-init # Destroy Terraform resources - make <env> terraform-destroy
	terraform -chdir=infrastructure/terraform destroy -var-file ../environments/${ENV_CONFIG}/variables.tfvars ${AUTO_APPROVE}

terraform-validate: terraform-init-no-backend # Validate Terraform changes - make <env> terraform-validate
	terraform -chdir=infrastructure/terraform validate
