.. _applications:

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

The multi-user application
---------------------------

The multi-user application provides a shared virtual space in which users can
embody themselves with "avatars" and manipulate objects (e.g the simulation box
in MD).

Clients can broadcast avatar representations of themselves, information about
their range of motion within shared space (useful for VR), and receive a server
suggestion about how to position themselves relatives to other clients.

Each user chooses a unique "player ID" for themselves to distinguish the
ownership and applicability of the user information shared. Commonly, clients
use a `UUID4
<https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)>`_
to reduce the risk of collision between IDs produced by different clients.

.. _multiplayer-coordinate-systems:

Coordinate systems
~~~~~~~~~~~~~~~~~~

The multi-user application distinguishes between two coordinate spaces:

* The **server space** is the coordinate system of the shared virtual space,
  the 3d poses of avatars, the simulation box, and any other objects are
  exchanged in this coordinate space. The characteristics are chosen to match
  Unity's VR: left-handed, with Y-up, lengths expressed in meters, and the origin
  at floor level.
* A **client space**, the local coordinate space of a client, may differ from
  server space. For example, in VR the coordinate system may be fixed in physical
  space such that it can't be changed directly to match server space. The server
  is not aware of this and it is the client's responsibility to transform
  coordinates into server space before communicating them.

The client is free to represent the server space anywhere in its game space.
Optionally, the server can suggest to a client where to place and how to orient
the game space relative to the server space with the :ref:`user-origin
<user-origin-description>` key.

.. note::

   In MD applications there is an additional **simulation space** coordinate
   system. Its relation to the server space is determined by the position
   of the simulation box (via `scene` key) and iMD interactions use this
   coordinate space.


.. _avatar-description:

Avatars
~~~~~~~

Users may share their presence in the virtual space by creating and continuously
updating an "avatar". For example, in the iMD-VR application, each VR client
shares their head and hand positions for others to see.

Avatars are exchanged via the shared state as a protobuf `Struct
<https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Struct>`_
under keys of the form ``avatar.<PLAYER_ID>``. This avatar Struct details the
user's player ID, a name for the user, a display color, and the list of its
spatial components.

.. warning::

   The avatar specifies its player ID twice: in the top level key and with the
   ``playerid`` sub-key. Both places MUST match. A discrepancy between the two
   is undefined behaviour. See `issue #98 in nanover-server-py
   <https://github.com/IRL2/nanover-server-py/issues/98>`_.

The name is an arbitrary string typically displayed as a name tag to the other
users. The color, intended for distinguishing multiple avatars easily, is provided
as a list of RGBA component values between 0 and 1.

The typical components are a head and two hands. An avatar can contain other
components, but they may not be supported by other clients. Each component is
a Struct with the following keys:

* ``name``, the predefined name of the component. The supported names are
  "headset", "hand.right", and "hand.left".
* ``position``, a translation vector in server space expressed as a vector
  of 3 values.
* ``rotation``, the rotation of the component in server space expressed as
  a quaternion.

.. note::

   The avatar description currently only support VR controllers. See `issue #97 in
   nanover-server-py <https://github.com/IRL2/nanover-server-py/issues/97>`_ for
   hand-tracking support.

How to represent the avatar is the responsibility of the client, but it should
be careful to handle cases where some information or components are missing.

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

.. _play-space-description:

Play area
~~~~~~~~~~

A client, typically in the case of a VR client, can share the a rough
boundary within which the user can safely move. This is used to visually
indicate the range of motion for each user, and is especially useful for
colocation and seeing the results of the radial orientation function.

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

   Typically we assume that the points defining the play area are on the floor
   (Y=0). However, nothing forces a client to send them a such.

.. _radial-orient:

Radial orient
~~~~~~~~~~~~~

The radial orient feature is an command optionally implemented on the
:ref:`command service <command-service>`. This command suggests how clients
should position their avatars relative to server space such that all clients
are positioned in a circle around the origin. These suggestions are in
the form of a :ref:`user origin <user-origin-description>` for each avatar.

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

.. _user-origin-description:

User origin
~~~~~~~~~~~

