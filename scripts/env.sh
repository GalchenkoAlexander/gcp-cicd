#!/usr/bin/env bash
set -euxo pipefail

# PROJECT ENV
export PROJECT_ID='gcp-cicd'
export BUCKET_NAME='gcp-cicd-artifacts'
export REPO_NAME='gcp-cicd'
export BRANCH_NAME='master'
export SHORT_SHA=$(date | md5)

export ROOT_BUILD_PATH=${BUCKET_NAME}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA}


# COMPOSER ENVs
export COMPOSER_ENV_NAME=${REPO_NAME}-airflow-${SHORT_SHA}
export COMPOSER_REGION='europe-west1'
export COMPOSER_ZONE='europe-west-1b'
export COMPOSER_DAG_BUCKET==$(gcloud composer environments describe $COMPOSER_ENV_NAME --location $COMPOSER_REGION --format="get(config.dagGcsPrefix)")


#gcloud config set project ${PROJECT_ID}
