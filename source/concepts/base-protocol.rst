.. _base-protocol:

============================
The NanoVer Network Protocol
============================

.. contents:: Contents
    :depth: 2
    :local:

----

########
Overview
########

Standard network communication between client and server in NanoVer is divided into
three parts: **command requests and responses**, **state updates**, and **simulation
updates**. These are used together, for example, to support VR iMD by providing live
simulation updates to the VR client, which itself sends interactions as state updates,
and can request simulation resets or pauses via commands.

**Command requests and responses** allow the client to request actions or information
from the server, such as pausing or resetting the active simulation, or retrieving the
list of available commands. This is also known as a Remote Procedure Call  (RPC).

**State updates** provide continuous information about the changes occurring to a
shared dictionary used for synchronising arbitrary data between clients. In the iMD-VR
case, this is used for sharing the head and hand positions of all users, and for the
interactive biasing potentials they wish to apply to the simulation.

**Simulation updates** are a specialised version of state updates, used to synchronise
data pertaining to the simulated system as it evolves over time during simulation.
Mostly this is a continuous sequence of messages with updated atom positions, but
when a client initially joins, the update from an empty state contains the topology of
the simulated system and other properties.

These are the three message types used and understood by NanoVer, but additional
types can be added safely and easily as necessary.

|

----

.. _commands:

##############################
Command requests and responses
##############################

Introduction
############

A server can expose named functions that clients can call remotely, optionally
providing parameters, to either to trigger some side effect or retrieve some value.
This is an implementation of Remote Procedure Call (RPC).

The standard server includes a command (``commands/list``) that returns the list of
available commands and information about the arguments they accept.

----

Running a command
#################

A command request contains three pieces of information: the string name of the command requested,
a dictionary of string keys mapping to arbitrary values to the named parameters of the function,
and an integer id used to match the associated response to this request:

.. code:: python

    {
        "command": {
            "request": {
                "name": "math/multiply",
                "arguments": {"a": 2, "b": 4},
                "id": 0,
            },
        },
    }

After receiving the command request and running the underlying function, the server will respond
with another message. A command response message contains the original request (which contains the
unique id) and the return value of the underlying function:

.. code:: python

    {
        "command": {
            "request": {
                "name": "math/multiply",
                "arguments": {"a": 2, "b": 4},
                "id": 0,
            },
            "response": {
                "multiplied": 8,
            },
        },
    }

If the command request couldn't be satisfied, the response message will instead contain an exception
message:

.. code:: python

    {
        "command": {
            "request": {
                "name": "math/multiply",
                "arguments": {"a": 2, "b": 4},
                "id": 0,
            },
            "exception": "No command math/multiply.",
        },
    }

For an interactive Jupyter notebook tutorial that demonstrates how to set up
and run commands in practice, check out our `commands_and_state` notebook
(see :ref:`nanover-fundamentals`).

|

----

.. _state:

#############
State updates
#############

Introduction
############

The server maintains a dictionary of string keys to arbitrary values intended to
be synchronised between all clients, that they can use to broadcast persistent data.

For an interactive Jupyter notebook tutorial that complements the information presented
in this section, check out our `commands_and_state` notebook (see :ref:`nanover-fundamentals`).

----

.. _state-updates:

State and state updates
#######################

The state is thought of as a key-value store. As clients insert, update, and delete values
from the store, the server sends out update messages so that all clients can keep their
local copy up-to-date.

A state update message contains two pieces of information: a map of updated keys and their
new values, and a list of keys that were removed:

.. code:: python

    {
        "state": {
            "updates": {
                "user.luis": {
                    "name": "luis",
                    "avatar": "😎",
                },
            },
            "removals": ["user.mark"],
        },
    }

Complex nested values can be stored, but in that case the whole nested structure must be
updated at once. It is still considered as a single value and there is currently no
provided method to partially update such structures.

A client requests changes to the state by sending a message of the same structure back to
the server with the updates and removals they want to make. Currently the only confirmation
of a successful update is observing the change in a future update message from the server.

|

----

.. _simulation-updates:

##################
Simulation updates
##################

Introduction
############

The server broadcasts molecular systems using the **simulation updates**.
Molecular systems can be running simulations, static structures, recorded
trajectories, or any collection of particles regardless of how they are
produced. They are represented as a sequence of one or more **frames** where each
frame represents a state of the molecular system.

.. note::

   This capability was initially designed with molecular systems in mind, hence the
   wording in this documentation. However, while we established a set of conventions
   to represent such systems, the protocol is not limited to them.

----

.. _frame-updates:

Frames and frame updates
########################

In NanoVer, frames are very similar to the key value store used for state, but specialised
for the purposes of particles simulations, especially molecular dynamics.

Frame updates are just a mapping of frame keys and their updated values:

.. code:: python

    {
        "frame": {
            "frame.index": 0,
            "particle.names": ["C0", "C1"],
        },
    }

.. note::

   For efficiency, some predefined keys, such as particle positions in ``particle.positions``
   are not sent as simple lists of numbers but are first packed into a raw bytestring before
   inclusion in the message. This is because MessagePack cannot assume they are homogenous
   arrays and instead sends type information for every single number, which wastes space.

   You can find a listing of packing types in the ``FRAME_PACKERS`` in `frame_dict.py`.

The server broadcasts these changes as the system evolves during simulation by sending
these frame update messages, and the clients aggregate the messages to arrive at a
complete frame.

.. note::

   Aggregating frames is a simple as taking all the existing frames of the previous
   aggregate frame (or empty) and overwriting all the updated keys from the next frame.
   However, by convention, a `frame.index` equal to 0 is used to indicate a change of
   simulation system, meaning that previous topological information, positions, etc., should be discarded.

.. note::

   The frame updates are sent at a constant rate, with any intermediate frames aggregated
   by the server. If more than one
   frame is generated by the server during the interval, then an aggregated
   frame is sent by the server. This can cause the client to miss data when one
   frame overwrites keys from the previous one. Client should expect to always
   receive the latest state of the trajectory, but not to receive all the time
   points generated by the server.

|

