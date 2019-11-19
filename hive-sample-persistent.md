# Sample CI/CD pipeline for running Hive job on persistent cluster

### Build
Build steps:
- copy resources into specific gs folder
- create UDF jar file
- publish this jars into specific gs folder
- copying input dataset files to GCS

Run build with this command:

```
gcloud builds submit \
--substitutions=_BUILD_BUCKET=builds-2,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=$(date | md5)  \
--config cloudbuilds/cloudbuild-hive-persistent.yaml .
```

### Dataproc
A Dataproc cluster must be up and running

### Composer

Next steps are describes process of composer creation.

- Cloud Composer environment
```
gcloud composer environments create <ENVIRONMENT-NAME> \
    --location us-central1 \
    --machine-type n1-standard-2 \
    --zone us-central1-f \
    --env-variables=CLUSTER_NAME=<COMPOSER_NAME>,

```

- create DAGs and dependencies

```
gcloud composer environments update gcp-test-3 \
--update-pypi-packages-from-file airflow/requirements.txt \
--location us-central1
```

with

```
gcloud composer environments describe gcp-test-3 \
  --location us-central1 \
  --format="get(config.dagGcsPrefix)"
```

with

```
gcloud composer environments storage dags import \
  --environment gcp-test-3  \
  --location us-central1 \
  --source airflow/dags/sample-dag-hive-persistent.py
```

with

```
gcloud composer environments run gcp-test-3 \
--location us-central1 
```