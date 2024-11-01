 .. _vr-client-tutorial:

===========
NanoVer iMD
===========

You can use the `NanoVer iMD application <https://github.com/IRL2/nanover-imd>`_
to **incorporate VR into your workflow**, including:

* visualising molecular systems in VR, including real-time MD simulations, recorded trajectories, and static structures
* interacting with real-time molecular simulations using VR controllers
* joining together with others for multi-person sessions in VR

To install the NanoVer iMD application, please go to :ref:`installation`.
For help choosing your VR setup, please see :ref:`choosing_setup_iMD-VR` below.

.. contents:: Contents
    :depth: 3

----


Using NanoVer iMD
#################

We call an instance of the NanoVer iMD application an iMD-VR client, or simply a **VR client**.
This is different to a *python client*, which connects to a NanoVer server from a python script or Jupyter notebook.
This distinction is important since the two types of client offer different functionalities.
For example, *both* can connect to a NanoVer server to access simulation data, run commands
such as play/pause/reset, & apply forces to the molecule system (interactive MD).
However, *only a VR client* allows you to visualise & interact with a simulation in VR,
and *only a python client* allows you to change the visualisation of the molecular system.

.. admonition:: Key point

   A **VR Client** or **iMD-VR client** is an instance of the NanoVer iMD application that has connected to a NanoVer server.

User Interface
~~~~~~~~~~~~~~

There are two types of user interface (UI) in the NanoVer iMD application:

.. toctree::
   :maxdepth: 1

   pcvrmenu.rst
   invrmenu.rst


.. figure:: /_static/UI_full-screen.png
    :align: center
    :width: 800px

    Screenshot of the NanoVer iMD application showing the on-screen (top left) and in-VR (center) menus.


.. _choosing_setup_iMD-VR:

Choosing your setup for iMD-VR
##############################

If you wish to visualise and/or interact with your simulations in VR, you will need to use an iMD-VR client.
We focus on NanoVer iMD as the prototypical iMD-VR client, but these instructions can be generalised to any iMD-VR client,
e.g. your own custom VR application that uses the NanoverUnityPlugin.


.. note::

    VR is developing fast and there are constantly new features/apps/ways of doing things. Therefore,
    these instructions may not be an exhaustive list of all the possible VR setups. Please feel free to choose whichever
    one you are most comfortable with! We also recommend checking out the online documentation for your VR headset if you
    run into any problems relating to setting up your VR kit.

Flow diagram for choosing your VR setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below is a flow diagram to help you decide which VR setup to choose.

.. image::  /_static/VR_client_flow_diagram.png
  :width: 600


Using PC-VR
~~~~~~~~~~~

You can run PC-VR via any of the following setups:

* Meta Quest Link (tethered\ :sup:`†`)
* Meta Quest AirLink (wireless*)
* SteamVR (tethered\ :sup:`†`)
* Steam Link (wireless*)

You can use either NanoVer-iMD installation option:

* **Downloading the latest release of the NanoVer iMD executable**, see :ref:`download_latest_release_VR_client`.

* **Conda installation of the NanoVer iMD package**, see :ref:`conda_installation_VR_client`.

.. admonition:: Key point

    For a **wireless setup** you will need to have a strong and stable internet connection that allows communication over the network.
    This option is often incompatible with public / institutional networks.

.. admonition:: Key definition

    \ **Tethered**: using a cable to connect your VR headset to your computer.


Running locally on a Meta Quest headset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case, you must:

* **Download the latest release of the NanoVer iMD apk** and sideload this onto your headset, see
  :ref:`download_latest_release_VR_client`. If you wish to use your VR headset wirelessly,
  then you must meet the requirements for a wireless setup (see above).


----



