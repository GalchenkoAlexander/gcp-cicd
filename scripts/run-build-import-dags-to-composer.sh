#!/usr/bin/env bash
set -euxo pipefail

. ./env-composer.sh
cd ..

### run build
gcloud builds submit \
--config=./cloudbuilds/cloudbuild-airflow-cicd.yaml
--substitutions=\
_COMPOSER_ENV_NAME=${COMPOSER_ENV_NAME},\
_COMPOSER_REGION=${COMPOSER_REGION},\
_SOURCE=./airflow/dags/sample-dag-hive-persistent.py