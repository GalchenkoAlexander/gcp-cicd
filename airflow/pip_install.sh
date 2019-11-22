#!/usr/bin/env bash
#set -euxo pipefail
chmod 777 /builder/home/.cache/pip
python3 -m venv $1
source $1/bin/activate
pip3 install -r $2/requirements.txt