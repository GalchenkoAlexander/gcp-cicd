#!/usr/bin/env bash

export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
export REPO_NAME=${PROJECT_ID}
#export BRANCH_NAME='master'
#export SHORT_SHA='sx782gdz'
export REPO_PATH=${PROJECT_ID}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA}
