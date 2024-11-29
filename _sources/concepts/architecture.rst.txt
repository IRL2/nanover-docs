NanoVer Architecture
====================

.. contents:: Contents
    :depth: 2
    :local:

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
  molecular dynamics simulations run using python, while our VR application
  is written in C#. 
* **The server can be running wherever it is convenient**, be it on your desktop,
  a cluster behind a firewall or on a cloud service, while multiple frontend 
  applications can connect simultaneously, such as a VR app, 
  smartphone app, or a Jupyter notebook. 

Services 
########

While the client/server model is useful, implementing monolithic client/server applications is not ideal,
as it limits the customisability and extensibility of the framework.
Instead, in NanoVer we have adopted a microservices architecture, in which many modular services communicate.

This architecture makes NanoVer very flexible.
New features can be added as new services as needed, without cluttering up the main framework.
We provide a number of service definitions and implementations, including:

* :doc:`nanover.trajectory <../../python/nanover.trajectory>`: Provides trajectories and live simulations.
* :doc:`nanover.state <../../python/nanover.state>`: Provides synchronisation of avatars and state for multiplayer applications.
* :doc:`nanover.command <../../python/nanover.command>`: Provides facilities to run arbitrary functions performed by the server.

The services described above provide the core for the NanoVer iMD-VR application, but the tools
can be used to create custom services for different applications.

These services are written using `gRPC <https://grpc.io/>`_, a framework for remote procedure calls. 
The key features that make it great for NanoVer are:

* **High performance, fast communication**.
* **Bidirectional streaming**. Clients and servers can establish long lived
  connections and stream data to and from each other flexibly.
* **Language portable**. Clients and servers can be written in many languages,
  including C#, Python and C++. 
* **Built on HTTP2**, so includes routing, authentication and security.

An Example: Interactive Molecular Dynamics
##########################################

The canonical NanoVer session is one of interactive molecular dynamics (IMD), where one or more front end applications 
connect to a live simulation that can be visualised and interacted with through biasing potentials. 

Conceptually, the IMD server consists of three services: a trajectory service, a state service, and a command service.

* **The trajectory service** provides updates as the state of the simulation progresses, enabling real-time analysis and
  visualisation of the system.
* **The state service**, meanwhile, takes care of incoming requests from the client applications to apply biasing potentials
  to the simulation. These are applied as forces to the molecular dynamics engine, which in turn integrates them.
  This service allows synchronisation of the state between all the clients and the server
  (note that these can be any arbitrary state variables).
  For instance, it synchronises the position of the users' avatars, allowing multi-user collaboration.
  It broadcasts users' avatar positions, therefore allowing multiuser collaboration with no server modification.
* **The command service** facilitates the communication of commands between the client and the server.
  For example, these could be playback control commands, such as requests to pause or reset the simulation.
  You can also create your own custom commands that can be handled by this service.

A server application can leverage these three services to implement IMD to facilitate the visualisation of, and
interaction with, a simulation in real time.


VR Front End
############

The VR front end app, :ref:`NanoVer iMD-VR <vr-client-tutorial>`, intended for 3D visualisation and
intuitive spatial iMD (iMD-VR), is a `distinct Unity/C# codebase <https://github.com/IRL2/nanover-imd-vr>`_
that follows the `gRPC protocol definitions <https://github.com/IRL2/nanover-server-py/tree/main/protocol/nanover/protocol>`_
and :ref:`application conventions <applications>` laid out in the present documentation.

