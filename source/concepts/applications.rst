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

Clients that implement the multiplayer application can send and recieve avatars
so users can share a virtual space.

Avatars
~~~~~~~

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


User origin
~~~~~~~~~~~

.. code::

   user-origin.<PLAYER_ID>: {
     position,
     rotation,
   }

Play space
~~~~~~~~~~

Radial orient (optional)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

   multiuser/radially-orient-origins(radius = 1.0) -> None

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

