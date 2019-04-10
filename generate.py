import glob
import os
import shutil
from distutils.dir_util import copy_tree

if os.path.exists('temp'):
    shutil.rmtree('temp')

for directory in glob.glob('../narupa-protocol/python-libraries/*/src/narupa'):
    print(directory)
    copy_tree(src=directory, dst='temp/python-source/narupa')


#sphinx-apidoc -o source/python temp/python-source/narupa --implicit-namespaces --force --separate --module-first
