 .. _installation:

Installation & Getting Started
==============================

NanoVer consists of two components, the python-based libraries
for running simulations, nanover-server, and the Unity3D libraries
and applications for visualising and interacting with simulations
in VR.

* Install the server software (see below)
* Interact with molecules in VR by `downloading the VR client <https://github.com/IRL2/nanover-imd/releases/download/nightly/StandaloneWindows64.zip>`_
* Check out the :ref:`tutorials <Tutorials>`

#####################
Installing the Server
#####################

Conda Installation
##################

* Install Anaconda
* Open the "Anaconda Powershell Prompt" to type the following commands.
* Create a conda environment (here we call the environment "nanover"): ``conda create -n nanover "python>3.11"``
* Activate the conda environment: ``conda activate nanover``
* Install the NanoVer packages:

.. code:: bash

    conda install -c irl -c conda-forge nanover-server

NanoVer can interact with the `LAMMPS <https://lammps.sandia.gov/>`_ simulation engine.
If you want to use this specific feature, you need to:

* install LAMMPS with python capabilities
* install mpy4py:
            * ``conda install -c conda-forge mpi4py`` on Linux and MacOS
            * ``python -m pip install mpi4py`` on Windows.
* install nanover-lammps: ``conda install -c irl -c conda-forge nanover-lammps``.

Installing from source
######################

Developers will want the manual install from source, follow the instructions on the README
of the `code repository <https://github.com/IRL2/nanover-protocol>`_.


#########################################
Installing the NanoVer Unity3D libraries.
#########################################

The NanoVer libraries for building your own VR applications in Unity3D are available `as NanoverUnityPlugin on GitHub <https://github.com/IRL2/NanoverUnityPlugin>`_.

######################
Installing NanoVer iMD
######################

Instructions for downloading and running the NanoVer iMD Unity3D application are available `as nanover-imd on GitHub <https://github.com/IRL2/nanover-imd>`_.
