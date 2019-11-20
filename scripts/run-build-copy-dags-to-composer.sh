#!/usr/bin/env bash

. ./env.sh

cd ..

### run build
gcloud builds submit \
--substitutions=COMPOSER_DAG_BUCKET=${COMPOSER_DAG_BUCKET},SOURCE=./airflow/dags/sample-dag-hive-persistent.py \
--config ./cloudbuilds/cloudbuild-dag-import-to-composer-persistent.yaml .

