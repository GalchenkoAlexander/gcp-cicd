#!/usr/bin/env bash
set -euxo pipefail

. ./env.sh

## run Composer Airflow
gcloud composer environments create ${COMPOSER_ENV_NAME} \
--location ${COMPOSER_REGION} \
--zone ${COMPOSER_ZONE} \
--machine-type n1-highcpu-2 \
--airflow-configs=core-dags_folder=${COMPOSER_DAG_BUCKET} \
--python-version 3
#    --env-variables=CLUSTER_NAME=<COMPOSER_NAME>, \
