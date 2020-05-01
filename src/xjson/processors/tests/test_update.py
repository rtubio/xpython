import os, tempfile, unittest

from xjson import xjson
from xjson.processors import update


class TestUpdateJSON(unittest.TestCase):

    _OLD_JSON = {
        'a': 'A text',
        'b': 'B text',
        'd': 'D text'
    }

    _NEW_JSON = {
        'a': 'A text',
        'b': 'B text (new)',
        'c': 'C text'
    }

    _EXPECTED_JSON = {
        'a': 'A text',
        'b': 'B text (new)',
        'c': 'C text',
        'd': 'D text'
    }

    def setUp(self):

        oldfp = tempfile.NamedTemporaryFile(delete=False)
        newfp = tempfile.NamedTemporaryFile(delete=False)
        self._oldpath = oldfp.name
        self._newpath = newfp.name
        oldfp.close()
        newfp.close()

        xjson.dumps(self._oldpath, self._OLD_JSON)
        xjson.dumps(self._newpath, self._NEW_JSON)

        self._backuppath = None

    def tearDown(self):
        os.remove(self._oldpath)
        os.remove(self._newpath)
        if self._backuppath:
            os.remove(self._backuppath)

    def test_update(self):

        update.UpdateJSON(self._oldpath, self._newpath)
        updated = xjson.loads(self._oldpath)

        self.assertEqual(self._EXPECTED_JSON, updated)

    def test_update_and_backup(self):

        self._backuppath = self._oldpath + '.bak'
        update.UpdateJSON(self._oldpath, self._newpath, backup=True)

        updated = xjson.loads(self._oldpath)
        backup = xjson.loads(self._backuppath)

        self.assertEqual(self._EXPECTED_JSON, updated)
        self.assertEqual(self._OLD_JSON, backup)

    def test_update_cli(self):

        argv = [
            "--old", self._oldpath, "--new", self._newpath
        ]
        update.UpdateJSON.create(argv)
        updated = xjson.loads(self._oldpath)

        self.assertEqual(self._EXPECTED_JSON, updated)

    def test_update_and_backup_cli(self):

        argv = [
            "--old", self._oldpath, "--new", self._newpath, "--backup"
        ]
        obj = update.UpdateJSON.create(argv)

        updated = xjson.loads(self._oldpath)
        backup = xjson.loads(obj.backuppath)

        self.assertEqual(self._EXPECTED_JSON, updated)
        self.assertEqual(self._OLD_JSON, backup)


if __name__ == '__main__':
    unittest.main()
