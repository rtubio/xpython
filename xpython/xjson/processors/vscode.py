import argparse, json, sys

from common import files


CALL_HELP = 'vscode_c_cpp_properties.py -i <inputfile>'


class VSCodeCPPConfiguration():

    forcedInclude_key = 'forcedIncluded'
    forcedInclude_replacement = [
        "/usr/share/arduino/hardware/arduino/cores/arduino/Arduino.h"
    ]

    includePath_key = 'includePath'
    includePath_replacement = [
        "/home/rtubio/.arduino/sketch/libraries/**",
        "/usr/share/arduino/libraries/**",
        "/usr/share/arduino/tools/**",
        "/usr/share/arduino/hardware/tools/**",
        "/usr/share/arduino/hardware/tools/avr/**",
        "/usr/share/arduino/hardware/arduino/cores/arduino/**",
        "${workspaceFolder}/**"
    ]

    defines_key = 'defines'
    defines_replacement = ["USBCON"]

    def _mod_matching_configurations(self, matching_key, replacement_value):
        matching_cfgs = [
            c['name'] for c in self.configuration['configurations'] if matching_key in c
        ]
        for c in self.configuration['configurations']:
            if c['name'] in matching_cfgs:
                c[matching_key] = replacement_value

    def _mod_defines(self):
        self._mod_matching_configurations(
            self.includePath_key, self.includePath_replacement
        )

    def _mod_includePath(self):
        self._mod_matching_configurations(
            self.defines_key, self.defines_replacement
        )

    def _mod_forcedIncluded(self):
        self._mod_matching_configurations(
            self.forcedInclude_key, self.forcedInclude_replacement
        )

    def _mod_configuration(self):
        self._mod_includePath()
        self._mod_forcedIncluded()

    def _load_configuration(self):
        with open(self.path, 'r') as f:
            self.configuration = json.load(f)

    def _save_configuration(self):
        with open(self.path, 'w') as f:
            json.dump(self.configuration, f, indent=2)

    def __init__(self, path):
        # Basic constructor, loads the configuration, modifies it and saves it
        self.path = path

        self._load_configuration()
        self._mod_configuration()
        self._save_configuration()

    @staticmethod
    def create(argv):
        # Basic class static factory method.

        parser = argparse.ArgumentParser(description="Modifies VS Code's CPP Configuration")
        parser.add_argument(
            "-j", "--jsonfile",
            type=files.is_writable_file, metavar="FILE", required=True,
            help="Path to the JSON file with VS code CPP configuration"
        )
        args = parser.parse_args()
        return VSCodeCPPConfiguration(args.jsonfile)


if __name__ == "__main__":
    config = VSCodeCPPConfiguration.create(sys.argv[1:])
