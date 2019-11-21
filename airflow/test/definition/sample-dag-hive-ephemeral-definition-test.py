import unittest
from airflow.models import DagBag


class TestHiveEphemeralDAG(unittest.TestCase):

    def setUp(self):
        self.dagbag = DagBag()

    def test_task_count(self):
        dag_id = 'hive-query-submit-ephemeral'
        dag = self.dagbag.get_dag(dag_id)
        self.assertEqual(len(dag.tasks), 3)

    def test_contain_tasks(self):
        dag_id = 'hive-query-submit-ephemeral'
        dag = self.dagbag.get_dag(dag_id)
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(task_ids, ['create_dataproc_cluster', 'submit_hive_task', 'delete_dataproc_cluster'])

    def test_dependencies_of_create_dataproc_cluster_task(self):
        dag_id = 'hive-query-submit-ephemeral'
        dag = self.dagbag.get_dag(dag_id)
        create_dataproc_cluster_task = dag.get_task('create_dataproc_cluster')

        upstream_task_ids = list(map(lambda task: task.task_id, create_dataproc_cluster_task.upstream_list))
        self.assertListEqual(upstream_task_ids, [])

        downstream_task_ids = list(map(lambda task: task.task_id, create_dataproc_cluster_task.downstream_list))
        self.assertListEqual(downstream_task_ids, ['submit_hive_task', 'delete_dataproc_cluster'])

    def test_dependencies_of_submit_hive_task_task(self):
        dag_id = 'hive-query-submit-ephemeral'
        dag = self.dagbag.get_dag(dag_id)
        create_dataproc_cluster_task = dag.get_task('create_dataproc_cluster')

        upstream_task_ids = list(map(lambda task: task.task_id, create_dataproc_cluster_task.upstream_list))
        self.assertListEqual(upstream_task_ids, ['dummy_task'])

        downstream_task_ids = list(map(lambda task: task.task_id, create_dataproc_cluster_task.downstream_list))
        self.assertListEqual(downstream_task_ids, ['delete_dataproc_cluster'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestHiveEphemeralDAG)
unittest.TextTestRunner(verbosity=2).run(suite)