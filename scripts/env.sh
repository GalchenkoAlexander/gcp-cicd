#!/usr/bin/env bash
set -euxo pipefail

# PROJECT ENV
export PROJECT_ID='gcp-cicd'
export BUCKET_NAME='gcp-cicd-artifacts'
export REPO_NAME='gcp-cicd'
export BRANCH_NAME='master'
export SHORT_SHA=$(date | md5)

touch $(pwd)/env-persional.sh
source $(pwd)/env-persional.sh