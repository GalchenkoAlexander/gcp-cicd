#!/usr/bin/env bash
set -euxo pipefail

cd ../airflow

export AIRFLOW=$(pwd)
export AIRFLOW_HOME=$(pwd)
export AIRFLOW__CORE__LOAD_EXAMPLES=False
airflow initdb
airflow webserver -p 8080