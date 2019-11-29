#!/usr/bin/env bash
set -euxo pipefail

gcloud builds submit --config=../cloudbuilds/dataproc-custom-image.yaml \
--substitutions=_ZONE=us-central1-b,_BUCKET_NAME=gcp-cicd-artifacts,\
REPO_NAME=gcp-cicd,BRANCH_NAME=master,COMMIT_SHA=778899,\
_IMAGE_NAME=dataproc-custom-image-1-$(date +%s)
