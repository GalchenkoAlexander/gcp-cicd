## Overview
    Airflow DAG that triggeres Dataproc Workflow template
## Tests
### DAG Validation Tests
#### `./test/validation`
DAG validation tests are common for all the DAGs in Airflow, hence we don’t need to write a separate test for each DAG. This test will check the correctness of each DAG. It will also check whether a graph contains cycle or not. Tests will fail even if we have a typo in any of the DAG. 
### DAG/Pipeline Definition Tests 
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
Is needed to have a test environment to run Integration Tests and End to End Pipeline Test. 
The test environment should be similar to the production environment but on a small scale. 
In this environment, we run all Airflow pipelines on sample data and assert the data for each pipeline. 
It will also help to make sure that everything is working fine on an actual cluster as well.