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

.. _choosing_setup_iMD-VR_client:

Choosing your setup for the iMD-VR client
#########################################

.. note::

    VR is developing fast and there are constantly new features/apps/ways of doing things. Therefore,
    these instructions may not be an exhaustive list of all the possible VR setups. Please feel free to choose whichever
    one you are most comfortable with! We also recommend checking out the online documentation for your VR headset if you
    run into any problems relating to setting up your VR kit.


If you wish to visualise and interact with your simulations in VR, you will need to install an iMD-VR client. Below is a
flow diagram to help you decide which setup to use.

.. image::  /_static/VR_client_flow_diagram.png
  :width: 600

Using PC-VR
~~~~~~~~~~~

In this case, you have two options for running the VR client:

* **Downloading the latest release of the NanoVer iMD executable**. This is a quick and easy option for those unfamiliar with conda, see :ref:`download_latest_release_VR_client`.

* **Conda installation of the NanoVer iMD package**. This is a good option if you are familiar with conda (or want to learn how to use it!), see :ref:`conda_installation_VR_client`.

Both options are compatible with any of the following:

* Meta Quest Link (tethered\ :sup:`†`)
* Meta Quest AirLink (wireless*)
* SteamVR (tethered\ :sup:`†`)
* Steam Link (wireless*)

\ :sup:`†` **Tethered**: using a cable to connect your headset to your computer.

\* Note that for a **wireless setup** you will need to meet the **requirements for a Wi-Fi setup** (see the key in the flow
diagram above).

Running locally on a Meta Quest headset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case, you have one option:

* **Downloading the latest release of the NanoVer iMD apk** and installing this on your headset, see
  :ref:`download_latest_release_VR_client`.

Note that for a **wireless setup** you will need to meet the **requirements for a Wi-Fi setup** (see the key in the flow
diagram above).

----

.. _installing_imdvr_client:


The VR client
#############

We call an instance of the NanoVer iMD application a **VR client**.
This is different to a *python client*, which connects to a server from a python script.
This distinction is important since the two types of client offer different functionalities.
For example, *both* can connect to a NanoVer server to access simulation data & run commands
such as play/pause/reset.
However, *only a VR client* allows you to visualise & interact with a simulation in VR,
and *only a python client* allows you to change the visualisation of the molecular system.

.. admonition:: Key point

   A **VR Client** is an instance of the NanoVer iMD application.


The UI
######

There are two types of UI in the NanoVer iMD application:

.. toctree::
   :maxdepth: 1

   pcvrmenu.rst
   invrmenu.rst


.. figure:: /_static/UI_full-screen.png
    :align: center
    :width: 800px

    Screenshot of the NanoVer iMD application showing the on-screen (top left) and in-VR (center) menus.


