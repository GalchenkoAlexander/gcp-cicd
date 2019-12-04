# Dataproc custom image
Create dataproc custom image based on Dataproc version `1.4.16-debian9` with tag `dataproc-custom-image`.
It will apply init actions from [dataproc/init-actions/custom-image-init-actions.sh](../dataproc/init-actions/custom-image-init-actions.sh)
Full path to the generated image `https://www.googleapis.com/compute/beta/projects/<PROJECT_ID>/global/images/<IMAGE_NAME>` will contains file `latest_image_uri.txt`. 
This file will be stored on GCS `gs://<BUCKET_NAME>/<REPO_NAME>/<BRANCH_NAME>/<COMMIT_SHA>/dataproc-custom-image/latest_image_uri.txt"` 

Find Dataproc images:
`gcloud compute images list --project <PROJECT_ID> | grep "dataproc-custom-image"`

To generate dataproc custom image is using [cloudbuilds/dataproc-custom-image.yaml](../cloudbuilds/dataproc-custom-image.yaml).

#### Generate custom image based on a Dataproc version
```
gcloud builds submit \
--config=./cloudbuilds/dataproc-custom-image.yaml \
--substitutions=\
_BUCKET_NAME=<BUCKET_NAME>,\
_ZONE=<ZONE>,\
_IMAGE_NAME=<IMAGE_NAME>.\
_DATAPROC_VERSION=<1.4.16-debian9 | ...>
```
Find necessary version here [Cloud Dataproc Release notes](https://cloud.google.com/dataproc/docs/release-notes) for `_DATAPROC_VERSION`

#### Generate custom image from base Dataproc image
To generate custom image from any others base Dataproc image you need to change file `dataproc-custom-image.yaml`
Change this `'--dataproc-version', '${_DATAPROC_VERSION}',` to `'--base-image-uri=projects/${PROJECT_ID}/global/images/${_BASE_IMAGE_NAME}',`
This `--base-image-uri` argument is mutually exclusive with `--dataproc-version` 
```
gcloud builds submit \
--config=./cloudbuilds/dataproc-custom-image.yaml \
--substitutions=\
_BUCKET_NAME=<BUCKET_NAME>,\
_ZONE=<ZONE>,\
_IMAGE_NAME=<IMAGE_NAME>,\
_BASE_IMAGE_NAME=<BASE_IMAGE_NAME>
```
Find base image `gcloud compute images list`

The example below shows how to do this manually:
```
gcloud builds submit --config=./cloudbuilds/dataproc-custom-image.yaml \
--substitutions=\
_ZONE=us-central1-b,\
_BUCKET_NAME=gcp-cicd-artifacts,\
REPO_NAME=gcp-cicd,\
BRANCH_NAME=master,\
COMMIT_SHA=778899,\
_IMAGE_NAME=dataproc-custom-image-$(date +%s),\
_DATAPROC_VERSION=1.4.16-debian9
```

It will create a custom image with name `dataproc-custom-image-1575030392` with Dataproc version `1.4.16-debian9`.

#### Cloud build steps
- clone repo from [dataproc-custom-images](https://github.com/GoogleCloudPlatform/dataproc-custom-images). 
It is used to generate image
- run `generate_custom_image.py` to generate image
- create `latest_image_uri.txt` file with image path
- copy resources to GCS and update manifest

#### Create cloud build trigger
github repo
```
gcloud beta builds triggers create github \
--description="Data proc custom image" \
--repo-owner="GalchenkoAlexander" \
--repo-name="gcp-cicd" \
--branch-pattern="^master$" \
--build-config="cloudbuilds/dataproc-custom-image.yaml" \
--substitutions \
_BUCKET_NAME=gcp-cicd-artifacts,\
_ZONE=us-central1-b,\
_IMAGE_NAME=dataproc-custom-image-$(date +%s),\
_DATAPROC_VERSION=1.4.16-debian9
```
cloud-source-repositories
```
gcloud alpha builds triggers create cloud-source-repositories \
--repo="gcp-cicd" \
--branch-pattern="^master$" \
--build-config="cloudbuilds/dataproc-custom-image.yaml" \
--substitutions \
_BUCKET_NAME=gcp-cicd-artifacts,\
_ZONE=us-central1-b,\
_IMAGE_NAME=dataproc-custom-image-$(date +%s),\
_DATAPROC_VERSION=1.4.16-debian9
```
#### More info found here 
- [dataproc-custom-images](https://github.com/GoogleCloudPlatform/dataproc-custom-images)