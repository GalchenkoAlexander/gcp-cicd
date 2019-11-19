from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator
from airflow.contrib.operators.dataproc_operator import DataProcHiveOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterDeleteOperator
from airflow.utils.trigger_rule import TriggerRule


from airflow.models import Variable

PROJECT_ID = 'gcp-cicd'
REGION_ID = 'europe-west1'
ZONE = 'europe-west1-d'

HQL_BUCKET = 'gs://' + PROJECT_ID + '-artifacts/hive/hql/'
UDF_BUCKET = 'gs://' + PROJECT_ID + '-artifacts/hive/udf/'
HQL_SCRIPT_NAME = 'input_tables.hql'
UDF_JAR_MANE = 'gcp-cicd-udf-1.0-SNAPSHOT.jar'

start_date = datetime(2019, 11, 18)

CLUSTER_NAME=PROJECT_ID + '-cluster-{{ ds_nodash }}'

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': start_date,
    'email': ['airflow-monitoring@somedomain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(dag_id='hive-query-submit-ephemeral',
         default_args=default_args,
         start_date=start_date,
         schedule_interval=None) as dag:

    # Create a Cloud Dataproc cluster with one node
    create_dataproc_cluster = DataprocClusterCreateOperator(
        task_id='create_dataproc_cluster',
        project_id=PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        num_workers=0,
        region=REGION_ID,
        zone=ZONE,
        # service_account='aaa-865@gcp-cicd-259411.iam.gserviceaccount.com',
        master_machine_type='n1-standard-1')

    submit_hive_task = DataProcHiveOperator(
        task_id='hive_submit',
        project_id=PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        query_uri=HQL_BUCKET + HQL_SCRIPT_NAME,
        # dataproc_hive_jars=[UDF_BUCKET + UDF_JAR_MANE],
        # variables={'PROJECT_ID': PROJECT_ID},
        region=REGION_ID
    )

    delete_dataproc_cluster = DataprocClusterDeleteOperator (
        task_id='delete_dataproc_cluster',
        project_id=PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        trigger_rule=TriggerRule.ALL_DONE)

    create_dataproc_cluster >> submit_hive_task >> delete_dataproc_cluster

