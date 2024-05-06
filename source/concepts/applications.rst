Applications
============

The :ref:`NanoVer protocol <base-protocol>` defines how clients and servers
communicate with each other. It leaves ample room for customisation: it does
not define the content of a :ref:`FrameData <frame-description>`, the
meaning of the shared state keys is not defined either, nor does the protocol
specifies what the commands should be. This points are defined by applications.
Applications define how to use the different services and how to format the
content for specific tasks.

The multiplayer application
---------------------------

Clients that implement the multiplayer application can send and receive avatars
so users can share a virtual space. It is the core of multi-user use cases.

Each user that is visible to the others have :ref:`an avatar
<avatar-description>`, the characteristic of which it shares using the
:ref:`state service <state-service>`. An :ref:`origin
<user-origin-description>` can optionally be associated to a user. That origin
is a suggestion from the server to place a users relative to each other.
Finally, a user can optionally describe its :ref:`play space
<play-space-description>`, being the area around the user in which it is deemed
safe to move.

Avatars, user origins, and play spaces are linked to a user with a player ID.
This ID is an arbitrary string chosen by the user's client. Commonly, clients
use a `UUID4
<https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)>`_
to reduce the risk of collision between IDs produced by different clients.
However, any non-empty string is a valid player ID.

.. warning::

   An empty string is an invalid player ID only by convention. At this time, no
   server will prevent the use of one. However, an empty player ID is more
   likely to enter in collision between clients which could cause a client's
   avatar to be overwritten by another client.

A multiplayer application can optionally implement the :ref:`radial orient
<radial-orient>` method to place the avatars in a circle around a point.

Coordinate systems
~~~~~~~~~~~~~~~~~~

The multiplayer application distinguishes between two coordinate spaces:

* the game space is the coordinate space of the client. It is fully the
  responsibility of the client and the server is not aware of any of its
  details.
* the server space is the space in which all coordinate through the server are
  expressed. It is a left-handed, Y-up, coordinate space, with lengths
  expressed in meters. The origin of the height is on the floor. It is modeled
  after Unity's coordinate system.

The client is free to represent the server space anywhere in its game space.
Optionally, the server can suggest to a client where to place and how to orient
the game space relative to the server space with the :ref:`user-origin
<user-origin-description>` key.

.. _avatar-description:

Avatars
~~~~~~~

A client can expose an avatar to the other clients by periodically updating the
corresponding key in the :ref:`shared state <state-updates>`. Since client get
updates 30 times per seconds by default, 30 avatar updates per seconds is the
recommended update rate.

Avatars are represented in the shared state as a protobuf `Struct
<https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Struct>`_
under a key formatted as ``avatar.<PLAYER_ID>``.

Inside the Struct, an avatar refers to its player ID. It can also specify a
name and a color. The most important part of an avatar is the list of its
components. Components are elements of the avatar with a position and a rotation.

.. warning::

   The avatar specifies its player ID twice: in the top level key and with the
   ``playerid`` sub-key. Both places MUST match. A discrepency between the two
   is undefined behaviour. See `issue #98 in nanover-protocol
   <https://github.com/IRL2/nanover-protocol/issues/98>`_.

The name is an arbitrary string meant to be displayed to the other users as a
human-readable identifier. The color is also meant to be displayed to the other
users. The color is provided as a list of RGBA values between 0 and 1.

The expected components are the head and the two hands. An avatar can contain
other components, but they may not be supported by other clients. Each
component is a Struct with the following keys:

* ``name``, the predefined name of the component. The supported names are
  "head", "hand.right", and "hand.left".
* ``position``, a translation vector in server space expressed as a vector
  of 3 values.
* ``rotation``, the rotation of the component in server space expressed as
  a quaternion.

.. note::

   The avatar description currently only support VR controllers. See `issue #97 in
   nanover-protocol <https://github.com/IRL2/nanover-protocol/issues/97>`_ for
   hand-tracking support.

How to represent the avatar is the responsibility of the client. It must assume
that any of the information may be missing.

In summary, an avatar is structured as such:

.. code::

   avatar.<PLAYER_ID>: {
     components : [
       {
         name
         position: 
         rotation
       }
     ],
     playerid,
     name,
     color,
   }

.. _user-origin-description:

User origin
~~~~~~~~~~~

Avatars are shared in server space. Each client is responsible to locate its
server space wherever it prefers relative to its game space. However, the
server can suggest how to center the game space relative to the server space in
order to place the users according to each other. This is used by the
:ref:`radial orient <radial-orient>` server feature.

.. note::

   We assume the user origin is always provided by the server. However, it can
   come from a client so it is possible to implement a client that will place
   the users relative to each other folowwing arbitrary pattern. This can be
   used, for instance, to prototype alternative to the radial orient feature
   without mofifying the server.

The suggested user origin describes where the server suggests a given user
places the center of its game space and how to rotate that space. The
origin is described as a protobuf Struct under the key
``user-origin.<PLAYER_ID>`` where ``<PLAYER_ID>`` is the ID of the user to whom
the suggestion is addressed. The Struct has the following keys:

* ``position`` is the suggested location of the center for the user's game
  space in the server space;
* ``rotation`` is a quaternion describing the rotation of the user's game
  space in the server space.

