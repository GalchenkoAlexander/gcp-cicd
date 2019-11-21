#!/usr/bin/env bash
set -euxo pipefail

cd ../airflow

python3 -m venv ./venv/
export AIRFLOW=$(pwd)
airflow scheduler