 .. _installation:

==============================
Installation & Getting Started
==============================

NanoVer consists of two components, the python-based libraries
for running simulations, nanover-server, and the Unity3D libraries
and applications for visualising and interacting with simulations
in VR.

* Install the server software (see below)
* Interact with molecules in VR by `downloading the VR client <https://github.com/IRL2/nanover-imd/releases/download/nightly/StandaloneWindows64.zip>`_
* Check out the :ref:`tutorials <Tutorials>`

.. contents:: Contents
    :depth: 3

~~~~

#######################
User Installation Guide
#######################

.. _creating_conda_env:

Creating a conda environment
############################

#. Install Conda through whichever program you prefer, e.g. `Miniforge <https://github.com/conda-forge/miniforge>`_
#. Open a terminal that you have conda installed in:

    * On Windows, this is Windows Powershell
    * On Mac and Linux, this is the terminal

#. Create a conda environment (here we call the environment "nanover"):

    .. code:: bash

        conda create -n nanover "python>3.11"

~~~~

Installing the server
#####################

If you have not already set up a NanoVer conda environment, please refer to :ref:`creating_conda_env`.

#. Activate your NanoVer conda environment: ``conda activate nanover``

#. Install the NanoVer packages: ``conda install -c irl -c conda-forge nanover-server``

For information on how to run NanoVer servers, check out the :ref:`tutorials <Tutorials>`.

~~~~

Setting up the iMD-VR client
############################

There are two main ways to set up the iMD-VR client:

* conda installation of the NanoVer iMD package
* downloading the latest build of the NanoVer iMD executable (necessary to facilitate running natively on
  VR headsets)

**Conda installation**

If you have not already set up a NanoVer conda environment, please refer to :ref:`creating_conda_env`.

#. Activate your NanoVer conda environment: ``conda activate nanover``

#. Install the NanoVer iMD package: ``conda install -c irl nanover-imd``

#. To start the program, run the command ``NanoverImd``

**Download the latest build**

#. Download the latest build of `NanoVer iMD <https://github.com/IRL2/nanover-imd/releases>`_

#. Extract the downloaded zip file

The next step(s) depend on the type of operating system that your VR headset uses:

* **Android (Meta Quest, etc.)**:
    * Sideload the ``NanoVerIMD.apk`` onto your device (you can use `SideQuest <https://sidequestvr.com>`_
      for this)
    * Look in the ``Unknown Sources`` section of your apps list and run NanoVer IMD

* **Windows (OpenXR / Meta Quest Link, etc.)**:
    * In the extracted directory, launch ``StandaloneWindows64.exe``. Windows will likely prompt you with
      a warning about the executable not being signed. If it happens, click on the "More info" button, then
      "Run anyway". You will also likely be prompted by the Windows firewall, allow NanoVer to access the network.

~~~~

Installing LAMMPS for NanoVer
#############################

NanoVer can interact with the `LAMMPS <https://lammps.sandia.gov/>`_ simulation engine.
If you want to use this specific feature, you need to:

* install LAMMPS with python capabilities
* install mpy4py:
            * ``conda install -c conda-forge mpi4py`` on Linux and MacOS
            * ``python -m pip install mpi4py`` on Windows.
* install nanover-lammps: ``conda install -c irl -c conda-forge nanover-lammps``.

~~~~

############################
Developer Installation Guide
############################

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
