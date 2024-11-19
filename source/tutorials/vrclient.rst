 .. _vr-client-tutorial:

===========
NanoVer iMD
===========

You can use the `NanoVer iMD application <https://github.com/IRL2/nanover-imd>`_
to **incorporate VR into your workflow**, including:

* visualising molecular systems in VR, including real-time MD simulations, recorded trajectories, and static structures
* interacting with real-time molecular simulations using VR controllers
* joining together with others for multi-person sessions in VR

To install the NanoVer iMD application, go to :ref:`installation`.
For help choosing your VR setup, see :ref:`choosing_setup_iMD-VR`.
For guidance on using the NanoVer iMD application, see :ref:`navigatingnanoverinvr`.

.. contents:: Contents
    :depth: 2
    :local:

----

.. _navigatingnanoverinvr:

########################
Navigating NanoVer in VR
########################

Introduction
############

We call an instance of the NanoVer iMD application an iMD-VR client, or simply a **VR client**.
This is different to a *python client*, which connects to a NanoVer server from a python script or Jupyter notebook.
This distinction is important since the two types of client offer different functionalities.
For example, *both* can connect to a NanoVer server to access simulation data, run commands
such as play/pause/reset, & apply forces to the molecule system (interactive MD).
However, *only a VR client* allows you to visualise & interact with a simulation in VR,
and *only a python client* allows you to change the visualisation of the molecular system.

.. admonition:: Key point

   A **VR Client** or **iMD-VR client** is an instance of the NanoVer iMD application that has connected to a NanoVer server.

|

Your VR controllers
~~~~~~~~~~~~~~~~~~~

Below are diagrams showing the positions of the VR controller buttons that you will use in NanoVer iMD,
using the Meta Quest 2 controllers for demonstration.
These buttons are in similar positions on most common VR controllers,
but please refer to your VR headset's documentation if you cannot locate them.

.. important::
    To press a button on a menu in VR,
    **place the end of your controller on the button and click the trigger**.

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. figure:: /_static/left-controller_trigger.png
         :align: center
         :width: 300px

     - **Trigger button**

   * - .. figure:: /_static/left-controller_grip.png
         :align: center
         :width: 300px

     - **Grip button**

   * - .. figure:: /_static/left-controller_joystick.png
         :align: center
         :width: 300px

     - **Joystick**

|

----

A typical iMD-VR workflow
#########################

You should now have NanoVer iMD and your VR setup ready to go! To begin, follow these steps:

#. **Start your NanoVer server** (see :ref:`basicsrunningaserver`)

#. **Setup your VR kit & open NanoVer iMD** (see :ref:`installing_imdvr_client`)

#. **Select your option for connecting to a Server**: using either the
   :ref:`in-VR main menu<vrclientinvrmenumainmenu>` or
   :ref:`desktop main menu<vrclientdesktopmenu>` (PC-VR only)

#. **Check out your molecular simulation in VR!** See instructions for the
   :ref:`VR controls and menus<vrclientvrcontrolsandmenus>`, or check out the :ref:`tutorials <Tutorials>` page for
   examples of how to integrate NanoVer iMD into your workflow

|

----

Connecting to a NanoVer server
##############################

You have several options for connecting to a NanoVer server:

* **Autoconnect**: connect to the first server (using the default port) found on the network
* **Discover**: find all servers (using the default port) on the network and list them for the user to choose from
* **Manual**: allow the user to specify the IP address and port of the server they wish to connect to and then, if found, connect to it

|

.. _vrclientinvrmenumainmenu:

In-VR main menu
~~~~~~~~~~~~~~~

.. grid:: 2
   :gutter: 2

   .. grid-item::

      .. figure:: /_static/in-vr_main-menu.png
         :align: center
         :width: 85%

   .. grid-item::

        .. important::
            To press a button on the in-VR main menu,
            **place the end of your right controller** on the button and **click the trigger**.


Select from the dropdown options below to see the **video tutorials**:

.. dropdown:: Autoconnect

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_autoconnect.mp4
             :width: 250
             :height: 250

         - Click ``Autoconnect``. If a server was found, the menu will close and you will see your simulation.


.. dropdown:: Discover

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_discover.mp4
             :width: 250
             :height: 250

         - Click ``Discover`` to show a list of available servers. Click your chosen server or click ``Refresh`` to
           search again.


