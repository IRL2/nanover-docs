 .. _invrmenu:

===========
In-VR menus
===========

.. contents:: Contents
    :depth: 2
    :local:

Using your VR controllers
=========================

Below are diagrams showing the positions of the VR controller buttons that you will use in NanoVer iMD,
using the Meta Quest 2 controllers for demonstration.
These buttons are in similar positions on most common VR controllers,
but please refer to your VR headset's documentation if you cannot locate them.

.. important::
    To press a virtual button on the in-VR menus, **place the end of your VR controller on the button and click the trigger**.

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


Main menu: connecting to a NanoVer server
=========================================

* **Autoconnect**: connect to the first server (using the default port) found on the network.
* **Discover**: find all servers (using the default port) on the network and list them for the user to choose from.
* **Manual**: allow the user to specify the IP address and port of the server they wish to connect to and then, if found, connect to it.

.. important::
    You interact with this menu using your **right controller**.

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_autoconnect.mp4
         :width: 250
         :height: 250

     - **Autoconnect**
        Click ``Autoconnect``. If a server was found, the menu will close and you will see your simulation.

   * - .. video:: /_static/in-vr-menu_discover.mp4
         :width: 250
         :height: 250

     - **Discover**
        Click ``Discover`` to show a list of available servers. Click your chosen server or click ``Refresh`` to
        search again.

   * - .. video:: /_static/in-vr-menu_manual.mp4
         :width: 250
         :height: 250

     - **Manual**
        Click ``Manual``, then type your IP address & port and click ``Connect``.
        If a server was found, the menu will close and you will see your simulation.


In-simulation controls
======================

Once you have connected to a server, you can visualize & interact with your simulation,
and have access to several menus.

Main controls
#############

You can access the main controls anytime you are in the simulation space and no menus are open.
With these controls, you can:

* interact with the simulation
* move the simulation box
* resize the simulation box

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_interaction.mp4
         :width: 250
         :height: 250

     - **Interact with the simulation**:
        Press and hold the trigger button on either controller to apply a force to the nearest atom of the molecule.
        You can use both controllers at the same time.

   * - .. video:: /_static/in-vr-menu_move-box.mp4
         :width: 250
         :height: 250

     - **Move the simulation box**:
        Press and hold the grip button on either controller to move the simulation box.

   * - .. video:: /_static/in-vr-menu_resize-box.mp4
         :width: 250
         :height: 250

     - **Resize the simulation box**:
        Press and hold both grip buttons to move & resize the simulation box.



Right hand controls
###################

Here you can adjust aspects of your interaction with the molecules, including:

* changing the magnitude of the force
* toggling between interacting with individual atoms or entire residues

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_change-interaction-scale.mp4
         :width: 250
         :height: 250

     - **Change the magnitude of the interaction force**:
        Push and hold the joystick on the right controller to the right to increase the force, or to the left to decrease it.
        Note that this changes the force for both controllers.


First menu (handheld)
~~~~~~~~~~~~~~~~~~~~~

.. important::
    Open this menu by **holding down the joystick on your right controller**.
    With the joystick held down, move your controller to a button and press the trigger to click it.
    Let go of the joystick to close the menu.

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_change-interaction-type.mp4
         :width: 250
         :height: 250

     - Select your interaction type: ``Single`` (default) or ``Residue``.

       * ``Single``: when interacting, you will apply a force to the nearest atom.

       * ``Residue``: when interacting, you will apply a force to the nearest residue.



Left hand controls
##################

Within these menus you can:

* run simulation commands, such as play/pause/reset
* change simulation
* customize your avatar

First menu (handheld)
~~~~~~~~~~~~~~~~~~~~~

.. important::
    Open this menu by **holding down the joystick on your left controller**.
    With the joystick held down, move your controller to a button and press the trigger to click it.
    Let go of the joystick to close the menu.

Here, you will see the following options:

* pause the simulation
* play the simulation
* restart the simulation

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_pause.mp4
         :width: 250
         :height: 250

     - **Pause** the simulation.

   * - .. video:: /_static/in-vr-menu_play.mp4
         :width: 250
         :height: 250

     - **Play** the simulation.

   * - .. video:: /_static/in-vr-menu_reset.mp4
         :width: 250
         :height: 250

     - **Restart** the simulation.

Second menu (full screen)
~~~~~~~~~~~~~~~~~~~~~~~~~

Click ``Menu`` on the first menu to open the second menu.
Here you will be able to:

* change simulation
* change avatar name & color

.. important::
    You interact with this menu with your **right controller**.
    Release the joystick on your left controller, and use your right controller to interact with buttons on this menu.
    When you are finished, click ``Back`` to return to the simulation.

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_change-simulation.mp4
         :width: 250
         :height: 250

     - **Change simulation** by selecting ``Sims`` and choosing from the list of simulations loaded onto the server.
       Click ``Back`` to return to the menu.

   * - .. video:: /_static/in-vr-menu_change-name-and-color.mp4
         :width: 250
         :height: 250

     - Change your **avatar name** by clicking on your avatar name at the bottom of the second menu.
       Delete the previous name, type a new one, and click ``>`` to return to the menu.

       Change your **avatar color** by selecting one of the colored circles around your avatar.

       Although not visible to you, these fields are stored in the shared state and determine how others will see your
       avatar during multiplayer sessions.

