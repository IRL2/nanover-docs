Applications
============

The :ref:`NanoVer protocol <base-protocol>` defines how clients and servers
communicate with each other. It leaves ample room for customisation: it does
not define the content of a :ref:`FrameData <frame-description>`, the
meaning of the shared state keys is not defined either, nor does the protocol
specifies what the commands should be. This points are defined by applications.
Applications define how to use the different services and how to format the
content for specific tasks.

.. _multiplayer-application:

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

.. _multiplayer-coordinate-systems:

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
  "headset", "hand.right", and "hand.left".
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
:math:`\mathbf{C}_i` for avatar :math:`i` is computed using polar coordinates converted
to Cartesian. Each avatar is assigned an angle :math:`\theta_i`:

.. math::

  \theta_i = \frac{i \times 2 \pi}{N}

Then the positions is:

.. math::

  \begin{align}
  \mathbf{C}_i &= \begin{bmatrix}
    r\cos{\theta_i}\\
    0\\
    r\sin{\theta_i}\\
  \end{bmatrix}
  \end{align}

The rotation :math:`\mathbf{R}_i` is expressed as a quaternion and is defined as:

.. math::

   \begin{align}
   \mathbf{R}_i &= \begin{bmatrix}
     0\\
     \sin{\frac{1}{2} \big(-\theta_i - \frac{2\pi}{N}\big)}\\
     0\\
     \cos{\frac{1}{2} \big(-\theta_i - \frac{2\pi}{N}\big)}\\
    \end{bmatrix}
   \end{align}

.. _trajectory-application:

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

.. _leap-frog-warning:

.. warning::

   Many molecular dynamics integrators are based on the leap frog integration
   method that calculates the velocities at the half time step. Simulation engines
   will typically report these half step velocities with the forces and the
   positions for the time step. Except in specific implementations, the
   FrameData will report the velocities in the same way as the simulation
   engine.

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
array map under the ``system.box.vectors`` key as a flattened 3x3 matrix where
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

.. note::

   Like :ref:`mentionned about particle velocities <leap-frog-warning>`, some
   molecular dynamics integrators use velocities computed out of sync of the
   positions. This may cause the kinetic and the potential energies to be out of
   sync as well. This is, however, a very common behaviour that can be ignored in
   most cases.

Playback indicators
^^^^^^^^^^^^^^^^^^^

The trajectory application defines commands that allow resetting or loading a
simulation. These keys in the value map allow to keep track of these reset and
load events:

* ``system.reset.counter`` is a counter of how many reset events occurred so far. It
  starts at 0 and is incremented whenever the simulation is reset, either from the
  reset command described below or from any other event.
* ``system.simulation.counter`` counts how many loading events occurred after the
  initial one. The counter starts at 0 and is incremented when a simulation is loaded
  after the initial one.

Playback commands
~~~~~~~~~~~~~~~~~

A trajectory application can define the following commands in the :ref:`command
service <command-service>` to control the stream of frames:

* ``playback/play() -> None``: in combination with ``playback/pause``, this
  command controls if new frames are being generated or not. The command does
  not take any argument and does not return anything.
* ``playback/pause() -> None``: pauses the generation of frames. This command
  does not take any argument and returns nothing.
* ``playback/step() -> None``: generate the next frame and pause the frame
  generation. No arguments, no return.
* ``playback/reset() -> None``: reset the frame generation from the beginning.
  If the frames are read from a pre-generated trajectory, it will start over
  from the first frame. If the trajectory is being generated on-the-fly, it
  will restart from the initial conditions. No arguments, no return.
* ``playback/list() -> {simulations: list of strings}``: if the server allows
  switching between molecular systems, this command returns the list of
  available systems. The order of the systems must match the indices used by
  ``playback/load``. The list contains arbitrary names that allow to identify
  these systems. They are aimed at being read by humans. The list is returned
  under the ``simulations`` name. The command does not take any arguments.
