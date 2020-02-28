#!/usr/bin/env python

"""
Installs narupa if the script is run from readthedocs.

All the narupa subpackages need to be installed to build the documentation.
This script runs `compile.sh` to install them, but only if the documentation
is built by readthedocs. If not run by read the docs, we assume that
everything is installed already.
"""

import subprocess
import sys
import os

if 'READTHEDOCS' in os.environ:
    os.environ['PATH'] = ':'.join([
        os.path.dirname(sys.executable),
        os.environ['PATH'],
    ])
    os.chdir('../narupa-protocol')
    subprocess.call(['./compile.sh', '--no-edit'])
    import narupa
