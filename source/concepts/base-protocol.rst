The NanoVer protocol
====================

General architecture
--------------------

NanoVer provides 3 services: the state service, the trajectory service,
and the command service. While none of the service is strictly
mandatory, some features expect two or three services to cooperate.

The *state service* maintains a state that is shared between the server
and one or more clients. The state is presented as a key-value store;
users can subscribe to updates to the state, send updates themselves,
and request exclusive write access to some keys. This service is used to
share the position of the user’s avatars, to send user’s interactions
with molecular systems, and to share the molecular representations. It
can be used to send any arbitrary data to the server and to the clients.

The *trajectory service* allows the server to broadcast the state of a
simulation to the clients. It sends frames to the clients at the
requested frame rate.

The *command service* lets client run functions on the server. This
service is used to pause or reset a molecular simulation.

The services can be all served from a different address and/or a
different port. However, they are commonly served together from the same
address and port. The default port is 38801.

The state service
-----------------

The state service maintains a state that is shared between the server
and the clients.

.. _state-updates:

State and state updates
~~~~~~~~~~~~~~~~~~~~~~~

The state is thought of as a key-value store.

Clients can subscribe to a stream of updates and need to maintain their
own version of the full state.

.. code:: protobuf

   message StateUpdate {
       // Struct where each field is an updated state key and it's latest value,
       // where null is equivalent to a key removal.
       google.protobuf.Struct changed_keys = 1;
   }

The state update is presented as a protobuf
`Struct <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Struct>`_.
The keys in the update directly refer to the keys in the full state. The
values in the update are the new values the state should contain. `Null
values <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.NullValue>`_
are a special case; indeed they correspond to keys that should be
removed from the full state. Therefore, the full state cannot contain
null values.

A state update can contain nested values. In that case, the whole nested
structure must be updated at once. A nested value is still considered as
a single value and the protocol does not offer ways of performing a
partial update of such structures.

Subscribing to state updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
update at the requested rate waiting at least the requested
``update_interval`` in between two updates. The waiting time may be
longer, though, due to a variety of factors including a slow server or
network delays. Therefore, a client should not assume the rate is either
regular, or even respected. Still, it is important to request the
longest update interval that is suitable for the needs in order to
reduce the load on all the involved actors.

.. warning::

   It is possible for an update to be too large to be
   transmitted in one gRPC packet. If this happens, the behaviour is
   undefined.

Updating the state
~~~~~~~~~~~~~~~~~~

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
once and they are either all successfully updated or none is updated. An update
can fail if one key is locked by another client. See the :ref:`State locks
<state-locks-description>`
section.

When an update succeeds, the server incorporate the changes and broadcast them
to all subscribed clients. Clients may receive these updates aggregated with
other updates depending on what updates were received by the server during the
client's subscription interval.

A server can make updates to the shared state. How the server does it is out of
scope of the protocol, but the server updates need to appear in the state update
stream of the subscribed clients.

.. _state-locks-description:

State locks
~~~~~~~~~~~

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
appear as visual or logical glitch. In practice, if clients display an object
with its location bound to a shared state key, and if multiple clients try to
move that object, it may appear as jumping between different locations as
clients receive conflicting locations. To avoid such situations, clients have
the ability to request a lock on a key or on a set of keys.

A lock applies to a key in the shared state. It has an access token, and a
duration in seconds during which it is valid. The access token is an arbitrary
string, chosen by the client, that associate the client with its locks. The
client sent this key alongside its requests to update shared state, the update
only succeeds if all the keys in the request have no valid locks on them or if
the locks are associated with the same access token as in the update request.

A client can create, renew, or remove locks. To do so, it needs to call the
``UpdateLocks`` method with an ``UpdateLocksRequest``. The request contains the
access token and a `Struct
<https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Struct>`_.
with the state key associated with the lock to update as key, and either a
duration in seconds or a `Null value
<https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.NullValue>`_
as value. If the value is a duration, then the lock is created or renewed with
the requested validity duration. If the value is null, then the lock is deleted.
A lock can only be updated if it does not yet exist, if it exists but is
expired, or if it is hold by the same access token as the request. Each update
can be about one or multiple locks; a request only succeeds if all the locks can
be updated. If any of the locks cannot be updated, then none of the locks are
updated.

Security issues
~~~~~~~~~~~~~~~

The way to handle updates larger than a gRPC packet is undefined.
Servers may implement that case by shutting down, implementing solutions
that lead to a stale state or a degraded experience. This makes the
state service very susceptible to low effort denial of service attacks.

For now, no server and no client implement any form of encryption.
Therefore, the access tokens used to lock keys in the shared state
should be considered publicly exposed.

The trajectory service
----------------------

A server can broadcast molecular systems using the trajectory service.

Frame description
~~~~~~~~~~~~~~~~~

* a trajectory is a series of frames
* frames are described as ``FrameData``
* ``FrameData`` describe the topology and the atom positions
* a ``FrameData`` describe changes in the trajectory, they are merged into the
  current frame

.. code:: protobuf

    /* A general structure to represent a frame of a trajectory. It is similar in structure to the Google Struct message, representing dynamically typed objects and lists. However, as frame's often consist of large arrays of data of the same type, a set of arrays are also provided as specified in nanover/protocol/array.proto */
    message FrameData {

      /* A standard key-value list of dynamically typed data */
      map<string, google.protobuf.Value> values = 1;

      /* A key-value list of value arrays */
      map<string, nanover.protocol.ValueArray> arrays = 2;
    }

* a ``FrameData`` has values and arrays
* the meaning of the keys are described in the next section

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

* when part of a stream, FramaData is wrapped into a GetFrameResponse
* when the frame index is 0, the base frame needs to be reset

.. code:: protobuf

    /* A server response representing a frame of a molecular trajectory */
    message GetFrameResponse {

      /* An identifier for the frame */
      uint32 frame_index = 1;

      /* The frame of the trajectory, which may contain positions and topology information */
      nanover.protocol.trajectory.FrameData frame = 2;

    }

Field conventions
~~~~~~~~~~~~~~~~~

* particles
* residues
* segments
* forces
* velocities
* bonds

Subscribing to the latest frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: protobuf

    /* A service which provides access to frames of a trajectory, which may either be precomputed or represent a live simulation. It can also be used to obtain one or more frames on demand, allowing molecules or trajectories to be generated based on requests */
    service TrajectoryService {

      /* Subscribe to a continuous updating source of frames. The client gets the latest available frame at the time of transmission. */
      rpc SubscribeLatestFrames (GetFrameRequest) returns (stream GetFrameResponse);
    }

.. code:: protobuf

    /* A client request to get frame(s) from a trajectory service */
    message GetFrameRequest {

      /* Arbitrary data that can be used by a TrajectoryService to decide what frames to return */
      google.protobuf.Struct data = 1;

      /* Interval to send new frames at e.g 1/30 sends 30 frames every second. */
      float frame_interval = 2;
    }

Subscribing to all frames
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: protobuf

    /* A service which provides access to frames of a trajectory, which may either be precomputed or represent a live simulation. It can also be used to obtain one or more frames on demand, allowing molecules or trajectories to be generated based on requests */
    service TrajectoryService {

      /* Subscribe to a continuous updating source of frames. Frames are added to the stream when they are available */
      rpc SubscribeFrames (GetFrameRequest) returns (stream GetFrameResponse);
    }


Limitations
~~~~~~~~~~~

-  Frame size
-  Falling behind

The command service
-------------------

Listing available commands
~~~~~~~~~~~~~~~~~~~~~~~~~~

Running commands
~~~~~~~~~~~~~~~~

