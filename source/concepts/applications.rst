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

In the trajectory application, the server broadcasts molecular structures for
the clients to display. The molecular structures can be static structures or
snapshots of a trajectory; the protocol refer to these snapshots as frames. The
application is agnostic about the frames being generated on-the-fly or being
pre-calculated.

This application defines a set of fields to describes the semantic of molecular
systems with the ``FrameData``. It also defines a set of optional commands a
server can implement to give the clients some control over how the frames are
streamed. Finally, it defines some interactions with the multiplayer
application to share where to display the molecular system relative to the
users, and how to render the molecules.

Frames
~~~~~~

The :ref:`trajectory service <trajectory-service>` allows to stream snapshots
of arbitrary data to clients. Each snapshot is described in a :ref:`FrameData
<frame-description>` which contains a key-value map of protobuf `Values
<https://protobuf.dev/reference/protobuf/google.protobuf/#value>`_ and one of
homogeneous arrays. Here, we define a set of keys and data format to describe
the semantics of molecular systems.

.. note::

   A server using this set of keys can implement keys from another application
   as well. For instance, a server implementing the :ref:`iMD application
   <imd-application>` can implement both this set of keys and :ref:`iMD-specific
   keys <imd-framedata-keys>`.

All FrameData values used by the trajectory application use the following set
of units:

* lengths are expressed in nanometers (:math:`\text{nm}`)
* durations are expressed in picoseconds (:math:`\text{ps}`)
* masses are expressed in atomic mass unit (AMU)
* charges are expressed in proton charge
* energies are expressed in :math:`\text{kJ}\cdot\text{mol}^{-1}`
* velocities are expressed in :math:`\text{nm}\cdot{ps}^{-1}`
* forces are expressed in :math:`\text{kJ}\cdot\text{mol}^{-1}\cdot\text{nm}^{-1}`

The coordinate system is the right-handed, Z-up, system used in most software
working with molecular systems.

Particles
^^^^^^^^^

A molecular system is composed of atoms. The application refers to them as
"particles" to account for representations that do not deal with individual
atoms, such as coarse-grained models (`e.g.` `Martini <http://cgmartini.nl/>`_
or `SIRAH <http://www.sirahff.com/>`_). Particles are described by the following
keys in the array map:

* ``particle.positions``: the Cartesian coordinates of each particle. The
  coordinates are stored as a flat array of coordinates where each triplet
  corresponds to the XYZ coordinates of a particle.
* ``particle.velocities``: the velocity of each particle. Like the positions,
  they are expressed as a flattened array of triplets.
* ``particle.forces``: the force array applied to each particle, as a flattened
  array of triplets.
* ``particle.elements``: the chemical element for each particle expressed as
  atomic numbers. If a particle is not an atom, or if a chemical element is not
  relevant for any reason, the atomic number can be set to 0.
* ``particle.names``: a name for each particle. Each name is an arbitrary string
  to identify the particle, usually within a residue. If an atom does not have
  a name, set it to an empty string. When applicable, it is recommended to use
  the names used in the Protein Data Bank.

.. note::

   The application used to define a ``particle.types`` key for non-atomic
   systems where ``particle.elements`` was not appropriate. However, the key
   not being used lead to a lack of support. The key not having a clear meaning
   defined, has been removed from the application. However, the protocol allows
   the use of arbitrary keys so users of the application can reintroduce this
   key, or any more appropriate ones, for their own use cases.

If the FrameData uses any key staring by ``particle.``, it must set the key
``particle.count`` in the value map. The value of ``particle.count`` is the
number of particles in the frame, it must match the length of the arrays.

Residues
^^^^^^^^

Particles can be grouped in residues when the molecule is a polymer. A residue
is usually a monomer within the polymer sequence. Particles are assigned to
residues using the ``particle.residues`` key in the array map. Each value in
the array is the index of the residue of which the corresponding particle is a
part. The indices are indices in the following arrays:

* ``residue.names``: the name of each residue as arbitrary strings. The names
  are commonly the name of the monomer templates.
