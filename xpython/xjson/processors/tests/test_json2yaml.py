import os, tempfile, unittest, yaml

from xjson import xjson
from xjson.processors import json2yaml


class TestJSON2YAML(unittest.TestCase):

    _JSON_TEST_1 = {
        'object-a': {
            'subobject-a': {'key1': 'value1', 'key2': 'value2'}
        },
        'object-empty': {},
        'array': [
            'list-element-1', 'list-element-2', 'list-element-3'
        ]
    }

    def setUp(self):
        jsonfp = tempfile.NamedTemporaryFile(delete=False)
        self._json_path = jsonfp.name + '.json'
        jsonfp.close()

        xjson.dumps(self._json_path, self._JSON_TEST_1)

    def tearDown(self):
        os.remove(self._json_path)
        if hasattr(self, '_yaml_path') and self._yaml_path:
            os.remove(self._yaml_path)

    def test_convert(self):

        test_object = json2yaml.JSON2YAML(self._json_path)

        with open(test_object.yfile_path) as f:
            yml_recovered = yaml.load(f, Loader=yaml.FullLoader)
        self.assertEqual(self._JSON_TEST_1, yml_recovered)

    def test_convert_cli(self):

        argv = ["--json", self._json_path]
        test_object = json2yaml.JSON2YAML.create(argv)

        with open(test_object.yfile_path) as f:
            yml_recovered = yaml.load(f, Loader=yaml.FullLoader)
        self.assertEqual(self._JSON_TEST_1, yml_recovered)

    def test_convert_cli_yaml(self):

        yamlfp = tempfile.NamedTemporaryFile(delete=False)
        self._yaml_path = yamlfp.name
        yamlfp.close()

        argv = ["--json", self._json_path, "--yaml", self._yaml_path]

        test_object = json2yaml.JSON2YAML.create(argv)

        with open(test_object.yfile_path) as f:
            yml_recovered = yaml.load(f, Loader=yaml.FullLoader)
        self.assertEqual(self._JSON_TEST_1, yml_recovered)
