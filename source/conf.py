# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import subprocess

subprocess.call([sys.executable, './install.py'])


# -- Project information -----------------------------------------------------

project = 'NanoVer'
copyright = 'University of Bristol, Intangible Realities Lab (https://www.intangiblerealitieslab.org), University of Santiago de Compostella and other contributors'
author = 'Intangible Realities Laboratory'

# The full version, including alpha/beta/rc tags
release = '2018.1.8'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage', 'sphinx.ext.autosummary']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


master_doc = 'index'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


def run_apidoc(_):
    import glob
    import os
    import shutil
    from distutils.dir_util import copy_tree

    print("Deleting temp folder")
    if os.path.exists('temp'):
        shutil.rmtree('temp')

    print("Working directory: " + os.getcwd())
    print("Copying python code")
    for directory in glob.glob('nanover-protocol/python-libraries/*/src/nanover'):
        print(directory)
        copy_tree(src=directory, dst='./temp/python-source/nanover')

    print("Running apidoc")
    ignore_paths = [
    ]

    argv = [
        "--implicit-namespaces",
        "--force",
        "--separate",
        "--module-first",
        "-o", "./source/python",
        "./temp/python-source/nanover"
    ] + ignore_paths

    try:
        # Sphinx 1.7+
        from sphinx.ext import apidoc
        apidoc.main(argv)
    except ImportError:
        # Sphinx 1.6 (and earlier)
        from sphinx import apidoc
        argv.insert(0, apidoc.__file__)
        apidoc.main(argv)


def setup(app):
    app.connect('builder-inited', run_apidoc)
