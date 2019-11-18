"""
DAG describing Hive pipeline
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.dataproc_operator import DataprocWorkflowTemplateInstantiateInlineOperator

PROJECT_ID = 'wmt-data-search'
TEMPLATE_ID = 'wlt-demo-wf'
REGION_ID = 'us-central1'

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

with DAG(dag_id='simple_dataproc_workflow--spark',
         default_args=default_args,
         start_date=start_date,
         schedule_interval=None) as dag:

    task_2 = DataprocWorkflowTemplateInstantiateInlineOperator(
        task_id='RunWorkflow',
        project_id=PROJECT_ID,
        region=REGION_ID,
        template={
            "jobs": [
                {
                    "sparkJob": {
                        "mainJarFileUri": f"TODO",
                        "mainClass": "TODO",
                        "args": []
                    },
                    "stepId": "1_load-data-job"
                }
            ],
            "placement": {
                "managedCluster": {
                    "clusterName": "two-node-cluster",
                    "config": {
                        "gceClusterConfig": {
                            "zoneUri": "us-central1-f"
                        },
                        "masterConfig": {
                            "diskConfig": {
                                "bootDiskSizeGb": 250
                            },
                            "machineTypeUri": "n1-standard-2"
                        },
                        "softwareConfig": {
                            "imageVersion": "1.4-deb9"
                        },
                        "workerConfig": {
                            "diskConfig": {
                                "bootDiskSizeGb": 250
                            },
                            "machineTypeUri": "n1-standard-2",
                            "numInstances": 2
                        }
                    }
                }
            }
        }
    )

    task_1 = DummyOperator(
        task_id='DummyTask'
    )

    task_1 >> task_2