A user-origin is a suggestion to the client of how to situate its coordinate
space (and therefore avatar) relative to server space. This is used by the
:ref:`radial orient <radial-orient>` server feature.

.. note::

   Any client can add user-origin keys. This can be used, for instance, to
   prototype alternative to the radial orient feature without modifying the server.

The suggested user origin describes where the server suggests a given user
places the center of its game space and how to rotate that space. The
origin is described as a protobuf Struct under the key
``user-origin.<PLAYER_ID>`` where ``<PLAYER_ID>`` is the ID of the user to whom
the suggestion is addressed. The Struct has the following keys:

* ``position`` is the suggested location of the center for the user's game
  space in the server space;
* ``rotation`` is a quaternion describing the rotation of the user's game
  space in the server space.

Client are free to ignore the user-origin suggestion and locate themselves in
the server space as they choose.

.. warning::

   Any client can add user-origin keys. If used without due care and
   responsibility a user in VR could get very nauseous.

As a summary, the user origin is specified as follow in the shared state:

.. code::

   user-origin.<PLAYER_ID>: {
     position,
     rotation,
   }


.. _multiplayer-update-index:

Update index
~~~~~~~~~~~~

If the client needs more precise knowledge of which of its updates have already
been received and rebroadcast to all clients, it can choose to maintain an
incrementing count of sent updates and store this in the shared state under
an ``update.index.<USER_ID>`` key. The client can then compare the remotely
received updates to this value with its internal count.


.. _trajectory-application:

The trajectory application
--------------------------

In the trajectory application, the server broadcasts molecular structures for
the clients to display. The molecular structures can be static structures or
snapshots of a trajectory; the protocol refers to these snapshots as frames. The
application is agnostic about the frames being generated on-the-fly or being
pre-calculated.

This application defines a set of fields to describe the semantics of molecular
systems within the ``FrameData``. It also defines a set of optional commands a
server can implement to give the clients some control over how the frames are
streamed. Finally, it defines some interactions with the multiplayer
application to share where to display the molecular system relative to the
users, and how to render the molecules.

Frames
~~~~~~

The trajectory application uses the :ref:`trajectory service <trajectory-service>`,
which allows a server to stream snapshots of arbitrary data to clients. Each snapshot is
described in a :ref:`FrameData <frame-description>` object, which contains:

* a key-value map of protobuf `Values <https://protobuf.dev/reference/protobuf/google.protobuf/#value>`_
* a key-value map of homogeneous arrays

Here, we define a set of keys and data formats to describe the semantics of
molecular systems.

.. note::

   A server using this set of keys can implement keys from another application
   as well. For instance, a server implementing the :ref:`iMD application
   <imd-application>` can implement both this set of keys and :ref:`iMD-specific
   keys <imd-framedata-keys>`.

All FrameData values used by the trajectory application use the following set
of units:

.. grid:: 3
   :gutter: 3

   .. grid-item::

   .. grid-item::
      .. list-table:: Units in NanoVer
         :widths: auto
         :header-rows: 1

         * - Quantity
           - Unit
         * - length
           - :math:`\text{nm}`
         * - time
           - :math:`\text{ps}`
         * - mass
           - atomic mass unit (AMU)
         * - charge
           - proton charge
         * - energy
           - :math:`\text{kJ}\cdot\text{mol}^{-1}`
         * - velocity
           - :math:`\text{nm}\cdot\text{ps}^{-1}`
         * - force
           - :math:`\text{kJ}\cdot\text{mol}^{-1}\cdot\text{nm}^{-1}`


   .. grid-item::


The coordinate system is the right-handed, Z-up, system used in most software
working with molecular systems.

.. important::

   The units used in NanoVer may differ from those used in the physics engine
   simulating the molecular system. This means that accessing a data field directly
   from the simulation itself may yield a different value to that delivered in the
   FrameData object generated for the same time step/configuration of the molecular
   system. **This is expected behaviour**.

   For example, for an :class:`ASESimulation` called :code:`ase_sim` and a
   NanoVer python client called :code:`client`:

   .. code-block:: python

      # Retrieve potential energy via ASE dynamics object directly (in ASE native units)
      ase_PE = ase_sim.dynamics.atoms.get_potential_energy()

      # Retrieve potential energy from the current frame (in NanoVer units)
      nanover_PE = client.current_frame.potential_energy


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

