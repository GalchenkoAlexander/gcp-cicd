## CI process for init actions scripts.
CI process for init actions scripts.

This cloud builds are perform next steps:
- clone init action script files and other resources to temp GCS dir
- import autoscaling-policy (for Auto-Scaling cluster only)
- create dataproc cluster with using these scripts
- submit "high load" teragen job for testing
- submit spark PI job for testing
- delete dataproc cluster
- delete autoscaling-policy (for Auto-Scaling cluster only)
- copy init actions script files to a permanent GCS
- delete temp dir from GCS 

Parameter `_CLUSTER_TYPE` is define type of cluster. It can be `single-node`, `multi-node`, `high-availability` or `auto-scaling`

Use these command to run build:

#### submit create and test Dataproc cluster build
```
gcloud builds submit \
--config=./cloudbuilds/init_actions_dataproc_cluster.yaml \
--substitutions=\
_BUCKET_NAME=${BUCKET_NAME},\
_CLUSTER_NAME=<CLUSTER_NAME>,\
_REGION=<REGION>,\
_ZONE=<ZONE>,\
_CLUSTER_TYPE=<single-node | multi-node | high-availability | auto-scaling>
```

#### Create cloud build trigger
There is an issue with google cloud build trigger. Build config has to be placed in a root dir `--build-config="init_actions_dataproc_cluster.yaml"` instead of `--build-config="./cloudbuilds/init_actions_dataproc_cluster.yaml"`
Otherwise google cloud build rise an error when trigger runs

github repo
```
gcloud beta builds triggers create github \
--description="Init actions testing for single-node cluster" \
--repo-owner="GalchenkoAlexander" \
--repo-name="gcp-cicd" \
--branch-pattern="^master$" \
--build-config="cloudbuilds/init_actions_dataproc_cluster.yaml" \
--substitutions \
_BUCKET_NAME=gcp-cicd-artifacts,\
_CLUSTER_NAME=gcp-cicd-dataproc-cluster,\
_REGION=us-central1,\
_ZONE=us-central1-b,\
_CLUSTER_TYPE=single-node
```

cloud-source-repositories
```
gcloud alpha builds triggers create cloud-source-repositories \
--repo="gcp-cicd" \
--branch-pattern="^master$" \
--build-config="cloudbuilds/init_actions_dataproc_cluster.yaml" \
--substitutions \
_BUCKET_NAME=gcp-cicd-artifacts,\
_CLUSTER_NAME=gcp-cicd-dataproc-cluster,\
_REGION=us-central1,\
_ZONE=us-central1-b,\
_CLUSTER_TYPE=single-node
```