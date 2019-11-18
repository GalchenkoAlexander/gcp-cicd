from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator
from airflow.operators.hive_operator import HiveOperator


from airflow.models import Variable

PROJECT_ID = 'gcp-cicd'
TEMPLATE_ID = 'gcp-cicd-airflow'
REGION_ID = 'us-central1'

INPUT_BUCKET = 'gs://' + 'gcp-cicd-artifacts' + '/hive/input'
OUTPUT_BUCKET = 'gs://' + 'gcp-cicd-artifacts' + '/hive/output'

HQL_BUCKET = 'gs://' + 'gcp-cicd' + '/hive/hql'

start_date = datetime(2019, 1, 1)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': start_date,
    'email': ['airflow-monitoring@somedomain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(dag_id='dataproc_workflow--hive',
         default_args=default_args,
         start_date=start_date,
         schedule_interval=None) as dag:

    run_cluster_task = DataprocClusterCreateOperator(
        task_id='HiveWorkflow',
        project_id=PROJECT_ID,
        region=REGION_ID,
        # properties={
        #     'autoscalingAlgorithm': 'THROUGHPUT_BASED',
        #     'maxNumWorkers': '3',
        # }
    )

    submit_hive_task = HiveOperator(
        task_id='HiveSubmit',
        project_id=PROJECT_ID,
        hql=HQL_BUCKET,
    )

    dummy_task = DummyOperator(
        task_id='DummyTask'
    )

    dummy_task >> run_cluster_task
    run_cluster_task >> submit_hive_task
