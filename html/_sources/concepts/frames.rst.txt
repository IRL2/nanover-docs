Trajectories and Frames
=======================

An N-body simulation, such as a molecular dynamics simulation, fundamentally consists of a set of **frames** - snapshots
of the system describing the particles and their positions. A **trajectory** is a set
of these frames, forming a three dimensional 'movie'. Simulations are essentially
trajectories which are being generated on the fly.

Each frame consists of information about the system and the atoms within it. This
data takes the form of values related to the frame (such as the system's temperature
or energy) and arrays storing information about the atoms themselves (such as position
or element).

The approach taken by NanoVer is to use a key value system to store frames, as what is 
available in a frame varies dramatically based on what is being simulated. NanoVer applications
use a set of standard keys to define common fields, such as 'particle_positions' for the the field
containing the coordinates of the particles in the system. See the python implementation of `FrameData <../../python/nanover.trajectory.frame_data>`_ 
or some of our `conversion <../../python/nanover.openmm.converter>`_  utilities for more examples.

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
integer, byte, float, string, or a JSON like Struct. 
