# This script will generate terraform files for all possibly Cloudflare
# settings for supported resources, and import (most of them) in the Terraform
# state file. More details in:
# https://developers.cloudflare.com/terraform/advanced-topics/import-cloudflare-resources

# The script uses a list of resources extracted from (valid in July/2024):
# https://github.com/cloudflare/cf-terraforming?tab=readme-ov-file#supported-resources

# HOW TO USE IT:
# --------------
# Clone the repo, create the .env file with the below variables and execute "run.sh":
# CLOUDFLARE_EMAIL=email@domain.tld
# CLOUDFLARE_API_TOKEN=XXXXXXXXXXXX
# ACCOUNT=XXXXXXXX
# ZONE01=XXXXXX
# ZONE02=xxxxx
#
# Ps: The number of zones is added/removed manually. Change it as necessary.

import csv
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()
CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
ACCOUNT = os.getenv('ACCOUNT')
ZONE01 = os.getenv('ZONE01')
ZONE02 = os.getenv('ZONE02')
SIMULATION = os.getenv('SIMULATION')


def read_CSV(csv_file) -> list:
    """
    docstring
    """
    temp = []
    with open(csv_file, 'r') as file:
        records = csv.DictReader(file)
        for record in records:
            temp.append(record)
    return temp


def account_or_zone(ResourceScope) -> list:
    if ResourceScope == "Account":
        acc_zone = [f"--account {ACCOUNT}"]
    else:
        acc_zone = [f"--zone {ZONE01}", f"--zone {ZONE02}"]
    return [acc_zone]


def generate_config(record):
    if eval(record["GenerateSupported"]) is True:
        acc_zone = account_or_zone(record["ResourceScope"])
        for id in acc_zone:
            if eval(str(SIMULATION)) == True:
                tty_file = ""
            else:
                tty_file = f"> {record['Resource']} {id[0]}.tf"
            os.system(f"cf-terraforming generate --email {CLOUDFLARE_EMAIL} \
                      --token {CLOUDFLARE_API_TOKEN} {id} --resource-type \
                        {record['Resource']} {tty_file}")
    return "Configuation generated"


def import_config(record):
    if eval(record["ImportSupported"]) is True:
        acc_zone = account_or_zone(record["ResourceScope"])
        for id in acc_zone:
            import_list = os.system(f"cf-terraforming import --email \
                                    {CLOUDFLARE_EMAIL} \
                                    --token {CLOUDFLARE_API_TOKEN} \
                                    {id} --resource-type {record['Resource']}")
            if import_list == type(list):
                if eval(str(SIMULATION)) == True:
                    print(import_list)
                else:
                    for command in import_list:
                        os.system(command)
    return "Terraform resources imported into state file"


def main():
    resource_types = read_CSV("./resource-types.csv")
    for item in resource_types:
        print (generate_config(item))
        print (import_config(item))


if __name__ == '__main__':

    main()
