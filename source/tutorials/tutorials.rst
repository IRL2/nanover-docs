.. _tutorials:

=========
Tutorials
=========

.. contents:: Contents
    :depth: 2
    :local:

----

#################
NanoVer tutorials
#################

This section provides tutorials on getting started with NanoVer.
We assume familiarity with setting up simulations in whichever
framework you're running with NanoVer. Choose from the following
sets of tutorials:

.. toctree::
   :maxdepth: 1

   basics.rst
   vrclient.rst
   fundamentals.rst
   ase.rst
   mdanalysis.rst
   openmm.rst

**Our tutorials can be used in conjunction with our iMD-VR application**,
`NanoVer iMD-VR <https://github.com/IRL2/nanover-imd-vr>`_, see the instructions for
:ref:`installing_imdvr_client`.

.. important::
    Our tutorials are provided as `Jupyter notebooks <https://jupyter.org>`_, and thus require Jupyter to run.
    Some of our notebooks also use `NGLView <https://github.com/nglviewer/nglview>`_ for visualising simulations.
    Both ``jupyterlab`` and ``nglview`` are installed automatically when you install ``nanover-server``.


|

----

.. _using_nanover_in_jupyter:

#################################
Tips for using NanoVer in Jupyter
#################################

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

|

----

###############
Further reading
###############

For more details, look at the documentation for the individual :ref:`modules <modules>`.

|