.. important::

   As the iMD application delivers system quantities separately from the interaction
   quantities, the key ``particle.forces.system`` is now used in place of
   ``particle.forces`` in iMD. The former contains the force array
   applied to each particle due to interactions from *within the molecular system*
   (i.e. excluding forces arising from iMD interactions).

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

If the FrameData uses any key starting with ``particle.``, it must set the key
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
the ``particle.residues`` array must be strictly less than the number of
residues. However, these indices may not refer to all of the residues. This
means it is possible to have residues with no particle attached to them. This
allows to filter particles out without having to modify the list of residues.

Chains
^^^^^^

Residues can be grouped by chains. There is no format semantic for chains
except that they are groups of residues. However, a chain is commonly either

(i) a complete set of residues connected by bonds, or
(ii) a complete set of connected residues and residues not connected by bonds but
     related to the main set.

In both cases, missing residues count in the connectedness of the set. The
latter case matches the meaning of a chain in the PDB format. To group residues
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
specified (in picoseconds) in the value map under the ``system.simulation.time``
key.

Energies
^^^^^^^^

The kinetic and potential energies of the system for the frame can be stored (in
:math:`\text{kJ}\cdot\text{mol}^{-1}`) under the ``energy.kinetic`` and
``energy.potential`` keys of the value map, respectively.

.. important::

   In the iMD application, the potential energy delivered under ``energy.potential``
   is the potential energy of the system *excluding* the potential energy associated
   with iMD interactions.

.. note::

   As :ref:`mentioned for particle velocities <leap-frog-warning>`, some
   molecular dynamics integrators compute velocities that are out of sync with the
   positions. This may cause the kinetic and the potential energies to be out of
   sync as well, depending on whether the velocities of the system are corrected
   for by the physics engine before the kinetic energy is calculated. It is up to
   the user to determine whether this is an issue for the integrator they employ
   in their chosen physics engine, and whether it is corrected for in any way.

.. warning::

   In the current implementation of iMD in NanoVer, when using OpenMM as a physics
   engine for molecular simulation *with* a
   :ref:`leapfrog algorithm <leap-frog-warning>`, the kinetic energy delivered
   *during an iMD interaction* differs marginally from the true kinetic energy of the
   system (see `Issue #324 <https://github.com/IRL2/nanover-server-py/issues/324>`_).
   This is not an issue when using the ASE as the physics engine with an
   :class:`OpenMMCalculator`.


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
  command controls whether the simulation or playback is advancing
  or not. The command does not take any argument and does not return anything.
* ``playback/pause() -> None``: pauses the simulation or playback. This command
  does not take any argument and returns nothing.
* ``playback/step() -> None``: advances simulation or playback until the next frame
  and then pause. No arguments, no return.
* ``playback/reset() -> None``: resets the simulation or playback to its initial
  state. If the frames are read from a pre-generated trajectory, it will start over
  from the first frame. If the trajectory is being generated on-the-fly, it
  will restart from the initial conditions. No arguments, no return.
* ``playback/list() -> {simulations: list of strings}``: returns the list of
  loadable simulations or recordings. Their names are arbitrary, user-facing
  strings for the sole purpose of identification. The list is returned
  under the ``simulations`` name. The command does not take any arguments.
* ``playback/load(index: int) -> None``: switches from the current system to the
  system corresponding to the index argument with respect to the available systems
  , as listed by the ``playback/list`` command. Indexing starts from 0. The command
  takes an integer as the ``index`` argument and returns nothing.
* ``playback/next() -> None``: switches from the current system to the next
  system in the list of available systems, as listed by the ``playback/list`` command.
  When called from the final system, cycles back to the first system.
  Note that the Rust server does not cycle back after the final system.
  This command does not take any arguments and does not return anything.

.. warning::

   At this time, the playback commands do not provide any error handling visible
   to the client. If a system fails to load, there is no client-side way to
   detect this.

