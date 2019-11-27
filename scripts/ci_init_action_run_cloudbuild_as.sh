#!/usr/bin/env bash

source ./env.sh

gcloud builds submit \
--config=../cloudbuilds/ci_init_actions_as_dataproc_cluster.yaml \
--substitutions=\
_CLUSTER_NAME=gcp-cicd-dataproc-cluster,\
_REGION=us-central1,\
_ZONE=us-central1-b,\
_BUCKET_NAME=${BUCKET_NAME}
_REPO_NAME=${REPO_NAME}
_BRANCH_NAME=${BRANCH_NAME}
_SHORT_SHA=${SHORT_SHA}
