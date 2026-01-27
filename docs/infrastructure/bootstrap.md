# Bootstrap environment deployment

## Deploy the bootstrap environment

Run the bootstrap deployment for the required hub environment:

```bash
make <hub-environment> bootstrap
```

Example

```bash
make hub-nonlive bootstrap
```

## Find the AVD SP object id (run as someone with AAD read access)

```bash
az ad sp show --id <principle id> --query id
```

## Then assign the role (run as Owner)

```bash
az role assignment create \
  --assignee-object-id <AVD_SP_OBJECT_ID> \
  --role "Desktop Virtualization Power On Contributor" \
  --scope /subscriptions/<SUBSCRIPTION_ID>
```
