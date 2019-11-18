# notes

# 1 node dataproc
```
gcloud dataproc clusters create gal-hadoop-udf \
  --project gal-wm-test \
  --region us-central1 \
  --zone us-central1-a \
  --initialization-actions 'gs://hive-init-action/add_hive_jars.sh' \
  --metadata hive-aux-libs=gs://hive-aux-libs/ \
  --subnet default \
  --single-node \
  --master-machine-type n1-standard-1 \
  --master-boot-disk-size 500 \
  --image-version 1.4-debian9
```
# Airflow

upload dag

gcloud composer environments storage dags import \
  --environment composer-env-name  \
  --location us-central1 \
  --source test-dags/quickstart.py
