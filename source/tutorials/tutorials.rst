.. _tutorials:

Tutorials
==================================

This section provides tutorials on getting started with NanoVer.
We assume familiarity with setting up simulations in whichever 
framework you're running with NanoVer.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   basics.rst
   fundamentals.rst
   openmm.rst
   ase.rst
   mdanalysis.rst
   vrclient.rst

Many of the tutorials for NanoVer are written as `Jupyter notebooks <https://jupyter.org>`_, and thus require that you
have Jupyter installed in your NanoVer conda environment (see the :ref:`installation instructions <installing_jupyter>`
below).

For useful tips on how to explore the functionality of NanoVer in Jupyter notebooks, please refer to the
:ref:`Tips for using NanoVer in Jupyter <using_nanover_in_jupyter>` section below.

.. _installing_jupyter:

Installing Jupyter
------------------

The tutorials use `Jupyter notebooks <https://jupyter.org>`_, `NGLView <https://github.com/nglviewer/nglview>`_ for
visualising trajectories, and, while not strictly necessary, assumes you have the
`NanoVer iMD-VR <https://github.com/IRL2/nanover-imd-vr>`_ application installed (see :ref:`installing_imdvr_client`).
Install Jupyter notebooks and NGLView with conda:

.. code-block:: bash

   # Assuming NanoVer is installed in a conda environment named "nanover",
   # change the name otherwise.
   conda activate nanover
   conda install jupyter
   conda install nglview

If you wish to access the Jupyter notebooks via `JupyterLab <https://jupyter.org>`_, installing JupyterLab
**before** NGLView should install the correct dependencies for NGLView automatically (i.e. replacing
``conda install jupyter`` with ``conda install jupyterlab`` in the installation instructions above).
If JupyterLab is installed outside of your conda environment, you will need to install
`ipywidgets <https://ipywidgets.readthedocs.io/en/stable/>`_ in your NanoVer conda environment following
`these instructions <https://ipywidgets.readthedocs.io/en/latest/user_install.html#installing-in-jupyterlab-3-x>`_.

.. _using_nanover_in_jupyter:

Tips for using NanoVer in Jupyter
---------------------------------

NanoVer provides a set of libraries that define a range of objects (classes, functions, etc.) that can be used to
perform interactive molecular dynamics simulations. The Jupyter notebook interface provides useful tools to navigate
these libraries and their functionality, making it easier to find the resources you need without
digging through the documentation.

.. image:: /_static/jupyter_tips_screen_recording.gif
    :alt: Explore NanoVer objects using Jupyter notebooks.
    :align: center
    :scale: 100%

\

The GIF above demonstrates how to use Jupyter to explore and understand objects in NanoVer:

* Use |Tab| (the `Tab` key) mid-way through typing to list options such as available functions within a class and select
  the desired option for autocompletion:

  e.g. selecting the :func:`OpenMMSimulation.from_xml_path` function for importing simulation files
* Use |Tab| to list the functionality of objects:

  e.g. pressing |Tab| after typing ``example_sim.`` to see the functionality associated with this instance
* Use the :func:`help` function to get information about objects, which can be used on

    * Instances of objects (e.g. ``example_sim``)

    * The objects themselves (e.g. ``OpenMMSimulation``)

Both |Tab| and :func:`help` provide useful information about the objects and their functionality. When using |Tab|, the
object's type is displayed next to it, making it easy to tell which functions, instances etc. are available to
a particular object.
The :func:`help` function prints the docstrings associated with the object, which can also be found in the
:ref:`modules <modules>` section of this documentation.

.. |Tab| unicode:: U+21E5

Further reading
---------------

For more details, look at the documentation for the individual :ref:`modules <modules>`.
