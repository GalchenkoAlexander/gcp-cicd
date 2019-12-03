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

#### Dataproc cluster
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