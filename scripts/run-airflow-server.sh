#!/usr/bin/env bash
set -euxo pipefail

cd ../airflow

export AIRFLOW=$(pwd)
airflow initdb
airflow webserver -p 8080