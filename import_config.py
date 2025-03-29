# This script will generate terraform files for all possibly Cloudflare
# settings for supported resources, and import (most of them) in the Terraform
# state file. More details in:
# https://developers.cloudflare.com/terraform/advanced-topics/import-cloudflare-resources

# The script uses a list of resources extracted from (valid in Mar/2025):
# https://github.com/cloudflare/cf-terraforming?tab=readme-ov-file#supported-resources

# HOW TO USE IT:
# --------------
# Clone the repo, create the .env file with the below variables and execute "run.sh":
# CLOUDFLARE_EMAIL=email@domain.tld
# TF_VAR_API_TOKEN=XXXXXXXXXXXX
# ACCOUNT=XXXXXXXX
# ZONE01=XXXXXX
# ZONE02=xxxxx
#
# PS: The number of zones is added/removed manually. Change it as necessary.

import csv
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()
CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
TF_VAR_API_TOKEN = os.getenv('TF_VAR_API_TOKEN')
ACCOUNT = os.getenv('ACCOUNT')
ZONE01 = os.getenv('ZONE01')
ZONE02 = os.getenv('ZONE02')
SIMULATION = os.getenv('SIMULATION')
ver = os.getenv('VERSION')
print(">>>> Version:", ver)
print(">>>> SIMULATION:", SIMULATION)


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


def remove_if_file_is_empty(path):
    """
    Remove empty file
    """
    if path != "" and os.stat(path).st_size == 0:
        os.remove(path)
        print("------> File removed:", path)
    elif path == "":
        print("------> Path Invalid")
    else:
        print("------> File not removed:", path)
        print("------> File size:", os.stat(path).st_size)


def account_or_zone(ResourceScope) -> list:
    if ResourceScope == "Account or Zone":
        acc_zone = [f"--account {ACCOUNT}", f"--zone {ZONE01}", f"--zone {ZONE02}"]
    elif ResourceScope == "Account":
        acc_zone = [f"--account {ACCOUNT}"]
    else:
        acc_zone = [f"--zone {ZONE01}", f"--zone {ZONE02}"]
    return acc_zone


def generate_config(record):
    if eval(str(record["GenerateSupported"])) is True:
        acc_zone = account_or_zone(record["ResourceScope"])
        for id in acc_zone:
            if eval(str(SIMULATION)) is True:
                tty_file = ""
            else:
                tty_file = f"> {record['Resource']}-{id[2:5].upper()}{id[10]}.tf"
            print("------> TF File:", tty_file)
            os.system(f"cf-terraforming generate --email {CLOUDFLARE_EMAIL} \
                      --token {TF_VAR_API_TOKEN} {id} --resource-type \
                        {record['Resource']} {tty_file}")
        remove_if_file_is_empty(tty_file)
    return "Generated configuration"


def generate_config_v5(record):
    acc_zone = account_or_zone("Account or Zone")
    for id in acc_zone:
        if eval(str(SIMULATION)) is True:
            tty_file = ""
        else:
            tty_file = f"> {record}-{id[2:5].upper()}{id[10]}.tf"
        print("------> TF File:", tty_file)
        os.system(f"cf-terraforming generate --email {CLOUDFLARE_EMAIL} \
                    --token {TF_VAR_API_TOKEN} {id} --resource-type \
                    {record} {tty_file}")
        remove_if_file_is_empty(tty_file)
    return "Generated configuration"


def import_config(record):
    if eval(record["ImportSupported"]) is True:
        acc_zone = account_or_zone(record["ResourceScope"])
        for id in acc_zone:
            os.system(f"cf-terraforming import --email {CLOUDFLARE_EMAIL} \
                        --token {TF_VAR_API_TOKEN} {id} --resource-type \
                        {record['Resource']} >> import_list.txt")
            with open('import_list.txt', 'r') as file:
                import_list = file.readlines()
            os.remove('import_list.txt')
            if eval(str(SIMULATION)) is True:
                print(import_list)
            else:
                for command in import_list:
                    print("------> COMMAND:", command)
                    os.system(command)
    return "Resource imported into state file"


def main():
    if ver == "4":
        resource_types = read_CSV("./resource-types.csv")
    elif ver == "5":
        os.system("terraform providers schema -json | jq -rM \
                                   '.provider_schemas[].resource_schemas| \
                                   keys[]' >> import_list.txt")
        with open('import_list.txt', 'r') as file:
            resource_types = file.readlines()
        os.remove('import_list.txt')
    else:
        print(">>>> Version not supported")
        exit(1)

    for item in resource_types:
        print(">>>> Attempting generation and import for:", item)
        if ver == "4":
            print(generate_config(item))
            # print(import_config(item))
        elif ver == "5":
            print(generate_config_v5(item))
            # print(import_config_v5(item))
        else:
            print(">>>> Version not supported")
            exit(1)        


if __name__ == '__main__':

    main()
