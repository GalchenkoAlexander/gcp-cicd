import json
import unittest

import jsonschema

from mf.config import config


# noinspection PyTypeChecker
class TestComponentBase(unittest.TestCase):

    def test_read_manifest(self):
        data = json.dumps({
            'bucket': 'a_bucket',
            'repository': 'a_repo',
            'components': {}
        })

        p = config(root=None, mf_file=data)

        self.assertEqual(p.bucket, 'a_bucket')
        self.assertEqual(p.repository, 'a_repo')

    def test_read_manifest_invalid_component_names(self):

        data = json.dumps({
            'bucket': 'a_bucket',
            'repository': 'a_repo',
            'components': {
                'invalid name': {}
            }
        })

        try:
            config(root=None, mf_file=data)
        except jsonschema.exceptions.ValidationError:
            return

        self.fail('unreachable')

    def test_read_manifest_valid_component_names(self):

        data = json.dumps({
            'bucket': 'a_bucket',
            'repository': 'a_repo',
            'components': {
                'invalid_name': {
                    'type': 'a_type',
                    'assets': []
                }
            }
        })

        p = config(root=None, mf_file=data)

        self.assertEqual(len(p.components), 1)


if __name__ == '__main__':
    unittest.main()
