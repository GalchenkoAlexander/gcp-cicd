# Dataproc custom image
Create dataproc custom image based on Dataproc version `1.4.16-debian9` with tag `dataproc-custom-image`.
It will apply init actions from `dataproc/custom-image/init_actions.sh`
Full path to the generated image `https://www.googleapis.com/compute/beta/projects/<PROJECT_ID>/global/images/<IMAGE_NAME>` will contains file `latest_image_uri.txt`. 
This file will be stored on GCS `gs://<BUCKET_NAME>/<REPO_NAME>/<BRANCH_NAME>/<COMMIT_SHA>/dataproc-custom-image/latest_image_uri.txt"` 

Find latest Dataproc images:
`gcloud compute images list --project <PROJECT_ID> | grep "dataproc-custom-image"`

To generate dataproc custom image is using `./cloudbuilds/dataproc-custom-image.yaml`.
Run this build:
```
gcloud builds submit \
--config=./cloudbuilders/dataproc-custom-image.yaml.yaml \
--substitutions=\
_BUCKET_NAME=<BUCKET_NAME>,\
REPO_NAME=<REPO_NAME>,\
BRANCH_NAME=<BRANCH_NAME>,\
COMMIT_SHA=<COMMIT_SHA>,\
_ZONE=<ZONE>,\
_PROJECT_ID=<PROJECT_ID>,\
_IMAGE_NAME=<IMAGE_NAME>
```
The example below shows how to do this manually:
```
gcloud builds submit \
--config=./cloudbuilds/dataproc-custom-image.yaml \
--substitutions=_ZONE=us-central1-b,_BUCKET_NAME=gcp-cicd-artifacts,\
REPO_NAME=gcp-cicd,BRANCH_NAME=master,COMMIT_SHA=778899,\
_IMAGE_NAME=dataproc-custom-image-$(date +%s)
```

It will create a custom image with name `dataproc-custom-image-1575030392` with Dataproc version `1.4.16-debian9`.

