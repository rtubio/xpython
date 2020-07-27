import argparse, io, json, yaml

from common import files, logger
from xjson import xjson


class JSON2YAML(logger.LoggingClass):
    """
    This class tansforms a JSON file into a YAML file.
    """

    def __init__(self, jfile_path, yfile_path=None):
        """
        Default constructor

        jfile_path - string with the path to the JSON input file
        yfile_path=None - string with the path to the YAML output file. If none is given, a default path is built
                            by replacing JSON's extension to YAML's.
        """
        super(JSON2YAML, self).__init__()

        if not yfile_path:
            yfile_path = jfile_path.replace('.json', '.yml')

        self.jfile_path = jfile_path
        self.yfile_path = yfile_path

        self._l.debug(f"Converting JSON <{self.jfile_path}> to YAML <{self.yfile_path}>")

        self._convert()

    def _convert(self):
        """This method converts the loaded JSON file into a YAML file."""

        json_data = xjson.loads(self.jfile_path)

        with io.open(self.yfile_path, 'w', encoding='utf8') as f:
            yaml.dump(json_data, f, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def create(argv):
        # Basic class static factory method.

        parser = argparse.ArgumentParser(description="Converts the given JSON file in a YAML file")
        parser.add_argument(
            "-j", "--json",
            type=files.is_readable_file, metavar="FILE", required=True,
            help="Path to the input JSON file"
        )
        parser.add_argument(
            "-y", "--yaml",
            type=files.is_parent_dir_writable, metavar="FILE", required=False,
            help="Path to the new YAML file to be created"
        )
        args = parser.parse_args(argv)
        return JSON2YAML(args.json, yfile_path=args.yaml)


if __name__ == "__main__":
    config = UpdateJSON.create(sys.argv[1:])
