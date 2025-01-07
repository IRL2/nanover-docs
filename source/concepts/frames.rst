.. _traj-and-frames:

=======================
Trajectories and Frames
=======================

An N-body simulation, such as a molecular dynamics simulation, fundamentally consists of a set of **frames** - snapshots
of the system describing the particles and their positions. A **trajectory** is a set
of these frames, forming a three dimensional 'movie'. Simulations are essentially
trajectories which are being generated on the fly.

Each frame consists of information about the system and the atoms within it. This
data takes the form of **values** related to the frame (such as the system's instantaneous temperature
or potential energy) and **arrays** storing information about the atoms themselves (such as position
or element symbol). Some of these data are updated each frame as the simulation progresses (such
as particle positions, simulation time or system potential energy) whilst others remain constant
throughout the simulation (such as element type or number of particles). NanoVer handles this by
only updating values or arrays that change between frames; to find out more about
this, please refer to :ref:`frame-description`.

The approach taken by NanoVer is to use a key-value system to store frames, as what is
available in a frame varies dramatically based on what is being simulated. NanoVer applications
use a set of standard keys to define common fields, such as 'particle_positions' for the the field
containing the coordinates of the particles in the system. See the python implementation of
:py:class:`FrameData <nanover.trajectory.frame_data.FrameData>`
or some of our :py:mod:`conversion <nanover.openmm.converter>`  utilities for more examples.

For a basic interactive molecular simulation, a frame typically has the following fields:

* Particle positions (we always use nanometers!)
* Particle elements
* Bond pairs 

For a simulation of a protein, a frame will have additional fields, such as:

* Particle residues
* Residue names
* Residue IDs
* Residue chains 
* Chain names

While in a QM calculation, we may have: 

* Bond orders 

If you need to customize a frame with your own data, you can - just pick a good key by which to identify
it, and convert your data into either an array of integers, bytes, floats, strings, or a single value type such as 
integer, byte, float, string, or a JSON like `Struct
<https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Struct>`_.

To learn more about the types of data you can send in a frame, or to see how to add data to a frame in practice,
take a look at our `frame` tutorial notebook (see :ref:`nanover-fundamentals`).

|

