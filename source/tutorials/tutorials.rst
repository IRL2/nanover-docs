.. _tutorials:

Tutorials
==================================

This section provides tutorials on getting started with NanoVer.
We assume familiarity with setting up simulations in whichever 
framework you're running with NanoVer.

The tutorials use `Jupyter notebooks <https://jupyter.org>`_, `NGLView <https://github.com/nglviewer/nglview>`_ for visualising trajectories, and while not strictly necessary, assumes you have the `NanoVer IMD VR <https://gitlab.com/intangiblerealities/nanover-applications/nanover-imd>`_ application installed. These can all be installed with conda:

.. code-block:: bash

   conda activate <nanover_conda_environment_name>
   conda install jupyter
   conda install nglview
   # On Windows only:
   conda install -c irl nanover-imd

Please note that in order to use NGLView we recommend installing Jupyter notebooks using the conda command shown above: the use of JupyterLab is not advised due to `difficulties building and debugging <https://github.com/nglviewer/nglview/issues/845>`_ NGLView with JupyterLab.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   ase.rst

Further reading
---------------

For more details, look at the documentation for the individual :mod:`modules <nanover>`.
