#!/usr/bin/env bash

source ./env.sh

gcloud builds submit \
--config=../cloudbuilds/ci_init_actions_ha_dataproc_cluster.yaml \
--substitutions=\
_CLUSTER_NAME=gcp-cicd-dataproc-cluster,\
_REGION=us-central1,\
_ZONE=us-central1-b,\
_BUILD_BUCKET=${ROOT_BUILD_PATH}
