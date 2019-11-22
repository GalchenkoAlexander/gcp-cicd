## Test and deploy DAGs 


To test and deploy to Composer DAG's dir execute the next command:

```
gcloud builds submit \
--substitutions=\
_COMPOSER_ENV_NAME=${COMPOSER_ENV_NAME},\
_COMPOSER_REGION=${COMPOSER_REGION},\
_SOURCE=./airflow/dags/sample-dag-hive-persistent.py \
--config=./cloudbuilds/cloudbuild-dag-import-to-composer-persistent.yaml .
```
or run `scripts/run-build-import-dags-to-composer.sh` shell script

This Cloud Build `cloudbuild-dag-import-to-composer-persistent.yaml` runs DAG tests and imports DAGs files to Airflow DAG_DIRS



 