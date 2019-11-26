## CI process for init actions scripts.
CI process for init actions scripts.

- single node: `cloudbuilds/ci_init_actions_single_node_dataproc_cluster.yaml` 
- multi node: `cloudbuilds/ci_init_actions_multi_node_dataproc_cluster.yaml`
- high availability: `cloudbuilds/ci_init_actions_ha_dataproc_cluster.yaml`
- auto-scaling: `cloudbuilds/ci_init_actions_as_dataproc_cluster.yaml`

This cloud builds are perform next steps:
- clone init actions script files to temp GCS 
- create dataproc cluster with using these scripts
- submit teragen job to testing
- submit spark PI job to testing
- delete dataproc cluster
- copy init actions script files to a permanent GCS
- remove init actions script files from temp GCS

Use these command to run build:

#### Single node cluster
```
gcloud builds submit \
--config=./cloudbuilds/ci_init_actions_single_node_dataproc_cluster.yaml \
--substitutions=\
_BUILD_BUCKET=${BUILD_BUCKET}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA},\
_CLUSTER_NAME=<CLUSTER_NAME>,\
_REGION=<REGION>,\
_ZONE=<ZONE>
```

#### Multi node cluster
```
gcloud builds submit \
--config=./cloudbuilds/ci_init_actions_multi_node_dataproc_cluster.yaml \
--substitutions=\
_BUILD_BUCKET=${BUILD_BUCKET}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA},\
_CLUSTER_NAME=<CLUSTER_NAME>,\
_REGION=<REGION>,\
_ZONE=<ZONE>
```

#### HA cluster
```
gcloud builds submit \
--config=./cloudbuilds/ci_init_actions_ha_dataproc_cluster.yaml \
--substitutions=\
_BUILD_BUCKET=${BUILD_BUCKET}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA},\
_CLUSTER_NAME=<CLUSTER_NAME>,\
_REGION=<REGION>,\
_ZONE=<ZONE>
```

#### Auto-Scaling cluster
