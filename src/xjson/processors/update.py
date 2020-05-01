"""
This module contains a JSON processor for updating the contents of one JSON object,
with the contents of the second one.
"""

import argparse, shutil, sys

from common import files, logger
from xjson import xjson


class UpdateJSON(logger.LoggingClass):
    """Class for the JSON update processor."""

    def __init__(
        self,
        oldpath, newpath,
        schemapath=None,
        backup=False, backuppath=None, backup_extension='.bak'
    ):
        """
        Constructor.

        oldpath : path to the 'old' (to be updated) JSON file
        newpath : path to the 'new' (to be used to update the old file) JSON file
        schemapath=None : schema to validate both files (OPTIONAL)
        backup=False : flag that marks whether a backup of the old file is required
        backuppath=None : path to the backup file
        backup_extension='.bak' : extension to be appended to the old file (DEFAULT)
        """
        super(UpdateJSON, self).__init__()

        old = xjson.loads(oldpath, schemapath=schemapath)
        new = xjson.loads(newpath, schemapath=schemapath)

        old.update(new)

        if backup:
            if not backuppath:
                self.backuppath = oldpath + backup_extension
            else:
                self.backuppath = backuppath
            shutil.copy(oldpath, self.backuppath)

        xjson.dumps(oldpath, old)

    @staticmethod
    def create(argv):
        # Basic class static factory method.

        parser = argparse.ArgumentParser(description="Updates old JSON file with new JSON file")
        parser.add_argument(
            "-o", "--old",
            type=files.is_writable_file, metavar="FILE", required=True,
            help="Path to the old JSON file to be updated"
        )
        parser.add_argument(
            "-n", "--new",
            type=files.is_writable_file, metavar="FILE", required=True,
            help="Path to the new JSON file to use to update the old one"
        )
        parser.add_argument(
            "-b", "--backup",
            default=False, action="store_true", required=False,
            help="Enables creating a backup of the old file"
        )
        args = parser.parse_args(argv)
        return UpdateJSON(args.old, args.new, backup=args.backup)


if __name__ == "__main__":
    config = UpdateJSON.create(sys.argv[1:])