A client may not follow the server suggestion and should not be assumed to do
so. If the key is absent from the shared state, the client may locate itself in
the server space as it chooses.

.. warning::

   A client has no way of knowing if the user origin emanates from a ligitimate
   source (i.e. the server or a trusted client). Therefore, a client could use
   this feature to move users without their conscent. This could cause
   discomfort if not used responsibly.

As a summary, the user origin is specified as follow in the shared state:

.. code::

   user-origin.<PLAYER_ID>: {
     position,
     rotation,
   }

.. _play-space-description:

Play space
~~~~~~~~~~

A client can share the shape of its play space with the others. A play space,
or play area, is the area the user can safely reach. This is mostly relevant
for VR clients which have to define such a safe space.

The play area is defined as four points, each as a vector of 3 XYZ values, in
server space, that form a quadrilateral. The play area is defined as a
Struct in the shared state under the key ``playarea.<PLAYER_ID>``. The points
are defined under the keys ``A``, ``B``, ``C``, and ``D``.

.. code::

   playarea.<PLAYER_ID>: {
      A,
      B,
      C,
      D,
    }

If they are available, a client can choose to represent them as they choose.

.. note::

   We assume that the points defining the play area are on the floor (Y=0).
   However, nothing forces a client to send them a such.

.. _radial-orient:

Radial orient
~~~~~~~~~~~~~

A server can, optionally, implement the radial orient feature as a command on
the :ref:`command service <command-service>`. The radial orient command places
all the avatars on a circle around the origin of the server space by
setting a :ref:`user origin <user-origin-description>` for each avatar.

The command is named ``multiuser/radially-orient-origins``. It takes a
``radius`` argument that is the distance, in meters, between the generated
centers and the center of the server space. The default radius is 1 meter.
The command does not return anything. This leads to the following signature:

.. code::

   multiuser/radially-orient-origins(radius = 1.0) -> None

Let a set of players :math:`P = \{P_0, P_1, ... P_{N - 1}\}`, :math:`N` the number of
players, and :math:`r` the radius given in argument. Then the center's position
:math:`C_i` for avatar :math:`i` is computed using polar coordinates converted
to Cartesian. Each avatar is assigned an angle :math:`\theta_i`:

.. math::

  \theta_i = \frac{i \times 2 \pi}{N}

Then the positions is:

.. math::

  \begin{align}
  C_i &= \begin{bmatrix}
    r\cos{\theta_i}\\
    0\\
    r\sin{\theta_i}\\
  \end{bmatrix}
  \end{align}

The rotation :math:`R_i` is expressed as a quaternion and is defined as:

.. math::

   \begin{align}
   R_i &= \begin{bmatrix}
     0\\
     \sin{\frac{1}{2} \big(-\theta_i - \frac{2\pi}{N}\big)}\\
     0\\
     \cos{\frac{1}{2} \big(-\theta_i - \frac{2\pi}{N}\big)}\\
    \end{bmatrix}
   \end{align}

The trajectory application
--------------------------

Frames
~~~~~~

.. code::

  BOX_VECTORS = "system.box.vectors"
  SIMULATION_TIME = "system.simulation.time"

  BOND_PAIRS = "bond.pairs"
  BOND_ORDERS = "bond.orders"

  PARTICLE_POSITIONS = "particle.positions"
  PARTICLE_VELOCITIES = "particle.velocities"
  PARTICLE_FORCES = "particle.forces"
  PARTICLE_ELEMENTS = "particle.elements"
  PARTICLE_TYPES = "particle.types"
  PARTICLE_NAMES = "particle.names"
  PARTICLE_RESIDUES = (
      "particle.residues"  # Index of the residue each particle belongs to.
  )
  PARTICLE_COUNT = "particle.count"

  RESIDUE_NAMES = "residue.names"
  RESIDUE_IDS = "residue.ids"  # Index of the chain each residue belongs to.
  RESIDUE_CHAINS = "residue.chains"
  RESIDUE_COUNT = "residue.count"

  CHAIN_NAMES = "chain.names"
  CHAIN_COUNT = "chain.count"

  KINETIC_ENERGY = "energy.kinetic"
  POTENTIAL_ENERGY = "energy.potential"
  TOTAL_ENERGY = "energy.total"
  USER_ENERGY = "energy.user.total"

  SERVER_TIMESTAMP = "server.timestamp"

  forces.user.index
  forces.user.sparse


Playback commands
~~~~~~~~~~~~~~~~~

* ``playback/play``
* ``playback/pause``
* ``playback/step``
* ``playback/reset``
* ``playback/load``
* ``playback/next``
* ``playback/list``

Simulation box (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

   scene

* position
* rotation
* scale


The iMD application
-------------------

User interactions
~~~~~~~~~~~~~~~~~

.. code::

  TYPE_KEY = "type"
  SCALE_KEY = "scale"
  MASS_WEIGHTED_KEY = "mass_weighted"
  RESET_VELOCITIES_KEY = "reset_velocities"
  MAX_FORCE_KEY = "max_force"

.. code::

   interaction.<INTERACTION_ID> {
       type,
       max_force,
       scale,
       particles,
       positions,
       mass_weighted,
       reset_velocities,
    }

Velocity reset (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~

``imd.velocity_reset_available``

