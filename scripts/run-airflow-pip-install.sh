#!/usr/bin/env bash
set -euxo pipefail

cd ../airflow/

python3 -m venv ./venv/
source ./venv/bin/activate
pip install -r ./requirements.txt
