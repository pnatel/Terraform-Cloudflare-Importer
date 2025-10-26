# This script will generate terraform files for all possibly Cloudflare
# settings for supported resources, and import (most of them) in the Terraform
# state file. More details in:
# https://developers.cloudflare.com/terraform/advanced-topics/import-cloudflare-resources

# The script uses a list of resources extracted from (valid in Mar/2025):
# https://github.com/cloudflare/cf-terraforming?tab=readme-ov-file#supported-resources

# HOW TO USE IT:
# --------------
# Clone the repo, create the .env file with the below variables
# and execute "run.sh":
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


def does_file_have_content(path):
    """
    Check file size and return True if file is not empty
    """
    size = os.stat(path).st_size
    # print("\n------> File size:", size)
    if size == 0:
        print(" ------> Empty File")
        return False
    elif path == "":
        print("------> Path Invalid")
        return False
    else:
        print("\n------> File size:", size)
        return True


def remove_if_file_is_empty(path):
    """
    Remove empty file
    """
    if (path != "") and not does_file_have_content(path):
        os.remove(path)
        print("------> File empty, removed:", path)
    elif path == "":
        print("------> Path Invalid") # This should never happen
    else:
        print("------> File not empty, keeping:", path)


def account_or_zone(ResourceScope) -> list:
    if ResourceScope.lower() == "account or zone":
        acc_zone = [f"--account {ACCOUNT}",
                    f"--zone {ZONE01}",
                    f"--zone {ZONE02}"]
    elif ResourceScope.lower() == "account":
        acc_zone = [f"--account {ACCOUNT}"]
    elif ResourceScope.lower() == "zone":
        acc_zone = [f"--zone {ZONE01}",
                    f"--zone {ZONE02}"]
    else:
        print("invalid Resource scope expected account or zone, but got:", ResourceScope.lower)
        exit(3)
    return acc_zone


def generate_config(record):
    if  eval(record["GenerateSupported"]) is True and \
          eval(record["ImportSupported"]) is True:
        acc_zone = account_or_zone(record["ResourceScope"])
        # print("DEBUG:", acc_zone, record["ResourceScope"])
        for id in acc_zone:
            tty_file = f"{record['Resource']}-{id[2:5].upper()}{id[10]}.tf"
            print("------> TF File:", tty_file)
            os.system(f"cf-terraforming generate --email {CLOUDFLARE_EMAIL} \
                      --token {TF_VAR_API_TOKEN} {id} --resource-type \
                        {record['Resource']} > {tty_file}")
            remove_if_file_is_empty(tty_file)
    return "Generated configuration attempt completed, check for errors above"


# def generate_config_v5(record):
#     acc_zone = account_or_zone("Account or Zone")
#     for id in acc_zone:
#         tty_file = f"{record}-{id[2:5].upper()}{id[10]}.tf"
#         # tty_file = record[:-1] + "-" + id[2:5].upper() + id[10] + ".tf"
#         print("------> TF File:", tty_file)
#         os.system(f"cf-terraforming generate -v --email {CLOUDFLARE_EMAIL} \
#                     --token {TF_VAR_API_TOKEN} {id} --resource-type \
#                     {record} > {tty_file}")
#         if (
#             id == f"--account {ACCOUNT}"
#             and does_file_have_content(tty_file) is True
#         ):
#             print("------> File generated for account:", id)
#             break
#         remove_if_file_is_empty(tty_file)
#     return "Generated configuration"


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
                print("------> SIMULATION: No command executed")
                print(*import_list)
            elif import_list == []:
                print("------> No command to execute")
            else:
                for command in import_list:
                    print("------> COMMAND:", command)
                    os.system(command)
    else:
        return "Resource cannot be imported"
    return "Resource imported into state file attempt completed"


# def import_config_v5(record):
#     acc_zone = account_or_zone("Account or Zone")
#     for id in acc_zone:
#         os.system(f"cf-terraforming import --email {CLOUDFLARE_EMAIL} \
#                     --token {TF_VAR_API_TOKEN} {id} --resource-type \
#                     {record} >> 'import_list{id}.txt'")
#         with open(f'import_list{id}.txt', 'r') as file:
#             import_list = file.readlines()
#         # os.remove('import_list.txt')
#         if eval(str(SIMULATION)) is True:
#             print("------> SIMULATION: No command executed")
#             print(*import_list)
#         else:
#             for command in import_list:
#                 print("------> COMMAND:", command)
#                 os.system(command)
#     return "Resource imported into state file"


def get_resource_type_list() -> list:
    if ver == "4":
        resource_types = read_CSV("./resource-types_v4.csv")
    elif ver == "5":
        # os.system("terraform providers schema -json | jq -rM \
        #         '.provider_schemas[].resource_schemas|keys[]' \
        #         >> resource_list.txt")
        # with open('resource_list.txt', 'r') as file:
        #     resource_types = file.readlines()
        # # os.remove('resource_list.txt')
        resource_types = read_CSV("./resource-types_v5.csv")
    else:
        print(">>>> Version not supported")
        exit(2)
    return resource_types


def main():
    resource_types = get_resource_type_list()
    print("DEBUG: >>>> Resource types:", len(resource_types))

    if eval(str(SIMULATION)) is True:
        # Reduce the number of resources to generate and import (testing)
        # qty_resource_types = resource_types[20:30]
        qty_resource_types = resource_types[0:5]
    else:
        qty_resource_types = resource_types
    for item in qty_resource_types:
        print("\n>>>> Attempting generation and import for:", item)
        # if ver == "4":
        #     # print("DEBUG: Version: 4")
        #         print(generate_config(item))
        #         print(import_config(item))
        # elif ver == "5":
        #     # the -1 is to remove the \n from the end of the string
        #     # item = item[:-1]
        #     # print("DEBUG: Version: 5")
        #     # print(generate_config_v5(item))
        #     # print(import_config_v5(item))
        # else:
        #     print(">>>> Version not supported")
        #     exit(1)
        print(generate_config(item))
        print(import_config(item))


if __name__ == '__main__':
    main()
