#!/usr/bin/env bash
set -euxo pipefail

cd ../airflow/

python3 -m venv ./venv/
echo $(pwd)
source ./venv/bin/activate
echo $(pwd)
pip install -r ./requirements.txt
