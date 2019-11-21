#!/usr/bin/env bash
set -euxo pipefail

. ./env.sh

# COMPOSER ENVs
export COMPOSER_ENV_NAME=${REPO_NAME}-airflow-${SHORT_SHA}
export COMPOSER_REGION='europe-west1'
export COMPOSER_ZONE='europe-west1-b'
export COMPOSER_DAG_BUCKET==$(gcloud composer environments describe $COMPOSER_ENV_NAME --location $COMPOSER_REGION --format="get(config.dagGcsPrefix)")
