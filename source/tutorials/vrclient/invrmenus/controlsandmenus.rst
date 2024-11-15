.. _controlsandmenus:

Controls & menus
================

Once you have connected to a server, you can visualize & interact with your simulation,
and have access to several menus.

.. contents:: Contents
    :depth: 2
    :local:

In-simulation controls
######################

You can access the main controls anytime you are in the simulation space and don't have any menus open.
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



Right hand menus
################

Here you can adjust aspects of your interaction with the molecules, including:

* changing the magnitude of the interaction force
* toggling between interacting with individual atoms or entire residues

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_change-interaction-scale.mp4
         :width: 250
         :height: 250

     - **Change the magnitude of the interaction force**:
        Push and hold the joystick on the right controller to the right to increase the force, or to the left to decrease it.
        Doing so will alter the scaling value of the interaction force (see video).
        Note that this changes the force for both controllers.


Handheld menu (right)
~~~~~~~~~~~~~~~~~~~~~

.. important::
    Open the right handheld menu by **holding the joystick of your right controller in the down position**.
    With the joystick held down, move your controller to a button and press the trigger to click it.
    Release the joystick to close the menu.

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_change-interaction-type.mp4
         :width: 250
         :height: 250

     - Select your interaction type: ``Single`` (default) or ``Residue``.

       * ``Single``: when interacting, you will apply a force to the nearest atom.

       * ``Residue``: when interacting, you will apply a force to the nearest residue.



Left hand menus
###############

Within these menus you can:

* run simulation commands, such as play/pause/reset
* switch between loaded simulations
* customize your avatar

Handheld menu (left)
~~~~~~~~~~~~~~~~~~~~

.. important::
    Open the left handheld menu by **holding the joystick of your left controller in the down position**.
    With the joystick held down, move your controller to a button and press the trigger to click it.
    Release the joystick to close the menu.

Here, you will see the following options:

* **Pause**: pauses a running simulation.
* **Play**: plays a paused simulation.
* **Reset**: resets the system to its initial coordinates.

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_pause.mp4
         :width: 250
         :height: 250

     - **Pause**
        Select the ``Pause`` button.

   * - .. video:: /_static/in-vr-menu_play.mp4
         :width: 250
         :height: 250

     - **Play**
        Select the ``Play`` button.

   * - .. video:: /_static/in-vr-menu_reset.mp4
         :width: 250
         :height: 250

     - **Reset**
        Select the ``Reset`` button.

Full screen menu
~~~~~~~~~~~~~~~~

Click ``Menu`` on the left handheld menu to open the full screen menu.
Here you will be able to:

* switch between loaded simulations
* customize your avatar name & color

.. important::
    Once you have opened the full screen menu, release the joystick on your left controller
    and use your **right controller** to interact with the buttons.
    When you are finished, click ``Back`` to return to the simulation.

.. list-table::
   :widths: 40 60
   :header-rows: 0

   * - .. video:: /_static/in-vr-menu_change-simulation.mp4
         :width: 250
         :height: 250

     - **Change simulation**
        Select ``Sims`` and choose from the list of simulations loaded onto the server.
        Click ``Back`` to return to the full screen menu.

   * - .. video:: /_static/in-vr-menu_change-name-and-color.mp4
         :width: 250
         :height: 250

     - **Change your avatar name**
        Click on your avatar name at the bottom of the full screen menu.
        Delete the previous name, type a new one, and click ``>`` to return to the full screen menu.

       **Change your avatar color**
        Select one of the colored circles around your avatar (on the full screen menu).

       Although not visible to you, these fields are stored in the shared state and determine how others will see your
       avatar during multiplayer sessions.
