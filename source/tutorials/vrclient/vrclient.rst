 .. _vr-client-tutorial:

===========
NanoVer iMD
===========

You can use the `NanoVer iMD application <https://github.com/IRL2/nanover-imd>`_
to **incorporate VR into your workflow**, including:

* visualising molecular systems, including real-time MD simulations, recorded trajectories, and static structures
* interacting with real-time molecular simulations using VR controllers
* joining together with others for multi-person sessions in VR

To install the NanoVer iMD application, please go to :ref:`installation`.


The VR client
#############

We call an instance of the NanoVer iMD application a **VR client**.
This is different to a *python client*, which is a client that connects to a server from a python script.
This distinction is important since the two types of clients offer different functionalities.
For example, both types of client can connect to a NanoVer server to access simulation data
& run commands such as play/pause/reset.
However, only a VR client allows you to visualise & interact with a simulation in VR,
and only a python client allows you to change the visualisation of the molecular system.

.. admonition:: key point

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


