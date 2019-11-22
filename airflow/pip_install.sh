#!/usr/bin/env bash
#set -euxo pipefail
python3 -m venv $1
source $1/bin/activate
sudo -H pip install -r $2/requirements.txt