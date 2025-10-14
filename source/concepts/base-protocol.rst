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
from the server, such as pausing or reseting the active simulation, or retrieving the
list of available commands. This is also known as a Remote Procedure Call  (RPC).

**State updates** provide continuous information about the changes occuring to a
shared dictionary used for synchronising arbitrary data between clients. In the iMD-VR
case, this is used for sharing the head and hand positions of all users, and for the
interactive biasing potentials they wish to apply to the simulation.

**Simulation updates** are a specialised version of state updates, used to synchronise
data pertaining to the simulated system as it evolves over time during simulation.
Mostly this is a continous sequence of messages with updated atom positions, but
when a client initially joins, the update from an empty slate contains the topology of
the simulated system and other rarely changing properties.

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
            "removes": ["user.mark"],
        },
    }

Complex nested values can be stored, but in that case the whole nested structure must be
updated at once. It is still considered as a single value and there is currently no
provided method to partially update such structures.

----

Subscribing to state updates
############################

.. code:: protobuf

   service State {
       // Periodically received aggregated updates from last known state to latest
       // state of a shared key/value store.
       rpc SubscribeStateUpdates(SubscribeStateUpdatesRequest) returns (stream StateUpdate) {}
       ...
   }

   message SubscribeStateUpdatesRequest {
       // Interval (in seconds) between update sends.
       float update_interval = 1;
   }

Clients can subscribe to a stream of updates. The server sends the
updates at the requested rate, waiting at least the requested
``update_interval`` between two updates. The waiting time may be
longer, though, due to a variety of factors including a slow server or
network delays. Therefore, a client should not assume that the rate is
regular, or even respected. Still, it is important to request the
longest update interval that is suitable for the needs in order to
reduce the load on all the involved actors.

.. warning::

   It is possible for an update to be too large to be
   transmitted in one gRPC packet. If this happens, the behaviour is
   undefined.

----

Updating the state
##################

.. code:: protobuf

   service State {
       // Attempt to make an update to the shared key/value store.
       rpc UpdateState(UpdateStateRequest) returns (UpdateStateResponse) {}
   }

   message UpdateStateRequest {
       // Token for associating requests to their lock ownership.
       string access_token = 1;

       // Updates to make to state.
       StateUpdate update = 2;
   }

   message UpdateStateResponse {
       // Whether the update was successful.
       bool success = 1;
   }

A client can request an update of the state using the ``UpdateSate`` method. The
request contains an ``access_token`` and the update itself. The update is
formatted in the same way as updates received from the server. The
``access_token`` is an arbitrary string, chosen by the client, and that
identifies that client to the server. The access token is used by the server to
resolve locks that may be set on the keys in the update. The method returns a
``UpdateStateResponse`` containing a boolean that is true if the update
succeeded.

State updates are "atomic" operations. All the keys in an update are updated at
once and they are either all successfully updated or none are updated. An update
can fail if one key is locked by another client. See the :ref:`State locks
<state-locks-description>`
section.

When an update succeeds, the server incorporates the changes and broadcasts them
to all subscribed clients. Clients may receive these updates aggregated with
other updates depending on what updates were received by the server during the
client's subscription interval.

.. note::

   A non-existing key can be removed if the locks allow.

A server can make updates to the shared state. How the server does it is out of
scope of the protocol, but the server updates need to appear in the state update
stream of the subscribed clients.

----

.. _state-locks-description:

State locks
###########

.. code:: protobuf

   service State {
       // Attempt to acquire, renew, or release exclusive control of keys in the
       // shared key/value store.
       rpc UpdateLocks(UpdateLocksRequest) returns (UpdateLocksResponse) {}
   }

   message UpdateLocksRequest {
       // Token for associating requests to their lock ownership.
       string access_token = 1;

       // Struct where each field an state key and either a time in seconds to
       // acquire or renew the lock for, or a null to indicate the lock should be
       // released if held.
       google.protobuf.Struct lock_keys = 2;
   }

   message UpdateLocksResponse {
       // Whether the locking was successful.
       bool success = 1;
   }

Multiple clients may update the same key. If they do so close enough in time,
other clients will receive a different assortment of these updates which can
appear as visual or logical glitches. In practice, if clients display an object
with its location bound to a shared state key, and if multiple clients try to
move that object, it may appear to jump between different locations as
clients receive conflicting locations. To avoid such situations, clients have
the ability to request a lock on a key or set of keys.

A lock applies to a key in the shared state. It has an access token, and a
duration in seconds during which it is valid. The access token is an arbitrary
string, chosen by the client, that associates the client with its locks. The
client sends this key alongside its requests to update the shared state, and the
update only succeeds if all the keys in the request have no valid locks on them
or if the locks are associated with the same access token as in the update request.

