#!/bin/bash
#
# This script freezes the current packages installed for the Python virtual environment,
# removing the following ones:
#
#     pkg-resources
#
# @author: rtpardavila@gmail.com

source "conf/project.conf"

source "$PYENV_ACTIVATE"
pip freeze | grep -v 'pkg-resources' | tee "$PYENV_PKGS"
deactivate