* ``playback/load(index: int) -> None``: if the server allows switching between
  molecular systems, this command requests the system with the given index to be
  loaded as the current system. The command takes an integer as the ``index``
  argument and returns nothing. If the client does not provide an index,
  provides a misformatted index, or provides an invalid index, the command is
  ignored silently. The bahaviour in case the index is valid but the system
  could not be loaded is undefined.
* ``playback/next() -> None``: if the server allows switching between molecular
  systems, this command requests the simulation with the next index to be
  loaded as the current simulation. The server is free to cycle through the
  available systems or ignore the command when the current system is the last
  available one. The behaviour when the system fails to load is undefined.

.. note::

   There is no command defined to toggle between playing and pausing the frame
   generation. This is on purpose as such a toggle command would be prone to
   race conditions when multiple clients call play/pause commands close to each
   other in time.

.. warning::

   The playback commands do not define any error handling. The commands to
   switch among molecular systems can be silently ignored and a failure to load
   a system, which is a probable event, has no defined behaviour.

Simulation box for multi user use cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the trajectory application is used in combination with the :ref:`multiplayer
application <multiplayer-application>`, it can share where the simulation box
should be placed relative to the avatar.

The clients or the server can set the ``scene`` key in the :ref:`shared state
<state-service>`. The value under that key is a list of numbers that merges
position of the box's origin, its rotation as a quaternion, and the scaling
compared to the default box size in each dimension. These are expressed in the
:ref:`server coordinate system <multiplayer-coordinate-systems>`.

By default:

* the origin of the simulation space is set at the origin of the server space
  (`i.e.` the position is ``[0, 0, 0]``);
* the Y and Z axes of the simulation space match the Y and Z axis of the server
  space, respectively; the X axis of the simulation space is reversed compared
  to the one of the server space, so positive X values in simulation space
  correspond to negative X values in the server space. This corresponds to a
  ``[0, 0, 0, 1]`` quaternion.
* 1 nanometer in simulation space corresponds to 1 meter in server space
  (`i.e.` the scale is ``[1, 1, 1]``). Negative scale values are not permitted.

The default ``scene`` value is therefore ``[0, 0, 0, 0, 0, 0, 1, 1, 1, 1]``.

Client should ignore invalid values and fallback to the default value when they
are encountered. Invalid values can be of the wrong type, be a list of the
wrong length, or include negative scale values.

.. note::

   The server space is Y-up while the simulation space is Z-up. However, the
   default orientation of the box matches the XY axes of both space so clients
   are expected to represent the simulation Y-up. In cases where the up
   orientation of the simulation space is meaningful, the simulation space must
   be rotated by setting the ``scene`` key rather than by altering the default
   orientation.

.. warning::

   The scale can be set to any value but it must be set to 3 identical
   values for the simulation space to keep its aspect ratio.

The ``scene`` key is likely to be modified often and by multiple users. To
avoid conflict, users should :ref:`lock <state-lock-description>` the key
before updating it.


.. _imd-application:

The iMD application
-------------------

For now, the main application of NanoVer is interactive molecular dynamics
simulations (iMD). A simulation runs on the server and users can apply forces
to particles on-the-fly.

The iMD application defines how to send user interactions to the server, the
expected behaviour of the server regarding these interactions, and how the
server can communicate the result of these interactions on the simulation to
the clients.

The application assumes it is used in conjunction with the :ref:`trajectory
application <trajectory-application>` or a similar enough application to share
the simulation itself.

A user sends an interaction as a point of origin, the particles to which it
applies and a set of parameters. The server, then collects all the user
interactions, computes the corresponding forces and propagates them with the
other forces in the simulation.