.. dropdown:: Manual

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_manual.mp4
             :width: 250
             :height: 250

         - Click ``Manual``, then type your IP address & port and click ``Connect``.
           If a server was found, the menu will close and you will see your simulation.

|

.. _vrclientdesktopmenu:

Desktop main menu (PC-VR only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you open the NanoVer iMD application on your PC, you will see a small menu on the top left of your monitor with the
below headings.
In **Server**, you can connect to your NanoVer server.
Select from the dropdown options below for further information and to browse other features:

.. dropdown:: Server

    .. image:: /_static/UI_server.png
        :align: left
        :scale: 45%

    +----------------------+---------------------------------------------------------------------------------------------+
    | **Autoconnect**      | Connect to the first server found on the network, using the default parameters.             |
    +----------------------+---------------------------------------------------------------------------------------------+
    | **Direct Connect**   | Toggle a menu where you can change the IP address and trajectory/multiplayer ports          |
    |                      | of the server you wish to connect to.                                                       |
    +----------------------+---------------------------------------------------------------------------------------------+
    | **Discover Services**| Toggle a menu to search for servers running on the network. Click "Search" to show the      |
    |                      | available servers.                                                                          |
    +----------------------+---------------------------------------------------------------------------------------------+
    | **Disconnect**       | If connected to a server, disconnect.                                                       |
    +----------------------+---------------------------------------------------------------------------------------------+

.. dropdown:: User

    .. image:: /_static/UI_user.png
        :align: left
        :scale: 45%

    +----------------------+---------------------------------------------+
    | **Interaction Force**| Scale the user's interaction force.         |
    +----------------------+---------------------------------------------+

.. dropdown:: Simulation

    .. image:: /_static/UI_simulation.png
        :align: left
        :scale: 45%

    +----------------------+---------------------------------------------------------------------------------------------+
    | **Play**             | Play the simulation.                                                                        |
    +----------------------+---------------------------------------------------------------------------------------------+
    | **Pause**            | Pause the simulation.                                                                       |
    +----------------------+---------------------------------------------------------------------------------------------+
    | **Step**             | Move to the next frame of the simulation.                                                   |
    +----------------------+---------------------------------------------------------------------------------------------+
    | **Reset**            | Reset the simulation to the starting positions.                                             |
    +----------------------+---------------------------------------------------------------------------------------------+
    | **Reset Box**        | Move and resize the box to the original dimensions and position in the VR space.            |
    +----------------------+---------------------------------------------------------------------------------------------+


.. dropdown:: Colocation

    .. image:: /_static/UI_colocation.png
        :align: left
        :scale: 45%

    +--------------------------------+----------------------------------------+
    | **Colocated Lighthouses**      | Toggle colocation. This is only        |
    |                                | compatible with players using HTC base |
    |                                | stations.                              |
    +--------------------------------+----------------------------------------+
    | **Reset Radial Orientation**   | Orient players' VR play spaces into a  |
    |                                | mandala.                               |
    +--------------------------------+----------------------------------------+
    | **Radial Displacement**        | Slide players' VR play spaces inwards  |
    |                                | and outwards from the centre of the    |
    |                                | shared space.                          |
    +--------------------------------+----------------------------------------+
    | **Rotation Correction**        | Adjust the rotation of players' VR     |
    |                                | play spaces to align with the shared   |
    |                                | space.                                 |
    +--------------------------------+----------------------------------------+


.. dropdown:: Debug

    .. image:: /_static/UI_debug.png
        :align: left
        :scale: 45%

    +--------------------------+-----------------------------------------------------------------------------+
    | **Simulate Controllers** | Toggle the simulation of random interaction forces.                         |
    +--------------------------+-----------------------------------------------------------------------------+


.. dropdown:: Misc

    .. image:: /_static/UI_misc.png
        :align: left
        :scale: 45%

    +----------------------+---------------------------------------------+
    | **Quit**             | Quit the program.                           |
    +----------------------+---------------------------------------------+

|

----

.. _vrclientvrcontrolsandmenus:

VR controls & menus
###################

Once you have connected to a server, you can visualize & interact with your simulation.
You now have access to your VR controls & several menus:

* :ref:`insimulationcontrols`

* :ref:`righthandheldmenu`

* :ref:`lefthandheldmenu`

* :ref:`fullscreenmenu`

|

.. _insimulationcontrols:

In-simulation controls
~~~~~~~~~~~~~~~~~~~~~~

You can access the in-simulation controls anytime you are connected to a server and don't have any menus open.
Select from the dropdown options below to see the **video tutorials**:

.. dropdown:: Interact with the simulation

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_interaction.mp4
             :width: 250
             :height: 250

         - Press and hold the trigger button on either controller to apply a force to the nearest atom of the molecule.
           You can use both controllers at the same time.


.. dropdown:: Move the simulation box

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_move-box.mp4
             :width: 250
             :height: 250

         - Press and hold the grip button on either controller to move the simulation box.


.. dropdown:: Resize the simulation box

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_resize-box.mp4
             :width: 250
             :height: 250

         - Press and hold both grip buttons to move & resize the simulation box.


.. dropdown:: Change the magnitude of the interaction force

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_change-interaction-scale.mp4
             :width: 250
             :height: 250

         - Push and hold the joystick on the right controller to the right to increase the force, or to the left to decrease it.
           Doing so will alter the scaling value of the interaction force (see video).
           Note that this changes the force for both controllers.

|

.. _righthandheldmenu:

Right handheld menu
~~~~~~~~~~~~~~~~~~~

Here you can adjust aspects of your interaction with the molecules, such as:

* **Select your interaction type**: toggle between interacting with individual atoms or entire residues

.. grid:: 2
   :gutter: 2

   .. grid-item::

      .. figure:: /_static/in-vr_right-handheld-menu.png
         :align: center
         :width: 65%

   .. grid-item::

      .. important::
         Open the right handheld menu by **holding the joystick of your right controller in the down position**.
         With the joystick held down, move your controller to a button and press the trigger to click it.
         Release the joystick to close the menu.

Open the dropdown below to see the **video tutorial**:

.. dropdown:: Select your interaction type

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_change-interaction-type.mp4
             :width: 250
             :height: 250

         - Select your interaction type:

           * ``Single`` (default): when interacting, you will apply a force to the nearest atom.

           * ``Residue``: when interacting, you will apply a force to the nearest residue.

|

.. _lefthandheldmenu:

Left handheld menu
~~~~~~~~~~~~~~~~~~

Here you can access the fullscreen menu and run simulation commands such as:

* **Pause**: pause a running simulation
* **Play**: play a paused simulation
* **Reset**: reset the system to its initial coordinates

.. grid:: 2
   :gutter: 2

   .. grid-item::

      .. figure:: /_static/in-vr_left-handheld-menu.png
         :align: center
         :width: 60%

   .. grid-item::

      .. important::
         Open the left handheld menu by **holding the joystick of your left controller in the down position**.
         With the joystick held down, move your controller to a button and press the trigger to click it.
         Release the joystick to close the menu.

Select from the dropdown options below to see the **video tutorials**:

.. dropdown:: Pause

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_pause.mp4
             :width: 250
             :height: 250

         - Select the ``Pause`` button.

.. dropdown:: Play

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_play.mp4
             :width: 250
             :height: 250

         - Select the ``Play`` button.

.. dropdown:: Reset

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_reset.mp4
             :width: 250
             :height: 250

         - Select the ``Reset`` button.

|

.. _fullscreenmenu:

Fullscreen menu
~~~~~~~~~~~~~~~

Click ``Menu`` on the left handheld menu to open the fullscreen menu.
Here you can:

* switch between loaded simulations
* customize your avatar name & color

.. grid:: 2
   :gutter: 2

   .. grid-item::

      .. figure:: /_static/in-vr_full-screen-menu.png
         :align: center
         :width: 85%

   .. grid-item::

        .. important::
            Once you have opened the fullscreen menu, release the joystick on your left controller
            and use your **right controller** to interact with the buttons.
            When you are finished, click ``Back`` to return to the simulation.

Select from the dropdown options below to see the **video tutorials**:

.. dropdown:: Switch between loaded simulations

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_switch-simulation.mp4
             :width: 250
             :height: 250

         - Select ``Sims`` and choose from the list of simulations loaded onto the server.
           Click ``Back`` to return to the fullscreen menu.

.. dropdown:: Customize your avatar

   .. list-table::
       :widths: 40 60
       :header-rows: 0

       * - .. video:: /_static/in-vr-menu_change-name-and-color.mp4
             :width: 250
             :height: 250

         - **Change your avatar name**
            Click on your avatar name at the bottom of the fullscreen menu.
            Delete the previous name, type a new one, and click ``>`` to return to the fullscreen menu.

           **Change your avatar color**
            Select one of the colored circles around your avatar (on the fullscreen menu).

           Although not visible to you, these fields are stored in the shared state and determine how others will see your
           avatar during multiplayer sessions.

|

----

.. _choosing_setup_iMD-VR:

##########################
Choosing your iMD-VR setup
##########################

If you wish to visualise and/or interact with your simulations in VR, you will need to use an iMD-VR client.
We focus on NanoVer iMD as the prototypical iMD-VR client, but these instructions can be generalised to any iMD-VR client,
e.g. your own custom VR application that uses the NanoverUnityPlugin.

Please feel free to use the instructions below to help you choose your VR setup,
then search online (or follow the links given below) for the documentation of your chosen method for the latest
instructions on configuring your setup.


#. For help choosing your VR setup, see our flow diagram in :ref:`choosingyourvrsetup`
#. Once you know your VR setup, head to :ref:`choosingyourinstallationmethod`
#. Once you're ready, head to :ref:`installation`


.. note::

    VR is developing fast and there are constantly new features/apps/ways of doing things. Therefore,
    these instructions may not be an exhaustive list of all the possible VR setups. Please feel free to choose whichever
    one you are most comfortable with! We also recommend checking out the online documentation for your VR headset if you
    run into any problems relating to setting up your VR kit.

|

.. _choosingyourvrsetup:

Choosing your VR setup
######################

Below is a flow diagram to help you decide which setup to choose based on: the operating system of your computer,
the type of network you have access to, your VR headset, and your desired configuration (single-/multi-person VR).

.. image::  /_static/VR_client_flow_diagram.png
  :width: 600

.. admonition:: Key point

    For a **wireless setup** you will need to have a strong and stable internet connection that allows communication over the network.
    This option is often incompatible with public / institutional networks.

.. admonition:: Key definition

    \ **Tethered**: using a cable to connect your VR headset to your computer.

|

.. _choosingyourinstallationmethod:

Choosing your installation method
#################################

Please choose from the dropdown options below to learn about how to install NanoVer iMD with your chosen VR setup:

.. dropdown:: Using PC-VR

    This option is compatible with the following VR setups:

    * `Meta Quest Link <https://www.meta.com/en-gb/help/quest/articles/headsets-and-accessories/oculus-link/connect-with-air-link/>`_ (tethered)
    * `Meta Quest AirLink <https://www.meta.com/en-gb/help/quest/articles/headsets-and-accessories/oculus-link/connect-with-air-link/>`_ (wireless)
    * `SteamVR <https://store.steampowered.com/app/250820/SteamVR/>`_ (tethered)
    * `Steam Link <https://store.steampowered.com/app/353380/Steam_Link/>`_ (wireless)

    You can use either NanoVer-iMD installation method:

    * **Downloading the latest release of the NanoVer iMD executable**, see :ref:`download_latest_release_VR_client`.

    * **Conda installation of the NanoVer iMD package**, see :ref:`conda_installation_VR_client`.

.. dropdown:: Running locally on a Meta Quest headset

    This option is compatible with the following VR setups:

    * Run directly on the App store of a Meta Quest headset (wireless)
    * `Meta Quest Link <https://www.meta.com/en-gb/help/quest/articles/headsets-and-accessories/oculus-link/connect-with-air-link/>`_
      with `Meta Quest Developer Hub <https://developer.oculus.com/meta-quest-developer-hub/>`_ (tethered)

    You must use the following NanoVer-iMD installation method:

    * **Download the latest release of the NanoVer iMD apk** and sideload this onto your headset, see
      :ref:`download_latest_release_VR_client`. If you wish to use your VR headset wirelessly,
      then you must meet the requirements for a wireless setup (see above).

    Choosing this option means that you cannot run NanoVer iMD via conda.

|
