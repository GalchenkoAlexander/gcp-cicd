#!/usr/bin/env bash
set -euxo pipefail

# PROJECT ENV
export PROJECT_ID='gcp-cicd'
export BUCKET_NAME='gcp-cicd-artifacts'
export REPO_NAME='gcp-cicd'
export BRANCH_NAME='master'
export SHORT_SHA=$('$PROJECT_ID' | md5)
#export SHORT_SHA=$(date | md5)

export ROOT_BUILD_PATH=${BUCKET_NAME}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA}

#gcloud config set project ${PROJECT_ID}
