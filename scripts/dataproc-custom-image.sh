#!/usr/bin/env bash
set -euxo pipefail

gcloud builds submit --config=./cloudbuilds/dataproc-custom-image.yaml \
--substitutions=\
_ZONE=us-central1-b,\
_BUCKET_NAME=gcp-cicd-artifacts,\
_IMAGE_NAME=dataproc-custom-image-1-$(date +%s),\
_DATAPROC_VERSION=1.4.16-debian9
