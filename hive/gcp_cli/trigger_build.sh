#!/usr/bin/env bash
#export GOOGLE_CLOUD_PROJECT=gal-wm-test
#gcloud config set project ${GOOGLE_CLOUD_PROJECT}

gcloud builds submit --config=cloudbuild.yaml