* ``residue.ids``: an identifier for the residue in the sequence. This ID is an
  arbitrary string. It is used to relate the residue with other data sources,
  such as the literature, the Protein Data Bank, or other data bases. This ID
  is often a numeric index starting at one and increasing monotonically. However,
  none of these properties should be relied upon. IDs can be strings
  representing negative numbers, for instance to convey that the residues have
  been alchemically added before the natural sequence of the polymer. There may
  be gap in the numerical sequence, for instance to convey that some residues
  are missing or if the IDs are shared with another sequence. The IDs may not
  represent numerical values whatsoever. Residue IDs should not be mistaken
  with the indices used in ``particle.residues``.

If the FrameData contains any array with a key staring with ``residue.``, it
must set a key ``residue.count`` in the value map. The value is the number of
residues and must match the length of the residue-related arrays. Indices in
the ``particle.residues`` array must be strictly lesser than the number of
residues. However, these indices may not refer to all of the residues. This
means it is possible to have residues with no particle attached to them. This
allows to filter particles out without having to modify the list of residues.

Chains
^^^^^^

Residues can be grouped by chains. There is not format semantic for chains
except that they are groups of residues. However, a chain is commonly either
(i) a complete set of residues connected by bonds or (ii) a complete set of
connected residues and residues not connected by bonds but related to the main
set. In both cases, missing residues count in the connectedness of the set. The
later case matches the meaning of a chain in the PDB format. To group residues
by chains, the FrameData must include the ``residue.chains`` key in the array
map with each value of the array being the index of the chain of which the
residue is a part. The FrameData also must set ``chain.count`` in the value map
with the number of chains that must match the number of element in the
``chain.name`` array. Chains may not have residues assigned to them. The
``chain.name`` array describes the name of each chain as arbitrary strings.

Bonds
^^^^^

Particles can be connected by covalent bonds. These bonds are described by two
keys in the array map of the FrameData:

* ``bond.pairs``: a flattened array of indices pairs. The indices reference the
  particles forming the pair in the arrays describing the particles.
* ``bond.orders``: an array of floating point numbers describing the bond order
  for each bond. A single bond is represented by a value of 1.0, a double bond
  a value of 2.0. Delocalised orbitals can be represented by non-integer
  values. This array must have half the size of the ``bond.pairs`` array with
  each value of bond order corresponding to a successive pair in the
  ``bond.pairs`` array. If this array is not present, the default bond order is
  1.0.

Simulation box
^^^^^^^^^^^^^^

Most molecular dynamics simulations are run in a sized box. The FrameData can
describe a triclinic box with its three box vectors. They are stored in the
array map under the ``system.box.vectors`` key as a flatten 3x3 matrix where
each row is a vector and each column is a dimension of the coordinate system.
The box is optional and should not be displayed if not provided.

Simulation time
^^^^^^^^^^^^^^^

If the frame corresponds to a given time in a simulation, this time can be
specified in picoseconds in the value map under the ``system.simulation.time``
key.

Energies
^^^^^^^^

The energy of the system for the frame can be stored in
:math:`\text{kJ}\cdot\text{mol}^{-1}` under the ``energy.kinetic``,
``energy.potential``, and ``energy.total`` key of the value map for the
kinetic, potential, and total energies, respectivelly. The total energy is
assumed to be the sum of the kinetic and potential energies.

Diagnostics
^^^^^^^^^^^

For diagnostics purpose, the time at which the frame has been generated, or
sent to the trajectory service, can be stored under the ``server.timestamp``
key in the value map. It is expressed as a fractional number of seconds. This
timestamp should only be used to compare with other timestamp in the same
stream as there is no requirement about the clock used to generate it.

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


.. _imd-application:

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

.. _imd-framedata-keys:

FrameData keys
~~~~~~~~~~~~~~

.. code::

  USER_ENERGY = "energy.user.total"
  forces.user.index
  forces.user.sparse

Velocity reset (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~

``imd.velocity_reset_available``

