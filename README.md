# gcp-cicd

This repository contains sample CI/CD pipelines for Hadoop-related GCP services.

## Sample CI/CD pipeline for running Spark job on persistent cluster
Cloud build configuration location: [cloudbuild-spark-persistent.yaml](cloudbuilds/cloudbuild-spark-persistent.yaml)
Run build with this command:
```
COMMAND TBD
```

## Sample CI/CD pipeline for running Hive job on persistent cluster
Cloud build configuration location: [cloudbuild-hive-persistent.yaml](cloudbuilds/cloudbuild-hive-persistent.yaml)
Run build with this command:
```
COMMAND TBD
```

## Sample CI/CD pipeline for running Spark job on ephemeral cluster


Spark builds based on sbt. For triggering from shell several git specific substitutions are required.

Example of shell triggered build:
```
gcloud builds submit \
--substitutions=_BUILD_BUCKET=builds-2,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=$(date | md5)  \
--config cloudbuilds/cloudbuild-spark-persistent.yaml .
```

### Composer

Next steps are describes process of composer creation.


- Cloud Composer environment
```
gcloud composer environments create <ENVIRONMENT-NAME> \
    --location us-central1 \
    --machine-type n1-standard-2 \
    --zone us-central1-f

```

- DAGs and dependencies

```
gcloud composer environments update gcp-test-env-2 \
--update-pypi-packages-from-file airflow/requirements.txt \
--location us-central1
```

with

```
gcloud composer environments describe gcp-test-env-2 \
  --location us-central1 \
  --format="get(config.dagGcsPrefix)"
```

with

```
gcloud composer environments storage dags import \
  --environment gcp-test-env-2  \
  --location us-central1 \
  --source airflow/dags/sample-dag-spark-ephimeral.py
```

## Sample CI/CD pipeline for running Hive job on ephemeral cluster