The interactions can use different :ref:`equations <force-equations>` to
compute the force :math:`\mathbf{F}_{\text{COM}}` to the center of mass of the group of
target particles. The force is then distributed among the particles; 
the method of force distribution depends on whether 
the interaction is mass weighted of not. If if it mass weighted, then the
force :math:`\mathbf{F}_i` applied to the particle :math:`i` is :math:`\mathbf{F}_i = s \cdot m_i
\frac{\mathbf{F}_{\text{COM}}}{N}` with :math:`s` a scaling factor set by the user,
:math:`m_i` the mass of particle :math:`i`, and :math:`N` the number of target
particles for the interaction. If the interaction is not mass weighted, then
:math:`\mathbf{F}_i = s \cdot \frac{\mathbf{F}_{\text{COM}}}{N}`. Finally, :math:`|\mathbf{F}_i|` can be
capped to a maximum value specified by the user to avoid applying too large
forces.

Each interaction type also defines the equation for the energy associated with the user interaction
:math:`E_{\text{COM}}`. For mass weighted interaction, the energy for the
interaction is :math:`E = \frac{E_{\text{COM}}}{N}\sum_{i=0}^{N}m_i`. For non
mass weighted :math:`E = E_{\text{COM}}`.

.. _force-equations:

Force equations
~~~~~~~~~~~~~~~

Each server is free to implement the interaction equation they choose. However,
there are some that are commonly implemented: the Gaussian force, the harmonic
force, and the constant force. They all depend on the vector :math:`\mathbf{d}` between
the origin of the interaction, :math:`\mathbf{r}_{\text{user}}`, and the center of mass
of the set of target particles :math:`\mathbf{r}_{\text{COM}}`. So, :math:`\mathbf{d} =
\mathbf{r}_{\text{user}} - \mathbf{r}_{\text{COM}}`.

The Gaussian force is defined by:

.. math::

   \begin{align}
      \mathbf{F}_{\text{COM}}^{\text{Gaussian}} &= -\frac{\mathbf{d}}{\sigma^2}\exp{-\frac{| \mathbf{d} | ^2}{2\sigma^2}} \\
      E_{\text{COM}}^{\text{Gaussian}} &= - \exp{-\frac{| \mathbf{d} |^2}{2\sigma^2}}
   \end{align}

with :math:`\sigma = 1`. With this force, the user interaction is stronger when
applied close to the particles.

The harmonic force is defined by:

.. math::

   \begin{align}
   \mathbf{F}_{\text{COM}}^{\text{Harmonic}} &= -k \mathbf{d} \\
   E_{\text{COM}}^{\text{Harmonic}} &=  \frac{1}{2}k| \mathbf{d} |^2
   \end{align}

with :math:`k = 2`.

The constant force is defined by:

.. math::

   \begin{align}
    \mathbf{F}_{\text{COM}}^{\text{Constant}} &=
    \begin{cases}
      (0, 0, 0),& \text{if } | \mathbf{d} | = 0 \\
      \frac{ \mathbf{d} }{| \mathbf{d} |},& \text{otherwise}
    \end{cases} \\
    E_{\text{COM}}^{\text{Constant}} &= 
    \begin{cases}
      0,& \text{if } | \mathbf{d} | = 0 \\
      1,& \text{otherwise}
    \end{cases}
   \end{align}

The direction of the constant force is undefined when the origin of the
interaction and the center of mass of the selection overlap, so the force is
not applied.

.. _velocity-reset:

Velocity reset
~~~~~~~~~~~~~~

Some server implementations can kill any residual momentum in the system due to the user-applied forces after the user interaction has ended
by setting the velocities of the affected particles to 0. This is called velocity
reset and can be requested by the user as part of the interaction description.

Servers that have the ability to do velocity reset should advertise the feature
by setting the ``imd.velocity_reset_available`` key to true in the :ref:`shared
state <state-service>`.

Sending user interactions
~~~~~~~~~~~~~~~~~~~~~~~~~

Users send, on the :ref:`shared state <state-service>`, the description of the
interactions they want to apply. There is no limit to the number of interaction
a user can send. Each interaction is described under the key
``interaction.<INTERACTION_ID>`` where ``<INTERACTION_ID>`` is an arbitrary
string, unique to the interaction, used to identify it. It is commonly a UUID4.
Under that key, the value is a Struct with the following keys:

