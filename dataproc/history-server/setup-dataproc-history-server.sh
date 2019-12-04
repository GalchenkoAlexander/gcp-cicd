#!/usr/bin/env bash

# cluster template mandatory
export PROJECT_ID='gcp-cicd'
export HISTORY_BUCKET_NAME='gcp-cicd-history'
export HISTORY_SERVER_NAME='gcp-cicd-history-server'
export HISTORY_REGION='europe-west1'
export HISTORY_ZONE='europe-west1-b'
export HISTORY_SUBNET_ID='history-server-subnet'

# cluster networking mandatory
export HISTORY_NET_ID='history-server-net'
export HISTORY_SERVER_ACCOUNT='history-server-account'
export HISTORY_FIREWALL_RULE=${HISTORY_SUBNET_ID}'-hadoop-history-ui-ssh'


## Storage and Service Account Setup

# Stage an empty file to create the spark-events path on GCS.
gsutil mb -c regional -l ${HISTORY_REGION} gs://${HISTORY_BUCKET_NAME}
touch .keep
gsutil cp .keep gs://${HISTORY_BUCKET_NAME}/spark-events/.keep
rm .keep

# Create a service account for history server
gcloud iam service-accounts create ${HISTORY_SERVER_ACCOUNT}

# Give this service account permissions to run a Dataproc cluster
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
--member=serviceAccount:${HISTORY_SERVER_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
--role=roles/dataproc.worker

# Grant read access to the history bucket
gsutil iam ch serviceAccount:${HISTORY_SERVER_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com:objectViewer \
gs://${HISTORY_BUCKET_NAME}


## Setting up a Network

# creates a regional network and specifies that we will create your own sub-networks.
gcloud compute networks create ${HISTORY_NET_ID} \
--bgp-routing-mode regional \
--subnet-mode custom

# Create a subnet for dataproc. It specifies a CIDR range that specifies
# the range of internal IPs for the machines on this network from 10.128.0.0 to 10.128.255.255
# It also enable private Google access
gcloud compute networks subnets create ${HISTORY_SUBNET_ID} \
--range 10.128.0.0/16 \
--network ${HISTORY_NET_ID} \
--region ${HISTORY_REGION} \
--enable-private-ip-google-access

# Create a firewall rule to allow ssh for the hadoop-history-ui-access tag
gcloud compute firewall-rules create ${HISTORY_FIREWALL_RULE} \
--allow tcp:22 \
--direction INGRESS \
--network ${HISTORY_NET_ID} \
--target-tags hadoop-history-ui-access,hadoop-admin-ui-access \
--source-ranges 0.0.0.0/0

# create this firewall rule as well to allow all tcp, udp and icmp traffic between nodes with any of the specified tags
gcloud compute firewall-rules create ${HISTORY_SUBNET_ID} \
--allow tcp,udp,icmp \
--source-tags hadoop-history-ui-access,hadoop-admin-ui-access \
--target-tags hadoop-history-ui-access,hadoop-admin-ui-access


## Spinning up a History Server

# Configure clusters to use GCS for log agregation and point at the history server
cd ./cluster-templates
sed -i 's/PROJECT/${PROJECT_ID}/g' *
sed -i 's/HISTORY_BUCKET/${HISTORY_BUCKET_NAME}/g' *
sed -i 's/HISTORY_SERVER/${HISTORY_SERVER_NAME}/g' *
sed -i 's/REGION/${HISTORY_REGION}/g' *
sed -i 's/ZONE/${HISTORY_ZONE}/g' *
sed -i 's/SUBNET/${HISTORY_SUBNET_ID}/g' *

# Stage initialization action for disabling history servers on ephemeral clusters
cd ..
gsutil cp ./init-actions/disable-history-servers.sh gs://${HISTORY_BUCKET_NAME}/init-actions/