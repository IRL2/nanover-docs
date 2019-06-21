Narupa Architecture
=======================

Narupa is a set of protocols, libraries and programs for performing interactive simulations, with a focus
on virtual reality (VR).

At the highest level, Narupa uses a client/server model, in which a frontend application connects
to a server, establishing an interactive session. Simulation data, interactions and controls are transmitted
over the network between the client and server. This means that the server can be running on your desktop,
a cluster behind a firewall or on a cloud service,
while multiple frontend applications can connect simultaneously, such as a VR app,
smartphone app, or a Jupyter notebook. 

.. image:: assets/architecture/narupa_2019_client_server.png 
    :height: 1578px
    :width: 4000px
    :scale: 20%
    :alt: The high-level client server model of Narupa.


Services 
########################

While the client/server model is useful, implementing monolothic client/server applications is not ideal, as it limits the
customisability and extensibility of the framework. Instead, in Narupa we have adopted a microservices architecture, in which 
many modular services communicate.

.. image:: assets/architecture/narupa_2019_microservices.png 
    :height: 1875px
    :width: 4000px
    :scale: 20%
    :alt: Narupa microservices architecture.

.. note::  The session orchestration via a lobby remains to be implemented, but is recorded here to outline the expected architecture.

A Narupa session represents a collection of these services running together to
produce an application experience.
Every session consists of a lobby, which is the entry point to a session.
Client applications can join the lobby, discover what services are available
or running, and join them.

This architecture makes Narupa very flexible.
New features can be added as new services as needed, without cluttering up
the main framework.
We provide a number of service definitions and implementations, including:

* :doc:`narupa.trajectory <../../python/narupa.trajectory>`: Provides trajectories and live simulations. 
* Interactive molecular dynamics (IMD) service: Exposes methods for applying interactive biasing potentials to a simulation. 

These services are written using `gRPC <https://grpc.io/>`_, a framework for remote procedure calls. 
The key features that make it great for Narupa are:

* High performance, fast communication. 
* Bidirectional streaming. Clients and servers can establish long lived connections and stream data to and from each other flexibly.
* Language portable. Clients and servers can be written in many languages, including C#, Python and C++. 
* Built on HTTP2, so includes routing, authentication and security. 

An Example: Interactive Molecular Dynamics
################################################

The canonical Narupa session is one of interactive molecular dynamics (IMD), where one or more front end applications 
connect to a live simulation that can be visualised and interacted with through biasing potentials. 

Conceptually, the IMD server consists of two services: a trajectory service and an IMD service. The trajectory
service publishes the changes in the simulation to clients, enabling it to be visualised. It also handles 
control of the simulation state, such as pausing or restarting. 
The IMD service, meanwhile, takes care of incoming requests from the client applications to apply biasing potentials
to the simulation. These are applied as forces to the molecular dynamics engine, which in turn integrates them. 

Combined together, the two services are sufficient to visualise and interact with a simulation in real time.
How these services actually talk to MD program that they provide is an implementation detail,
which the protocol does not need to know about.
They don't necessarily even need to be running in the same program. For the narupa.openmm package, the trajectory 
service is written at the python layer in the form of an OpenMM reporter, while to perform the IMD it is necessary 
to write a C++ plugin that is instantiated as a force field within OpenMM. Hence in this case, the two services actually
run as separate servers.

.. image:: assets/architecture/narupa_2019_imd_server.png 
    :height: 1809px
    :width: 4000px
    :scale: 20%
    :alt: Narupa interactive molecular dynamics architecture. 

The trajectory and IMD service are sufficient to produce an application that front end clients
can connect to and visualise.
In the simplest case, the services will run on a particular port on the network,
and a front end can be configured to connect to them. 

However, ideally we want to automatically discover what services are running. Additionally, 
Narupa provides additional useful functionality,
such as synchronisation as of avatars in a multiuser environment.
The trajectory and IMD services do not need to concern themselves
with the details of multiplayer,
and so this functionality is implemented in another service, the Multiplayer service. 

To orchestrate these services, the lobby service is the core service that defines a Narupa session. 
In the case of an IMD session, when a user starts a Narupa session, it will start
the lobby service, configured to run the multiplayer service, the trajectory service and the IMD service.
The user can then share the details of the lobby session with front end applications.
When additional VR users or other front ends connect to the lobby, they can query what else is running and 
then proceed to join the other services that are running as appropriate.

Front End Architecture
################################################

As the server side is modular, so too is the front end. For the VR front end, NarupaXR, 
there are modules for handling the communication with each service, 
which in turn are used to produce application modules that simplify the development of different 
VR applications. For example, there are modules for handling trajectories and simulations, modules 
for performing multiplayer synchronisation, and of course modules for rendering molecular structures. 

.. image:: assets/architecture/narupa_2019_imd_frontend.png 
    :height: 1793px
    :width: 4000px
    :scale: 20%
    :alt: Narupa interactive molecular dynamics front end example architecture.