* ``positions``: the coordinates of the interaction's origin in simulation
  space. This is typically a position attached to the controller of the user in
  VR, but it does not have to be. By default, this is `[0, 0, 0]`.
* ``particles``: the indices of the affected particles in the array of
  particles used by the :ref:`trajectory application <trajectory-application>`.
  If the order in this array does not match the order used by the simulation
  engine, it is the server's responsibility to map them. The default value is
  an empty list.
* ``type``: the type of interaction to apply, this is what defines which
  :ref:`force equation <force-equations>` will be used. It should be set to
  `gaussian` for the Gaussian force, `spring` for the harmonic force, and
  `constant` for the constant force. Interactions with an type unknown to the
  server will be ignored silently. By default, the Gaussian force is assumed.
* ``scale``: the scaling factor :math:`s` to apply to the force. The default
  scale is 1.
* ``mass_weighted``: a boolean, true if the interaction is mass weighted, false
  otherwise. The default is true.
* ``max_force``: the maximum force magnitude that can be applied to a particle
  by this interaction. The default is 20,000
  :math:`kJ\cdot\text{mol}^{-1}\cdot\text{nm}^{-1}`.
* ``reset_velocities``: a boolean, true if :ref:`velocity reset
  <velocity-reset>` should be applied, false otherwise. This is false by
  default and will be ignored silently if the server does not have the feature.

If the iMD application is used in conjunction with the :ref:`multiplayer
application <multiplayer-application>`, then the interaction can also use the
following fields:

* ``owner.id``: if the interaction originates from a client that defines an
  avatar, it can set this field to the player id attached to its avatar. This
  allows one to match interactions with avatars when analysing session recordings.
* ``label``: used with ``owner.id``, this is the name of the avatar component
  from which the interaction originates (`e.g.` ``hand.right`` or
  ``hand.left``).

.. _imd-framedata-keys:

FrameData keys
~~~~~~~~~~~~~~

Some details about how the user interactions where applied can be added to the
:ref:`FrameData <frame-description>`.

The sum of the energies from user interactions can be included, in
:math:`\text{kJ}\cdot\text{mol}^{-1}`, under the ``energy.user.total`` key in
the value map. Depending on the implementations, this energy may or may not be
included in the total energy included by the :ref:`trajectory application
<trajectory-application>` under the ``energy.total`` key.

The forces applied to each particle by the interactions can be stored under the
``forces.user.index`` and ``forces.user.sparse`` in the array map. Because the
user interactions usually apply only to a small subset of the particles, it is
wasteful to provide the forces for all the particles as they would be null for
most of them. Instead, the user forces are transmitted in a sparse way by
indicating which particles are affected with ``forces.user.index`` that will
list the indices in relation of the particle arrays (`e.g.`
``particle.positions``). The ``forces.user.sparse`` key contains the forces for
the these particles in the same order as the ``forces.user.index`` as a flatten
array.

Miscellaneous applications
--------------------------

Some clients or servers may use their own keys in the :ref:`state
<state-service>` or :ref:`trajectory <trajectory-service>` services. These keys
are not formally part of any application, but documenting their meaning can
only improve interoperability among the implementations.

For diagnostics purpose, the time at which a frame has been generated, or
sent to the trajectory service, can be stored under the ``server.timestamp``
key in the value map. It is expressed as a fractional number of seconds. This
timestamp should only be used to compare with other timestamp in the same
stream as there is no requirement about the clock used to generate it.

A client can send an internal index of the updates it sends under the
``update.index.<USER_ID>`` key in the shared state; where ``<USER_ID>`` can be
the player id used in the :ref:`multiplayer application
<multiplayer-application>` or any string unique to the client. The index is the
index of the update to be sent by the client in its own internal counter. By
receiving this value in the update stream, the client can know which of its
updates have been acknowledged by the server.
