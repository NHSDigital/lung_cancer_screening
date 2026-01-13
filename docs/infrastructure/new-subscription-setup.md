# Subscription Quota requirements

New subscription that are created within Azure often have limitations on them, there are several steps needed to help avoid deployment problems.

## Step 1

Resource providers components need to be enabled:-

- Microsoft.Authorization
- Microsoft.AzureTerraform  +
- Microsoft.Billing
- Microsoft.ChangeSafety
- Microsoft.ClassicSubscription
- Microsoft.Commerce
- Microsoft.Compute +
- Microsoft.ComputeSchedule +
- Microsoft.Consumption
- Microsoft.ContainerService +
- Microsoft.CostManagement
- Microsoft.DesktopVirtualization +
- Microsoft.DevCenter +
- Microsoft.DevOpsInfrastructure +
- Microsoft.Diagnostics
- Microsoft.Features
- Microsoft.GuestConfiguration
- Microsoft.Insights
- Microsoft.KeyVault +
- Microsoft.ManagedIdentity
- Microsoft.MarketplaceOrdering
- Microsoft.Network +
- Microsoft.PolicyInsights
- Microsoft.Portal
- Microsoft.Quota +
- Microsoft.ResourceGraph
- Microsoft.ResourceIntelligence
- Microsoft.ResourceNotifications
- Microsoft.Resources
- Microsoft.Security
- Microsoft.SerialConsole
- Microsoft.Storage +
- Microsoft.Support

## Step 2

The following quotas need to be increased, raise a support ticket with Azure support to get these increased. This list used for the all the new subscriptions. Microsoft will likely need a business justification for the increase in quota, as of the time of writing this, but that will likely not be the case in the future.

| Subscription Name                     | Subscription ID                           | Environment | Region   | Alternative Region | Specify AZ | AZ / Zonal Deployment Notes | Azure Service | SKU                | Alternative SKU | Unit  | Oct-25 | Nov-25 | Dec-25 | Jan-26 | Feb-26 | Mar-26 |
|--------------------------------------|-------------------------------------------|-------------|----------|--------------------|------------|-----------------------------|---------------|--------------------|------------------|-------|--------|--------|--------|--------|--------|--------|
| Lung Cancer Risk Check - Non-live hub | ******                                      | Non Live    | UK South | N/A                | N/A        | Regional deployment         | Compute       | Standard_D2ads_v5  | N/A              | Units | 4      | 4      | 4      | 4      | 4      | 4      |
| Lung Cancer Risk Check - Live hub     | ******                                      | Live        | UK South | N/A                | N/A        | Regional deployment         | Compute       | Standard_D2ads_v5  | N/A              | Units | 4      | 4      | 4      | 4      | 4      | 4      |
| Lung Cancer Risk Check - Dev          | ******                                      | Dev         | UK South | N/A                | N/A        | Regional deployment         | Compute       | B_Standard_B1ms    | N/A              | Units | 1      | 1      | 1      | 1      | 1      | 1      |
| Lung Cancer Risk Check - Review       | ******                                      | Review      | UK South | N/A                | N/A        | Regional deployment         | Compute       | B_Standard_B1ms    | N/A              | Units | 1      | 1      | 1      | 1      | 1      | 1      |
| Lung Cancer Risk Check - Prod         | ******                                      | Prod        | UK South | N/A                | N/A        | Regional deployment         | Compute       | GP_Standard_D2ds_v5| N/A              | Units | 3      | 3      | 3      | 3      | 3      | 3      |
| Lung Cancer Risk Check - Preprod      | ******                                      | Preprod     | UK South | N/A                | N/A        | Regional deployment         | Compute       | GP_Standard_D2ds_v5| N/A              | Units | 3      | 3      | 3      | 3      | 3      | 3      |
