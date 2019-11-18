"""
DAG describing Hive pipeline
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.dataproc_operator import DataprocWorkflowTemplateInstantiateInlineOperator

from airflow.models import Variable


SPARK_JAR = Variable.get("spark__mainJarFileUri")
SPARK_MAIN_CLASS = 'com.sparkexamples.SparkPi'



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

with DAG(dag_id='dataproc_workflow--spark',
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
                        "mainJarFileUri": str(SPARK_JAR),
                        "mainClass": str(SPARK_MAIN_CLASS),
                        "args": []
                    },
                    "stepId": "1_run-job"
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

    task_1
