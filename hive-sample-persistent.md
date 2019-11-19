# Sample CI/CD pipeline for running Hive job on persistent cluster

### Build

```
gcloud builds submit \
--substitutions=_BUILD_BUCKET=builds-2,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=$(date | md5)  \
--config cloudbuilds/cloudbuild-hive-persistent.yaml .
```

##