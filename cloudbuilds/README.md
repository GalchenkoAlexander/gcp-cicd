# Cloud builds



## CI process for init actions scripts.
 `ci_init_actions_single_node_dataproc_cluster.yaml` and `ci_init_actions_multi_node_dataproc_cluster.yaml`
CI process for init actions scripts.

This cloud builds have next steps:
- clone init actions script files to GCS 
- create dataproc cluster and uses these scripts
- submit teragen job to testing
- submit spark PI job to testing
- delete dataproc cluster 
- remove init actions script files from GCS

Run this build to use command:

#### Single node cluster
```
gcloud builds submit \
--config=./cloudbuilders/ci_init_actions_single_node_dataproc_cluster.yaml \
--substitutions=\
_BUILD_BUCKET=${BUILD_BUCKET}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA},\
_CLUSTER_NAME=<CLUSTER_NAME>,\
_REGION=<REGION>,\
_ZONE=<ZONE>
```

#### Multi node cluster
```
gcloud builds submit \
--config=./cloudbuilders/ci_init_actions_multi_node_dataproc_cluster.yaml \
--substitutions=\
_BUILD_BUCKET=${BUILD_BUCKET}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA},\
_CLUSTER_NAME=<CLUSTER_NAME>,\
_REGION=<REGION>,\
_ZONE=<ZONE>
```

#### HA cluster
TODO

#### Auto-Scaling cluster
