# CI/CD for Airflow DAG
This document describes CI/CD pipeline for Airflow DAGs, specifically:
* Capturing DAGs from source repository 
* Running tests
* Staging DAGs in Cloud Storage

*Notice that CI process is decoupled from CD process: i.e., DAGs deployment to some Cloud Composer environment is separate step and not included into the build.*

Source DAGs are here: [Airflow DAGs](../airflow/dags)

Cloud Build YAML configuration file is here: [cloudbuild-airflow-cicd.yaml](../cloudbuilds/cloudbuild-airflow-cicd.yaml)

## Prerequisites
Before running build make sure:
* There is a GCS bucket to store artifacts

## How to start build
Run build with this command:
```
gcloud builds submit \
--substitutions=_BUILD_BUCKET=gcp-cicd-artifacts,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=$(date | md5)  \
--config cloudbuilds/cloudbuild-airflow-cicd.yaml
```
## DAGs deployment to Cloud Composer - TBD
You can deploy staged DAGs to a Cloud Composer environment by this command:
```
gcloud composer environments storage dags import \
    --environment ENVIRONMENT_NAME \
    --location LOCATION \
    --source LOCAL_FILE_TO_UPLOAD
```

## Airflow DAGs tests
### DAG Validation Tests
#### `./test/validation`
DAG validation tests are common for all the DAGs in Airflow, hence we don’t need to write a separate test for each DAG. This test will check the correctness of each DAG. It will also check whether a graph contains cycle or not. Tests will fail even if we have a typo in any DAG. 
### DAG Definition Tests 
#### `./test/definition`
It doesn’t test any processing logic, only help us to verify the pipeline definition. It includes the total number of tasks in the pipeline, the nature of the tasks, upstream and downstream dependencies of each task.
### Unit Tests
#### `./test/unit/operator`
#### `./test/unit/sensor`
In Airflow, there are many built-in operators and sensors. 
We can also add our custom operators and sensors. 
As a part of this tests, we can check the logic of our custom operators and sensors.
### Integration Tests
### End to End Pipeline Tests
It is needed to have a test environment to run Integration Tests and End to End Pipeline Test. 
The test environment should be similar to the production environment but on a small scale. 
In this environment, we run all Airflow pipelines on sample data and assert the data for each pipeline. 
It will also help to make sure that everything is working fine on an actual cluster as well.