Simulation box for multi user use cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the trajectory application is used in combination with the :ref:`multiplayer
application <multiplayer-application>`, the position and orientation of the
simulation box can be defined in the shared virtual space by means of the ``scene``
key in the :ref:`shared state <state-service>`. The clients and the server can
freely modify the ``scene`` key to reposition, reorient and resize the simulation box.

The value under that key is a list of numbers that merges
position of the box's origin, its rotation as a quaternion, and the scaling
compared to the default box size. These are expressed in the
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

   The scaling format technically supports non-uniform scales, however this is
   likely to cause rendering issues.

The ``scene`` key is likely to be modified often and by multiple users. To
avoid conflict, users should :ref:`lock <state-locks-description>` the key
before updating it.


.. _imd-application:

The iMD application
-------------------

For now, the main application of NanoVer is interactive molecular dynamics
(iMD) simulations, in  which a simulation runs on the server and users can
apply forces to particles on-the-fly. The iMD application builds on the capacity of the
:ref:`trajectory application <trajectory-application>` to provide live molecular
dynamics by defining the means to perform real-time interactions with the
simulation.

The application defines how to send user interactions to the server, the
expected behaviour of the server regarding these interactions, and how the
server can communicate the result of these interactions on the simulation to
the clients.

A user sends an interaction as a point of origin (in simulation space),
the particles to which it applies and a set of parameters. The server, then
collects all the user interactions, computes the corresponding forces and
propagates them with the other forces in the simulation.

Blueprint for quantitative iMD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`trajectory service <trajectory-service>` used by the
:ref:`trajectory application <trajectory-application>` (and thus by the iMD
application) allows users to choose a frame interval, an integer that specifies
the number of simulation steps to be performed by the physics engine between each
published frame. This can take an integer value :math:`n_{\text{f}} \geq 1`, and
by default is set to 5 in the iMD application. The frame interval enables a balance
to be struck between the accuracy of the numerical integration of the equations of
motion in the physics engine and the usability of the application for watching
the molecular simulation progress in real-time.

In the iMD application, clients can apply forces to the molecular simulation in
real-time. In order for any client connecting to a server to gain all of the
information relevant for quantitative analysis of the effect of iMD interactions
on the dynamics of the system on-the-fly, all implementations of the iMD application
in NanoVer are modelled on the following blueprint that describes how to progress
from one frame to the next:

1. Perform :math:`n_{\text{f}}` simulation steps
2. Use the final particle positions to calculate the iMD forces (and potential energies)
   to be applied to the molecular system during the next :math:`n_{\text{f}}` simulation
   steps
3. Publish a frame containing all of the information about the current state of
   the system (including any iMD forces calculated in step 2)

Steps 1--3 are iterated to perform an interactive iMD simulation in which all
quantitative information regarding the instantaneous state of the system and
all information about the iMD interactions applied to the system are delivered
to the clients connecting to the server. The iMD forces and energies calculated in step
2 remain constant throughout the following :math:`n_{\text{f}}` simulation steps,
so all clients know what iMD forces act on the simulation between consecutive frames.

Interactive forces
~~~~~~~~~~~~~~~~~~

The interactions can use different :ref:`equations <force-equations>` to
compute :math:`\mathbf{F}_{\text{COM}}`, the force at the center of mass of the group of
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

Each interaction type also defines the equation for the potential energy associated
with the user interaction :math:`E_{\text{COM}}`. For mass weighted interaction, the
energy for the interaction is :math:`E = \frac{E_{\text{COM}}}{N}\sum_{i=0}^{N}m_i`.
For non mass weighted :math:`E = E_{\text{COM}}`.

.. _force-equations:

Force equations
~~~~~~~~~~~~~~~

Each server is free to implement the interaction equation they choose. However,
there are some that are commonly implemented: the Gaussian force, the harmonic
(spring) force, and the constant force. They all depend on the vector :math:`\mathbf{d}` between
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
  :math:`\text{kJ}\cdot\text{mol}^{-1}\cdot\text{nm}^{-1}`.
* ``reset_velocities``: a boolean, true if :ref:`velocity reset
  <velocity-reset>` should be applied, false otherwise. This is false by
  default and will be ignored silently if the server does not have the feature.

