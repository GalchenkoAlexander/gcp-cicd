#!/usr/bin/env bash
set -euxo pipefail

. ./env-composer.sh

## run Composer Airflow
gcloud composer environments create ${COMPOSER_ENV_NAME} \
--location ${COMPOSER_REGION} \
--zone ${COMPOSER_ZONE} \
--machine-type n1-highcpu-2 \
--python-version 3 \
--service-account ${SERVICE_ACCOUNT}
#--airflow-configs=core-dags_folder=${COMPOSER_DAG_BUCKET} \
#--env-variables=CLUSTER_NAME=<COMPOSER_NAME>, \
