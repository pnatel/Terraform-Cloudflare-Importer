# Terraform-Cloudflare-Importer

This script will generate terraform files for all possibly Cloudflare
settings for supported resources, and import (most of them) in the Terraform
state file. More details in:
https://developers.cloudflare.com/terraform/advanced-topics/import-cloudflare-resources

The script uses a list of Version 4 resources extracted from: (From Mar/2025)
https://github.com/cloudflare/cf-terraforming?tab=readme-ov-file#supported-resources

## HOW TO USE IT

1. Clone this repo
2. Create the .env file with the following variables:
   ```
   CLOUDFLARE_EMAIL=email@domain.tld
   TF_VAR_API_TOKEN=XXXXXXXXXXXX  # This is the Clouflare API token
   ACCOUNT=XXXXXXXX
   ZONE01=XXXXXX
   ZONE02=xxxxx
   SIMULATION=True
   ```

> PS: The number of zones is added/removed manually. Change it as necessary.
>
> PS2: Keep `SIMULATION=True` in the first run to confirm the script will output the commands as expected.

3. Update the Cloudflare version in the `provider.tf` (This script works with version's 4 and 5 of Cloudflare).
4. (FOR CLOUDFLARE VERSION 4 ONLY) Check/update resource-types.csv table using the list of resources available in:
   https://github.com/cloudflare/cf-terraforming?tab=readme-ov-file#supported-resources
5. Execute run.sh

## Error List

1. *FATA[0003] failed to detect provider installation* > The repo was not initialised (run terraform init)
2. *FATA[0004] failed to detect provider installation* > The repo was not initialised (run terraform init)
3. FATA[0010] error installing Terraform: Get "https://releases.hashicorp.com/terraform/index.json": net/http: TLS handshake timeout (try again)
4. FATA[0012] error installing Terraform: Get "https://releases.hashicorp.com/terraform/index.json": net/http: TLS handshake timeout (try again)
5. *FATA[0000] No quota has been allocated for this zone or for this account. If you're already a paid SSL for SaaS customer, please contact your Customer Success Manager for additional provisioning. If you're not yet enrolled, please fill out this form and someone from our sales team will contact you: https://www.cloudflare.com/plans/enterprise/contact/. (1404)* {'Resource': 'cloudflare_custom_hostname'} > No freebies 😕
6. FATA[0004] failed to read provider schemaexit status 1
Error: Failed to load plugin schemas
Error while loading schemas for plugin components: Failed to obtain provider
schema: Could not load the schema for provider
registry.terraform.io/cloudflare/cloudflare: failed to instantiate provider
"registry.terraform.io/cloudflare/cloudflare" to obtain schema: fork/exec
.terraform/providers/registry.terraform.io/cloudflare/cloudflare/4.40.0/darwin_arm64/terraform-provider-cloudflare_v4.40.0:
permission denied..
7. FATA[0005] You are not entitled for this service (10403)
8. FATA[0005] The request is not authorized to access this setting. Cause(s): smart_routing (1015)
9. FATA[0005] Plan level does not allow custom certificates with type  (1011) {'Resource': 'cloudflare_custom_ssl'}
10. FATA[0001] error installing Terraform: unexpected EOF {'Resource': 'cloudflare_filter'}
11. FATA[0005] Unauthorized (10000) {'Resource': 'cloudflare_logpush_job'}
12. FATA[0004] Could not route to /client/v4/zones/custom_hostnames/fallback_origin, perhaps your object identifier is invalid? (7003) {'Resource': 'cloudflare_custom_hostname_fallback_origin'}


## TODO
- simulation mode is not usefull anymore. It would be better to replace it with a sample step instead (at least for the generation part)