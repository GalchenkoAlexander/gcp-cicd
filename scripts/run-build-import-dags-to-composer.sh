#!/usr/bin/env bash
set -euxo pipefail

. ./env-composer.sh
cd ..

### run build
gcloud builds submit \
--substitutions=\
COMPOSER_ENV_NAME=${COMPOSER_ENV_NAME},\
COMPOSER_REGION=${COMPOSER_REGION},\
SOURCE=./airflow/dags/sample-dag-hive-persistent.py \
--config ./cloudbuilds/cloudbuild-dag-import-to-composer-persistent.yaml .

