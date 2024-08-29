====================
NanoVer Fundamentals
====================

.. contents:: Contents
    :depth: 2
    :local:

Jupyter notebook tutorials
==========================

We provide a set of Jupyter notebook tutorials that introduce NanoVer as a framework for performing interactive
molecular dynamics simulations, and the fundamental concepts associated with the client-server
architecture that NanoVer uses. These tutorials can be used in conjunction with the
information in :ref:`concepts <Concepts>` to understand how NanoVer works and are found in the
`examples <https://github.com/IRL2/nanover-protocol/tree/main/examples/fundamentals>`_ folder of the GitHub repository.

Here we give a summary of each tutorial:

* `getting_started`: **New to NanoVer? Start here!** An introductory notebook that showcases how
  NanoVer can be used to run an interactive molecular dynamics (iMD) simulation for a
  pre-prepared methane & nanotube system.
* `frame`: A notebook that introduces the concept of the **frame**, the object sent by
  the NanoVer server to the client that contains data associated with the molecular system.
* `servers`: A notebook that introduces the concept of the **NanoVer server**, and
  explains its role within the client-server architecture of NanoVer.
* `commands_and_state`: A notebook that introduces the concepts of **commands**, and explains
  how NanoVer achieves synchronised multi-user interactive molecular simulations via the
  **shared state** dictionary.
* `visualisations`: A notebook that demonstrates how to change the **visualisation** of the
  interactive molecular simulation within the NanoVer iMD VR client.


Running a server
================

There are two NanoVer servers available:

* **The primary NanoVer server**, found in the `nanover-protocol <https://github.com/IRL2/nanover-protocol>`_ git repo.
  This server is written in python and is the go-to server for NanoVer users.
* The Rust Server, found in the `nanover-rs <https://github.com/IRL2/nanover-rs>`_ git repo, and is written
  in Rust. We include brief instructions for using this server on this page, but we recommend using the Python Server.

Nanover Protocol
~~~~~~~~~~~~~~~~

The NanoVer protocol package can be installed using conda (see :ref:`user_installation_guide`) or using the source code
(see :ref:`developer_installation_guide`). Once installed, you can run a NanoVer server using either
(a) a python script or Jupyter notebook
or (b) the command line.

via a python script or notebook
###############################

For running a NanoVer server using a python script or Jupyter notebook, please see our :ref:`tutorials` page.
If you are new to NanoVer, we recommend starting with our
`getting_started notebook <https://github.com/IRL2/nanover-protocol/blob/main/examples/fundamentals/getting_started.ipynb>`_.

via the command line
####################

Once you have the ``nanover-server`` package installed in your conda environment, you will be able to use the
``nanover-omni`` command to run a server.
This server can take any of the following:

* An OpenMM NanoVer simulation
* An OpenMM NanoVer simulation with ASE as an interface
* A NanoVer recording, with either or both of the trajectory and shared state recording files

Note that you can give the simulations/recordings either explicitly as a string
or simply by typing the file path.
Here are some example commands:

.. code-block:: bash

    # load a single NanoVer OpenMM simulation
    nanover-omni --omm "my-openmm-sim.xml"

    # load multiple simulations
    nanover-omni --omm "my-openmm-sim-1.xml" "my-openmm-sim-2.xml" --omm-ase "my-ase-omm-sim.xml"

    # load a NanoVer recording
    nanover-omni --playback "my-recording.state" "my-recording.traj"

For more information about the arguments provided with this command, type:

.. code-block:: bash

    nanover-omni --help


The Rust Server
~~~~~~~~~~~~~~~

The Rust Server is compiled into an executable (or equivalent, depending on your operating system), rather than being
installed on your computer. For this, you have two options:

* Download the `latest release <https://github.com/IRL2/nanover-rs/releases>`_ from the git repo, ensuring you choose
  the correct option for your operating system.
* Compile it yourself using the source code by following the instructions in the
  `README <https://github.com/IRL2/nanover-rs>`_.

This program can run OpenMM NanoVer simulations and NanoVer recordings (but not simulations that use ASE as
an interface) and has many features, including:

* Recording NanoVer sessions
* Loading multiple simulations and/or recordings onto a single server, and switching between them while the
  server is running
* A graphical user interface (GUI), useful for new users to familiarise themselves quickly and easily with the various
  options offered by NanoVer

To **run the server**, first, navigate to the build directory:

* If you have downloaded the latest release, extract the files from the zip folder and navigate to the build directory:
  this directory will be named ``{operating_sys}-build`` (e.g. ``windows-build``).
* If instead you have compiled from source, navigate to the build directory (e.g. ``cd {path_to_repo}/target/release``
  on MacOS).

Here you are provided with two executables for running a server:

* An executable for running via the command line (e.g. ``nanover-cli.exe`` on Windows)
* An executable for running via the GUI (e.g. ``nanover-gui.exe`` on Windows)

.. warning::
    On MacOS, the first time you run either ``nanover-cli`` or ``nanover-gui`` from a downloaded release, it
    is necessary to open the executables manually by

    #. Opening the build directory in Finder
    #. Right-clicking the executables and selecting ``Open``
    #. When prompted, click ``Open``

    The same needs to be done for the ``libOpenMM`` executables in the ``lib`` and ``lib/plugins`` directories.

via the command line
####################

To run the server using the command line, run the executable as a command, passing it the path to
your NanoVer simulation file, e.g.:

.. code-block::

    # Windows Powershell
    .\nanover-cli.exe "my-openmm-sim.xml"

    # MacOS/Linux
    ./nanover-cli "my-openmm-sim.xml"

    # if you are not in the same directory as this executable, you will need to give the entire file path
    # e.g. for Windows Powershell
    .\path\to\build\directory\nanover-cli.exe "my-openmm-sim.xml"

The server can serve multiple simulations: just pass it multiple input files.

.. code-block::

    # load several simulations onto the server by passing multiple simulation files, e.g. Windows Powershell
    .\nanover-cli.exe "my-openmm-sim-1.xml" "my-openmm-sim-2.xml"


.. _command line help:

For more information about the arguments provided with this command, type:

.. code-block::

    # Windows Powershell
    .\nanover-cli.exe --help

    # MacOS/Linux
    ./nanover-cli --help


.. _rust_server_via_the_gui:

via the GUI
###########

To run the server via the GUI, open the ``nanover-gui`` executable (or run it via the command line e.g.
``./nanover-gui`` on MacOS) and you will see the following interface:

.. image:: /_static/nanover-rs-gui.png
    :align: center
    :scale: 50%

|

Simply click ``Run demonstration input!`` to run a demo simulation. Alternatively, click ``+OpenMM`` and select your
own OpenMM NanoVer simulation file, then click ``Run!`` to start the server. You can also add NanoVer recordings by
clicking ``+Recording`` and selecting your trajectory (.traj) and shared state (.state) files.

Please click on the headings to open up menus to customise your server further: ``Verbosity``, ``Network``,
``Simulation``, and ``Recording``.
For further information about these options, use the :ref:`help function <command line help>` in the command line.
