# Terraform-Cloudflare-Importer

This script will generate terraform files for all possibly Cloudflare
settings for supported resources, and import (most of them) in the Terraform
state file. More details in:
https://developers.cloudflare.com/terraform/advanced-topics/import-cloudflare-resources

The script uses a list of resources extracted from: (From July/2024)
https://github.com/cloudflare/cf-terraforming?tab=readme-ov-file#supported-resources

## HOW TO USE IT:

1. Clone this repo
2. Create the .env file with the following variables:
   ```
   CLOUDFLARE_EMAIL=email@domain.tld
   CLOUDFLARE_API_TOKEN=XXXXXXXXXXXX
   ACCOUNT=XXXXXXXX
   ZONE01=XXXXXX
   ZONE02=xxxxx
   SIMULATION=True
   ```

> Ps: The number of zones is added/removed manually. Change it as necessary.
>
> Ps2: Keep `SIMULATION=True` in the first run the script will output the correct commands.

3. Check/update resource-types.csv table using the list of resources available in:
   https://github.com/cloudflare/cf-terraforming?tab=readme-ov-file#supported-resources
4. Execute run.sh
