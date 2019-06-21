Trajectories and Frames
=======================

An atomic simulation fundamentally consists of a set of **frames** - snapshots
of the system describing the atoms and their positions. A **trajectory** is a set
of these frames, forming a three dimensional 'movie'. Simulations are essentially
trajectories which are being generated on the fly.

Each frame consists of information about the system and the atoms within it. This
data takes the form of values related to the frame (such as the system's temperature
or energy) and arrays storing information about the atoms themselves (such as position
or element).