A client can create, renew, or remove locks. To do so, it needs to call the
``UpdateLocks`` method with an ``UpdateLocksRequest``. The request contains the
access token and a `Struct
<https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Struct>`_.
with the state key associated with the lock to update as key, and either a
duration in seconds or a `Null value
<https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.NullValue>`_
as value. If the value is a duration, then the lock is created or renewed with
the requested validity duration. If the value is null, then the lock is deleted.
A lock can only be updated if:

* it does not yet exist
* it exists but has expired
* it is held by the same access token as the request

Each update can be about one or multiple locks; a request only succeeds if
all the locks can be updated. If any of the locks cannot be updated, then
none of the locks are updated.

.. note::

   Locks can be applied to non-existing keys. Removing a lock does not remove
   the key on which it was applied and removing a key does not remove a lock
   that would apply to it.

----

Security issues
###############

The way to handle updates larger than a gRPC packet is undefined.
Servers may implement that case by shutting down, implementing solutions
that lead to a stale state or a degraded experience. This makes the
state service very susceptible to low effort denial of service attacks.

For now, no server nor client implement any form of encryption.
Therefore, the access tokens used to lock keys in the shared state
should be considered publicly exposed.

|

----

.. _trajectory-service:

######################
The trajectory service
######################

Introduction
############

A server can broadcast molecular systems using the **trajectory service**.
Molecular systems can be running simulations, static structures, recorded
trajectories, or any collection of particles regardless of how they are
produced. They are represented as a sequence of one or more **frames** where each
frame represents a state of the molecular system.

.. note::

   The trajectory service was initially designed with molecular systems in mind,
   hence the wording in this documentation. However, while we established a set
   of conventions to represent such systems, the protocol is not limited to
   them.

----

.. _frame-description:

Frame description
#################

.. code:: protobuf

    /* A general structure to represent a frame of a trajectory.
    It is similar in structure to the Google Struct message,
    representing dynamically typed objects and lists. However,
    as frames often consist of large arrays of data of the same
    type, a set of arrays are also provided as specified in
    nanover/protocol/array.proto */
    message FrameData {

      /* A standard key-value list of dynamically typed data */
      map<string, google.protobuf.Value> values = 1;

      /* A key-value list of value arrays */
      map<string, nanover.protocol.ValueArray> arrays = 2;
    }

NanoVer describes frames using the ``FrameData`` structure. A ``FrameData``
contains two key-value maps to describe the changes from the previous state of
the trajectory. An implementation using this structure needs to maintain an
aggregate ``FrameData`` and merge all incoming frames to get the current state
of the system.

A ``FrameData`` contains two fields: ``values`` and ``arrays``.

* The ``values`` field is a key-value map where each key is a string and each value is
  a protobuf `Value <https://protobuf.dev/reference/protobuf/google.protobuf/#value>`_.
  This map typically stores simple data related to the frame: data consisting of a
  single number, boolean, or string. This being said, it can contain more complex data structures
  such as heterogeneous lists or protobuf `Structs
  <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Struct>`_.
* The ``arrays`` field is a key-value map in which homogeneous arrays (i.e. arrays
  where all the values have the same type) can be stored. In this map, each key is a string
  and each value is a ``ValueArray``, which can contain a homogeneous array of either
  floats (``FloatArray``), unsigned integers (``IndexArray``), or strings (``StringArray``).

The meaning of the keys in both fields of the ``FrameData`` depends on the application.

To see examples of how these types of data are added to frames in practice, take a look
at our `frame` tutorial notebook (see :ref:`nanover-fundamentals`).

.. code:: protobuf

    message FloatArray {
      repeated float values = 1;
    }

    message IndexArray {
      repeated uint32 values = 1;
    }

    message StringArray {
      repeated string values = 1;
    }

    message ValueArray {
      oneof values {
        FloatArray float_values = 1;
        IndexArray index_values = 2;
        StringArray string_values = 3;
      }
    }

While a ``FrameData`` can describe a full frame, it is mostly used to describe
the changes in a frame compared to the previous ones. As such, it is expected
that a program working with these frames will merge them. A ``FrameData``
contains the key-value pairs to change for both the ``values`` and the
``arrays`` fields. In case of complex structures in ``values``, the new
``FrameData`` needs to contain the full new value even if only part of it
changed. Likewise for ``arrays``, the new ``FrameData``
needs to contain the full array in ``arrays`` even if only a
single element of it has changed. When merging, key-value pairs from the new frame
replace those from the aggregated frame. Key-value pairs that are only in the
new frame are added to the aggregated frame. Pairs that do not appear in the
new frame remain untouched in the aggregated one.

