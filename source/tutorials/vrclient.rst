 .. _vr-client-tutorial:

======================
Using an iMD-VR Client
======================

##############
A PC-VR client
##############

When you open a PC-VR client, either from the command line using conda or by running the executable, you will see an
on-screen menu with the following headings:

#. :ref:`server`

#. :ref:`User`

#. :ref:`Simulation`

#. :ref:`Colocation`

#. :ref:`Debug`

#. :ref:`Misc`

----

 .. _server:

Server
~~~~~~

.. image:: /_static/UI_server.png
    :align: left
    :scale: 45%

+----------------------+---------------------------------------------------------------------------------------------+
| **Name**             | **Description**                                                                             |
+======================+=============================================================================================+
| **Autoconnect**      | Connects to the first server found on the network, using the default parameters.            |
+----------------------+---------------------------------------------------------------------------------------------+
| **Direct Connect**   | Toggles a menu where you can change the IP address and trajectory/multiplayer ports         |
|                      | of the server you wish to connect to.                                                       |
+----------------------+---------------------------------------------------------------------------------------------+
| **Discover Services**| Toggles a menu for searching for servers running on the network. Click "Search" to show the |
|                      | available servers.                                                                          |
+----------------------+---------------------------------------------------------------------------------------------+
| **Disconnect**       | If connected to a server, disconnects.                                                      |
+----------------------+---------------------------------------------------------------------------------------------+


.. _user:

User
~~~~

.. image:: /_static/UI_user.png
    :align: left
    :scale: 45%

+----------------------+---------------------------------------------+
| **Name**             | **Description**                             |
+======================+=============================================+
| **Interaction Force**| Scales the user's interaction force.        |
+----------------------+---------------------------------------------+


.. _simulation:

Simulation
~~~~~~~~~~

.. image:: /_static/UI_simulation.png
    :align: left
    :scale: 45%

+----------------------+---------------------------------------------------------------------------------------------+
| **Name**             | **Description**                                                                             |
+======================+=============================================================================================+
| **Play**             | Plays the simulation.                                                                       |
+----------------------+---------------------------------------------------------------------------------------------+
| **Pause**            | Pauses the simulation.                                                                      |
+----------------------+---------------------------------------------------------------------------------------------+
| **Step**             | Moves to the next frame of the simulation.                                                  |
+----------------------+---------------------------------------------------------------------------------------------+
| **Reset**            | Resets the simulation to the starting positions.                                            |
+----------------------+---------------------------------------------------------------------------------------------+
| **Reset Box**        | Moves and resizes the box to the original dimensions and position in the VR space.          |
+----------------------+---------------------------------------------------------------------------------------------+


.. _colocation:

Colocation
~~~~~~~~~~

.. image:: /_static/UI_colocation.png
    :align: left
    :scale: 45%

+--------------------------------+----------------------------------------+
| **Name**                       | **Description**                        |
+================================+========================================+
| **Colocated Lighthouses**      | Toggles colocation. This is only       |
|                                | compatible with players using HTC base |
|                                | stations.                              |
+--------------------------------+----------------------------------------+
| **Reset Radial Orientation**   | Orients players' playspaces into a     |
|                                | mandala.                               |
+--------------------------------+----------------------------------------+
| **Radial Displacement**        | Slides players' playspaces inwards and |
|                                | outwards from the centre of the shared |
|                                | space.                                 |
+--------------------------------+----------------------------------------+
| **Rotation Correction**        | Adjusts the rotation of players'       |
|                                | playspaces to align with the shared    |
|                                | space.                                 |
+--------------------------------+----------------------------------------+

.. _debug:

Debug
~~~~~

.. image:: /_static/UI_debug.png
    :align: left
    :scale: 45%

+--------------------------+--------------------------------------------------------+
| **Name**                 | **Description**                                        |
+==========================+========================================================+
| **Simulate Controllers** | Toggles the simulation of random interaction forces.   |
+--------------------------+--------------------------------------------------------+


.. _misc:

Misc
~~~~

.. image:: /_static/UI_misc.png
    :align: left
    :scale: 45%

+----------------------+---------------------------------------------+
| **Name**             | **Description**                             |
+======================+=============================================+
| **Quit**             | Quits the program.                          |
+----------------------+---------------------------------------------+


