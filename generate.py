import glob
import os
import shutil
from distutils.dir_util import copy_tree

if os.path.exists('temp'):
    shutil.rmtree('temp')

for directory in glob.glob('nanover-protocol/python-libraries/*/src/nanover'):
    print(directory)
    copy_tree(src=directory, dst='temp/python-source/nanover')


# sphinx-apidoc -o source/python temp/python-source/nanover --implicit-namespaces --force --separate --module-first
