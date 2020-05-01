#!/bin/bash

source "conf/project.conf"

virtualenv --python "$PYENV_PYTHON_VER" "$PYENV_D"

sudo apt-get install $(grep -vE "^\s*#" $DEBIAN_PKGS  | tr "\n" " ")

source "$PYENV_ACTIVATE"
pip install -r "$PYENV_PKGS"
deactivate
