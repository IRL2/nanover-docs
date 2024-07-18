.. _tutorials:

Tutorials
==================================

This section provides tutorials on getting started with NanoVer.
We assume familiarity with setting up simulations in whichever 
framework you're running with NanoVer.

The tutorials use `Jupyter notebooks <https://jupyter.org>`_, `NGLView <https://github.com/nglviewer/nglview>`_ for visualising trajectories, and while not strictly necessary, assumes you have the `NanoVer IMD <https://github.com/irl2/nanover-imd>`_ application installed (i.e. the VR client). These can all be installed with conda:

.. code-block:: bash

   # Assuming NanoVer is installed in a conda environment named "nanover",
   # change the name otherwise.
   conda activate nanover
   conda install jupyter
   conda install nglview
   # On Windows only:
   conda install -c irl nanover-imd

If you wish to access the Jupyter notebooks via `JupyterLab <https://jupyter.org>`_, installing JupyterLab **before** NGLView should install the correct dependencies for NGLView automatically (i.e. replacing ``conda install jupyter`` with ``conda install jupyterlab`` in the installation instructions above). If JupyterLab is installed outside of your conda environment, you will need to install `ipywidgets <https://ipywidgets.readthedocs.io/en/stable/>`_ in your NanoVer conda environment following  `these instructions <https://ipywidgets.readthedocs.io/en/latest/user_install.html#installing-in-jupyterlab-3-x>`_. 

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   fundamentals.rst
   openmm.rst
   ase.rst
   lammps.rst
   mdanalysis.rst

Further reading
---------------

For more details, look at the documentation for the individual :mod:`modules <nanover>`.
