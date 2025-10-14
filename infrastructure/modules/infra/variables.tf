variable "app_short_name" {
  description = "Application short name (6 characters)"
  type        = string
}

variable "environment" {
  description = "Application environment name"
  type        = string
}

variable "features" {
  description = "Feature flags for the deployment"
  type = object({
    front_door         = optional(bool, true)
    hub_and_spoke      = optional(bool, true)
    private_networking = optional(bool, true)
  })
}

variable "github_mi_name" {
  description = "Name of the GitHub Managed Identity."
  type        = string
}

variable "key_vault_secrets_officer_groups" {
  description = "List of Entra ID group names which will have Key Vault Secrets Officer RBAC role."
  type        = list(string)
}

variable "resource_group_name" {
  description = "Infra resource group name"
  type        = string
}

variable "hub" {
  description = "Hub name (dev or prod)"
  type        = string
}

variable "region" {
  description = "The region to deploy in"
  type        = string
}

variable "vnet_address_space" {
  description = "VNET address space. Must be unique across the hub."
  type        = string
}

variable "protect_keyvault" {
  description = "Ability to recover the key vault or its secrets after deletion"
  type        = bool
  default     = true
}

locals {
  hub_vnet_rg_name = "rg-hub-${var.hub}-uks-hub-networking"
}
