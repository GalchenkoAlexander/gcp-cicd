There are two dataproc cluster configurations to support Application History:
- for ephemeral cluster `dataproc/history-server/cluster-templates/ephemeral-cluster.yaml`
- for history server `dataproc/history-server/cluster-templates/history-server.yaml`

These ephemeral cluster and history server have to be align by configuration like next: 
Ephemeral worker nodes of Datoproc cluster have to save event logs to a specified GCS bucket and 
History server has to read these logs from the same bucket.

When ephemeral cluster is starting it has to apply `dataproc/init-actions/disable-history-servers.sh` init-action 
script to disable its own history servers. Thi script just stop spark-history-server and hadoop-mapreduce-historyserver.

Configure clusters to use GCS for log aggregation and point at the history server execute next with substitute arguments:
```
cd ./dataproc/history-server/cluster-templates
sed -i 's/PROJECT/${PROJECT_ID}/g' *
sed -i 's/HISTORY_BUCKET/${HISTORY_BUCKET_NAME}/g' *
sed -i 's/HISTORY_SERVER/${HISTORY_SERVER_NAME}/g' *
sed -i 's/REGION/${HISTORY_REGION}/g' *
sed -i 's/ZONE/${HISTORY_ZONE}/g' *
sed -i 's/SUBNET/${HISTORY_SUBNET_ID}/g' *
```


Create the history server.
```
gcloud beta dataproc clusters import history-server \
--source=dataproc/history-server/cluster-templates/history-server.yaml \
--region=us-central1
```

Create an ephemeral cluster.
```
gcloud beta dataproc clusters import ephemeral-cluster \
--source=dataproc/history-server/cluster-templates/ephemeral-cluster.yaml \
--region=us-central1
```

#### Useful links:
https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/dataproc-persistent-history-server
https://medium.com/google-cloud/persisting-application-history-from-ephemeral-clusters-on-google-cloud-dataproc-7b1b03a49686