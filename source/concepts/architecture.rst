====================
NanoVer Architecture
====================

.. contents:: Contents
    :depth: 2
    :local:

----

########
Overview
########

NanoVer is a set of protocols, libraries and programs for performing interactive simulations,
with a focus on virtual reality (VR).

At the highest level, NanoVer uses a client/server model, in which a frontend application connects
to a server that runs a simulation in real-time, establishing an interactive session.
Simulation data, interactions and controls are transmitted over the network between the client and server.
There a several good reasons for using this model:

* **Separation of concerns**. Keeping the simulation separate from the visualisation
  makes it easier to customise and add new features. You want to swap out a 
  molecular simulation for a galaxy simulation? Just change the server!
* **Scientific software is often written in different programming languages to
  those that are best suited for visualisation**. For example, most of our
  molecular dynamics simulations run using Python, while our VR application
  is written in C#. 
* **The server can be running wherever it is convenient**, be it on your desktop,
  a cluster behind a firewall or on a cloud service, while multiple frontend 
  applications can connect simultaneously, such as a VR app, 
  smartphone app, or a Jupyter notebook. 

|

----

##########
Networking
##########

NanoVer servers and clients communicate by sending [MessagePack](https://msgpack.org/index.html) encoded data over
[WebSocket](https://en.wikipedia.org/wiki/WebSocket) connections. These two technologies were chosen for their maturity,
wide support across languages and environments, and ease of use.

At the high level, NanoVer communicates using JSON-like messages between server and client. Each message sent and
received is an object with a key mapping a particular message type to an object representing the message payload.
The standard message types in NanoVer are "frame", "state", and "command", but it is simple to add support for
additional types as desired for new applications.

|

----

##########################################
An Example: Interactive Molecular Dynamics
##########################################

The standard NanoVer server is built for interactive molecular dynamics (iMD), where one or more front end applications
connect to a live simulation that can be visualised and interacted with through biasing potentials.

Conceptually, the external interface of the server is divided into three parts: the simulation frame, the shared state,
and the commands.

* **The simulation frame** is the current state of the simulation, represented by a dictionary of string keys mapping
  to positions, elements, and other other relevant data that is exposed to clients. Updates are sent as "frame" messages
  that contain the updated values of each key that has changed.
* **The shared state** is the a more general store of data, also represented by a dictionary of string keys, that is
  shared and updated by all clients. For instance, multi-user collaboration is implemented by each client updating this
  shared state with the positions of their VR headsets and controllers so that they can be visualised in real time by
  other connected clients. This is also where the interactive biasing potentials of iMD are added and updated. Updates
  are sent as "state" messages that contain the updated values of each key that has changed, and a list of keys that
  have been deleted.
* **The commands** are kept as a registry of named functions added to the server that are available to be invoked by
  remote clients. These could be, for example, playback control commands, such as requests to pause or reset the
  simulation. You can define custom commands on the server for whatever purpose arises. Command requests and responses
  are sent as "command" messages containing the command name and arguments (or in the case of responses, the response
  values).

An application can leverage these three parts to implement iMD that provides visualise and interact with a simulation
in real time.

|

----

############
VR Front End
############

The VR front end app, :ref:`NanoVer iMD-VR <vr-client-tutorial>`, intended for 3D visualisation and
intuitive spatial iMD (iMD-VR), is a `distinct Unity/C# codebase <https://github.com/IRL2/nanover-imd-vr>`_
that follows the `gRPC protocol definitions <https://github.com/IRL2/nanover-server-py/tree/main/protocol/nanover/protocol>`_
and :ref:`application conventions <applications>` laid out in the present documentation.

|

