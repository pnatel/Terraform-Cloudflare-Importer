#!/bin/bash

echo "----------------------RUN.SH---------------------------"
echo "-------------------IF-.venv-folder------------------------"
if [ -d ".venv" ]
then
    echo "----------------------IF THEN---------------------------"
    source .venv/bin/activate
    pip install -r requirements.txt
    if [[ $(terraform providers | grep cloudflare) =~ "4" ]]; then
        export VERSION="4"
    else
        export VERSION="5"
    fi
    echo Version=$VERSION
    terraform init -upgrade
    python3 ./import_config.py & \
    wait
else
    echo "----------------------IF ELSE---------------------------"
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    if [[ $(terraform providers | grep cloudflare) =~ "4" ]]; then
        export VERSION="4"
    else
        export VERSION="5"
    fi
    echo Version=$VERSION
    terraform init -upgrade
    python3 ./import_config.py & \
    wait
fi
echo "----------------------IF END---------------------------"
