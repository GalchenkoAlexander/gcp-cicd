#!/usr/bin/env bash

gcloud builds submit --config=./cloudbuilds/ci_init_actions_single_node_dataproc_cluster.yaml \
--substitutions=_CLUSTER_NAME=gcp-cicd-dataproc-cluster,_REGION=us-central1,_ZONE=us-central1-b,\
_BUCKET_NAME=gcp-cicd-artifacts,REPO_NAME=gcp-cicd,BRANCH_NAME=master,COMMIT_SHA=778899
