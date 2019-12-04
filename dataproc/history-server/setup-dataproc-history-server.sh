#!/usr/bin/env bash

# cluster template mandatory
export PROJECT_ID='gcp-cicd'
export HISTORY_BUCKET_NAME='gcp-cicd-history'
export HISTORY_SERVER_NAME='gcp-cicd-history-server'
export HISTORY_REGION='europe-west1'
export HISTORY_ZONE='europe-west1-b'
export HISTORY_SUBNET_ID='history-server-subnet'


# Configure clusters to use GCS for log aggregation and point at the history server
cd ./cluster-templates
sed -i 's/PROJECT/${PROJECT_ID}/g' *
sed -i 's/HISTORY_BUCKET/${HISTORY_BUCKET_NAME}/g' *
sed -i 's/HISTORY_SERVER/${HISTORY_SERVER_NAME}/g' *
sed -i 's/REGION/${HISTORY_REGION}/g' *
sed -i 's/ZONE/${HISTORY_ZONE}/g' *
sed -i 's/SUBNET/${HISTORY_SUBNET_ID}/g' *