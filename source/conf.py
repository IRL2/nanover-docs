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
import sys
import subprocess
from datetime import datetime
from pytz import timezone

subprocess.call([sys.executable, './install.py'])

# -- Project information -----------------------------------------------------

timezone = timezone('UTC')
release = datetime.now(timezone).strftime("%d-%m-%Y")
full_release_date = datetime.now(timezone).strftime("%a, %d %b %Y %H:%M:%S")

copyright = (f'{datetime.now().year}, Intangible Realities Lab | University of Santiago de Compostela | University of '
             f'Bristol | and other contributors. Last updated on {full_release_date} UTC')

author = 'Intangible Realities Laboratory'

# Set the version based on the commit count (how nanover-server-py currently does it)
def get_git_commit_count(repo_path="."):
    """
    Get the number of commits in nanover-server-py submodule to calculate the version.
    """
    try:
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error calculating commit count: {e}")
        return "unknown"

base_version = "0.1"
commit_count = get_git_commit_count("../nanover-server-py")
version = f"{base_version}.{commit_count}" if commit_count != "unknown" else base_version

project = f'NanoVer {version}'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage', 'sphinx.ext.autosummary', 'sphinx_copybutton',
              'sphinx_design', 'sphinxcontrib.video']

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

html_theme = 'sphinx_rtd_theme'

html_title = f"NanoVer {version} documentation"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['custom.css']

html_meta = {"description": "Documentation for the NanoVer application",
             "keywords": "nanover, imd, virtual reality, vr, molecular simulation,"
                         "documentation, imd-vr, intangible realities lab, irl,"
                         "interactive molecular dynamics, molecular dynamics"}

html_context = {
    'favicon': '_static/favicon-32x32.ico',
    'favicon_32': '_static/favicon-32x32.png',
    'favicon_16': '_static/favicon-16x16.png',
    'apple_touch_icon': '_static/favicon.png',
    'safari_pinned_tab': '_static/favicon.svg',
    'version': version,
}

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
    for directory in glob.glob('nanover-server-py/python-libraries/*/src/nanover'):
        print(directory)
        copy_tree(src=directory, dst='./temp/python-source/nanover')

    print("Running apidoc")
    ignore_paths = [
    ]

    argv = [
        "--implicit-namespaces",
        "--force",
        "--separate",
        "--no-toc",
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
    app.add_js_file('custom.js')
    app.add_css_file('custom.css')
