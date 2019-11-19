from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator
from airflow.contrib.operators.dataproc_operator import DataProcHiveOperator


from airflow.models import Variable

PROJECT_ID = 'gcp-cicd-artifacts'
REGION_ID = 'us-central1'

INPUT_BUCKET = 'gs://' + 'gcp-cicd-artifacts' + '/hive/input'
OUTPUT_BUCKET = 'gs://' + 'gcp-cicd-artifacts' + '/hive/output'

HQL_BUCKET = 'gs://' + PROJECT_ID + '/hive/hql/'
UDF_BUCKET = 'gs://' + PROJECT_ID + '/hive/udf/'
HQL_SCRIPT_NAME = 'input_tables.hql'
UDF_JAR_MANE = 'gcp-cicd-udf-1.0-SNAPSHOT.jar'

start_date = datetime(2019, 11, 18)

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

with DAG(dag_id='hive-query-submit',
         default_args=default_args,
         start_date=start_date,
         schedule_interval=None) as dag:

    # run_cluster_task = DataprocClusterCreateOperator(
    #     task_id='HiveWorkflow',
    #     project_id=PROJECT_ID,
    #     region=REGION_ID,
    #     # properties={
    #     #     'autoscalingAlgorithm': 'THROUGHPUT_BASED',
    #     #     'maxNumWorkers': '3',
    #     # }
    # )

    submit_hive_task = DataProcHiveOperator(
        task_id='HiveSubmit',
        project_id='gcp-cicd',
        cluster_name='cluster-1',
        query_uri='gs://gcp-cicd-artifacts/hive/hql/input_tables.hql',
        # dataproc_hive_jars=[UDF_BUCKET + UDF_JAR_MANE],
        # variables={'PROJECT_ID': PROJECT_ID},
        region='europe-west1'
    )

    dummy_task = DummyOperator(
        task_id='DummyTask'
    )

    # dummy_task >> run_cluster_task
    # run_cluster_task >> submit_hive_task
    dummy_task >> submit_hive_task