.. note::

   This aggregation process is made use of in NanoVer's interactive molecular
   dynamics application, in which clients can access the most
   recent updates to the frame (:py:attr:`NanoverImdClient.latest_frame`) or
   the full set of aggregated data pertaining to the current frame of the
   simulation (:py:attr:`NanoverImdClient.current_frame`).

Here is an example of frames being merged:

::

  Aggregated frame:        New frame:           Resulting frame:
    * values:                * values:            * values:
      - key0: A                - key1: B            - key0: A
      - key1: A        +       - key4: B     =      - key1: B
    * arrays:                * arrays:              - key4: B
      - key2: A                - key2: B          * arrays:
      - key3: A                                     - key2: B
                                                    - key3: A

When part of a stream, ``FrameData`` messages are wrapped into ``GetFrameResponse`` ones.

.. code:: protobuf

    /* A server response representing a frame of a molecular trajectory */
    message GetFrameResponse {

      /* An identifier for the frame */
      uint32 frame_index = 1;

      /* The frame of the trajectory, which may contain positions and topology information */
      nanover.protocol.trajectory.FrameData frame = 2;

    }

A ``GetFrameResponse`` message contains a ``FrameData`` and a frame index. This
index is an unsigned integer that is commonly incremented every time a new
frame is created. The exact value of the index, however, is only meaningful
when it is 0. When it is 0, it signals that the aggregated frame needs to be
reset. This can occur when the new frame originates from a completely different
simulation, for instance. In this case, the aggregated frame and the new frame
do not describe the same system and they should not be merged. Note that this
is the only mechanism that allows the removal of a key from the aggregated frame.

----

Subscribing to the latest frames
################################

.. code:: protobuf

    /* A service which provides access to frames of a trajectory,
    which may either be precomputed or represent a live simulation.
    It can also be used to obtain one or more frames on demand,
    allowing molecules or trajectories to be generated based on requests */
    service TrajectoryService {

      /* Subscribe to a continuous updating source of frames.
      The client gets the latest available frame at the time of transmission. */
      rpc SubscribeLatestFrames (GetFrameRequest) returns (stream GetFrameResponse);
    }

    /* A client request to get frame(s) from a trajectory service */
    message GetFrameRequest {

      /* Arbitrary data that can be used by a TrajectoryService to
      decide what frames to return */
      google.protobuf.Struct data = 1;

      /* Interval to send new frames at e.g 1/30 sends 30 frames every second. */
      float frame_interval = 2;
    }

A client can subscribe to a stream of the frames broadcast by the server
using the ``SubscribeLatestFrames`` method. When subscribing, the client sends
a ``GetFrameRequest`` message with a time interval expressed in seconds. The
server will try to send new frames as they are available and at most at this
interval. If multiple frames were produced during the interval, the server will
send the aggregate of these frames. The frames are sent as ``GetFrameResponse``
messages.

When subscribing, a client may provide additional data as part of the
``GetFrameRequest``. This aims at allowing some server-side filtering of the
broadcast frames. **At this time, no server uses this data.**

.. note::

   A client subscribed to this stream may miss some data. If more than one
   frame is generated by the server during the interval, then an aggregated
   frame is sent by the server. This can cause the client to miss data when one
   frame overwrites keys from the previous one. Client should expect to always
   receive the latest state of the trajectory, but not to receive all the time
   points generated by the server.

----

Subscribing to all frames
#########################

.. code:: protobuf

    /* A service which provides access to frames of a trajectory,
    which may either be precomputed or represent a live simulation.
    It can also be used to obtain one or more frames on demand,
    allowing molecules or trajectories to be generated based on requests */
    service TrajectoryService {

      /* Subscribe to a continuous updating source of frames.
      Frames are added to the stream when they are available */
      rpc SubscribeFrames (GetFrameRequest) returns (stream GetFrameResponse);
    }

**Optionally**, a server may allow a client to subscribe to all the broadcast
frames using the ``SubscribeFrames`` method. In this case, the client sends a
``GetFrameRequest`` with a time interval and possibly extra data. The server
will send frames as ``GetFrameResponse`` objects when they are available and at
most at the requested interval. However, the frames will not be aggregated so
the last frame received by the client may not be the last frame that was
produced. A client subscribing to this stream will receive all the time points
produced by the server, but may lag behind the current state of the simulation.

This subscription method can be a security risk and servers may choose to not
implement it. Indeed, if a client subscribes to all the frames with a long
interval, the server needs to record all the frames until they are sent to the
client. This can cause significant disk and/or memory usage.

|

