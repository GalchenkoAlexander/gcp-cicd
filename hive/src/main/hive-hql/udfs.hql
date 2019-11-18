CREATE FUNCTION txt_to_lower AS 'com.udf.LowerTextUdf'
USING JAR 'gs://gcp-cicd-artifacts/hive/jars/gcp-cicd-udf-1.0-SNAPSHOT.jar';

CREATE FUNCTION txt_to_upper AS 'com.udf.UpperTextUdf'
USING JAR 'gs://gcp-cicd-artifacts/hive/jars/gcp-cicd-udf-1.0-SNAPSHOT.jar';
