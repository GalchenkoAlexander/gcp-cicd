Run build Dataproc Init Action for:
##### SN
```
gcloud builds submit --config=./cloudbuilds/ci_init_actions_single_node_dataproc_cluster.yaml \
--substitutions=_CLUSTER_NAME=gcp-cicd-dataproc-cluster,_REGION=us-central1,_ZONE=us-central1-b,\
_BUCKET_NAME=gcp-cicd-artifacts,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=778899
```
##### MN
```
gcloud builds submit --config=./cloudbuilds/ci_init_actions_multi_node_dataproc_cluster.yaml\
 --substitutions=_CLUSTER_NAME=gcp-cicd-dataproc-cluster,_REGION=us-central1,_ZONE=us-central1-b,\
_BUCKET_NAME=gcp-cicd-artifacts,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=778899
```
##### HA
```
gcloud builds submit --config=./cloudbuilds/ci_init_actions_ha_dataproc_cluster.yaml \
--substitutions=_CLUSTER_NAME=gcp-cicd-dataproc-cluster,_REGION=us-central1,_ZONE=us-central1-b,\
_BUCKET_NAME=gcp-cicd-artifacts,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=778899
```

##### AS
```
gcloud builds submit --config=./cloudbuilds/ci_init_actions_as_dataproc_cluster.yaml \
--substitutions=_CLUSTER_NAME=gcp-cicd-dataproc-cluster,_REGION=us-central1,_ZONE=us-central1-b,\
_BUCKET_NAME=gcp-cicd-artifacts,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=778899
```

##### dataproc custom image
```
gcloud builds submit --config=./cloudbuilds/dataproc-custom-image.yaml --substitutions=\
_ZONE=us-central1-b,\
_BUCKET_NAME=gcp-cicd-artifacts,\
REPO_NAME=gcp-cicd,\
BRANCH_NAME=master,\
SHORT_SHA=778899,\
_IMAGE_NAME=dataproc-custom-image-$(date +%s)
```