.. warning::

   The Rust server does not currently support non-mass-weighted interactions.

.. note::

   The pure OpenMM server implementation does not support velocity reset at this
   time.

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

Some details about how the user interactions where applied are added to the
:ref:`FrameData <frame-description>`.

Each of the interactions applied to the molecular system by a user in the iMD
application has an associated potential energy. As multiple users can interact
simultaneously with the same atom(s), the resultant iMD force applied to the each
atom is a sum of the individual forces applied by the users. Similarly, the iMD
potential energy associated with the resultant forces is a sum of all of the iMD
potentials applied to the system by the users. Both the potential energy and the
resultant forces associated with iMD interactions are delivered to the user in
the FrameData. These quantities are only non-zero during user interactions.

To distinguish the contributions to the overall potential energy of the
simulation, the iMD application delivers the potential energy associated with
interactions within the molecular system itself *separately* from the iMD potential
energy, under the following keys:

* ``energy.potential``: the potential energy of the molecular system
  (i.e. without iMD interactions)
* ``energy.user.total``: the total iMD potential energy (i.e. the sum of the
  potential energies of all current user interactions)

Both of these energies are delivered in units of :math:`\text{kJ}\cdot\text{mol}^{-1}`.

Similarly, to distinguish the contributions to the total forces acting on the atoms
in the simulation, the iMD application delivers the forces associated with interactions
within the molecular system *separately* from the resultant forces from iMD interactions,
under the following keys:

* ``particle.forces.system``: the force array applied to each particle resulting from
  interactions within the molecular system (i.e. without iMD forces), as a flattened
  array of triplets.
* ``forces.user.index``: a 1-D array of indices (with :math:`n` elements) of the particles
  to which iMD forces are being applied.
* ``forces.user.sparse``: the force array applied to each particle for a subset of
  particles, resulting from iMD interactions (i.e. the total iMD forces applied to
  specific atoms in the molecular system), as a flattened array of triplets (with
  :math:`3n` elements). The particles to which the forces are applied are specified by
  the indices in ``forces.user.index`` (more on this below).

Both force arrays are delivered in units of :math:`\text{kJ}\cdot\text{mol}^{-1}\text{nm}^{-1}`.

As the user interactions usually apply only to a small subset
of the particles, it would be wasteful to provide the forces for all the particles
in the FrameData, as most would be null. Instead, the user forces are transmitted in
a sparse way by indicating which particles are affected with ``forces.user.index``,
whose entries are the indices of the particles affected by the iMD force,
corresponding to the indexing in the particle arrays (`e.g.` ``particle.positions``).
The ``forces.user.sparse`` key contains the corresponding forces applied to these particles
as a flattened array of triplets. The order of the elements of ``forces.user.index`` correspond to the
order of the triplets stored in ``forces.user.sparse``.

In addition to delivering information about the forces and potential energies associated
with the iMD interactions applied to the molecular simulation, the iMD application also
calculates the cumulative work done on the molecular system by the iMD interactions,
delivered under the following key:

* ``forces.user.work_done``: the cumulative work done on the molecular system by all iMD
  forces applied to the system.

The user work done is delivered in the same units as the potential energies, i.e.
:math:`\text{kJ}\cdot\text{mol}^{-1}`.

.. _velocity-reset:

Velocity reset
~~~~~~~~~~~~~~

Some server implementations can kill any residual momentum in the system due to the user-applied forces after the user interaction has ended
by setting the velocities of the affected particles to 0. This is called velocity
reset and can be requested by the user as part of the interaction description.

Servers that have the ability to do velocity reset should advertise the feature
by setting the ``imd.velocity_reset_available`` key to true in the :ref:`shared
state <state-service>`.

Miscellaneous applications
--------------------------

For diagnostics purpose, the time at which a frame has been generated, or
sent to the trajectory service, can be stored under the ``server.timestamp``
key in the value map. It is expressed as a fractional number of seconds. This
timestamp should only be used to compare with other timestamp in the same
stream as there is no requirement about the clock used to generate it.
