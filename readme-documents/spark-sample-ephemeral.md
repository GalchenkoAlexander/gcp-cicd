
## Sample CI/CD pipeline for running Spark job on ephemeral cluster

Spark builds based on sbt. For triggering from shell several git specific substitutions are required.
Current sample build spark application and publish it into specific gs folder.

After build success, specified
cloud composer environment's variable will be updated with newly assembled jar file.

Run build with this command:
```
gcloud builds submit \
--substitutions=_BUILD_BUCKET=builds-2,REPO_NAME=gcp-cicd,BRANCH_NAME=master,SHORT_SHA=$(date | md5)  \
--config cloudbuilds/cloudbuild-spark-ephimeral.yaml .
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
  --source airflow/dags/sample-dag-spark-ephimeral.py
```


with

```
gcloud composer environments run gcp-test-3 \
--location us-central1 variables -- \
--set spark__mainJarFileUri gs://builds-2/gcp-cicd/master/43124321/spark/app.jar

```

### CI

Build is based on sbt tool. For speedup make  sense to save build tools cache directories.
More optimal way will be a bash script that zip-and-store folders on GS after the main steps and "vice versa" before run.

For dependencies management sbt uses sbt-assembly plugin (that creats uber jar with shaded dependencies).
