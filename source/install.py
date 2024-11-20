#!/usr/bin/env python

"""
Installs NanoVer if the script is run from readthedocs.

All the nanover subpackages need to be installed to build the documentation.
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
    os.chdir('../nanover-server-py')
    subprocess.call(['./compile.sh', '--no-edit'])
    import nanover
