======
OpenMM
======

.. contents:: Contents
    :depth: 2
    :local:

Openmm Tutorials
==============================================
A set of tutorials that demonstrate how to use NanoVer to run interactive molecular
dynamics simulations using OpenMM directly.

The Jupyter notebook tutorials that demonstrate how to run interactive molecular
dynamics simulations by interfacing NanoVer with OpenMM directly can be found in
the `examples <https://github.com/IRL2/nanover-protocol/tree/main/examples/openmm>`_
folder of the GitHub repository. It contains:

* `openmm_polyalanine`: A notebook that demonstrates how to set up an interactive
  OpenMM simulation from scratch with NanoVer, use features of OpenMM in conjunction
  with NanoVer, and record & playback simulations directly using NanoVer.
* `openmm_nanotube`: A notebook that demonstrates how to interact with an OpenMM
  NanoVer simulation using a python client.
* `openmm_neuraminidase`: A notebook that demonstrates how to set up an interactive
  OpenMM simulation from scratch with NanoVer and change the visualisations of
  different atom selections for a protein-ligand system.

Openmm XML Files
==============================================

The XML format described here is used specifically for manipulating NanoVer simulations from OpenMM serialized XML files. It consists of a root element ``<OpenMMSimulation>`` containing three main components:

1. **Starting Structure**: Enclosed in either ``<pdbx>`` or ``<pdb>`` tags
2. **OpenMM Serialized System**: Enclosed in the ``<System>`` tag
3. **OpenMM Serialized Integrator**: Enclosed in the ``<Integrator>`` tag

An optional fourth component, the OpenMM serialized state, may also be included.
The format allows for efficient storage and exchange of OpenMM simulation data, including the starting structure, system configuration, and integrator settings.

XML structure
-------------

.. code-block:: xml

    <OpenMMSimulation>
        <pdbx>
            <!-- Content of the PDBx file -->
        </pdbx>
        <System ...>
            <!-- XML content of the OpenMM serialized system -->
        </System>
        <Integrator ...>
            <!-- XML content of the OpenMM serialized integrator -->
        </Integrator>
    </OpenMMSimulation>

Components description
----------------------

1. **Starting structure**:
^^^^^^^^^^^^^^^^^^^^^^^^^^

   * Tag: ``<pdbx>`` (preferred) or ``<pdb>`` (for backward compatibility)
   * Content: The entire PDBx or PDB file content

2. **OpenMM serialized system**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within this tag, you'll find:

    **Particles:** They are represented with ``<Particle>`` tags, each containing:

        - Mass
        - Charge (if using a `NonbondedForce`)

    **Forces:** Various force components are represented by specific tags (a detailed list could be found `here <http://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#standard-forces>`_), for example:

        - ``<HarmonicBondForce>``: For bond stretching
        - ``<HarmonicAngleForce>``: For angle bending
        - ``<PeriodicTorsionForce>``: For dihedral angles
        - ``<NonbondedForce>``: For electrostatic and van der Waals interactions
        - ``<CustomNonbondedForce>``: For user-defined nonbonded interactions

        Each force tag contains parameters specific to that force type. For example:

        .. code-block:: xml

           <HarmonicBondForce>
             <Bond p1="0" p2="1" length="0.1" k="1000"/>
           </HarmonicBondForce>

    **Constraints:** If present, constraints are listed under a ``<Constraints>`` tag:

        .. code-block:: xml

           <Constraints>
             <Constraint p1="0" p2="1" distance="0.1"/>
           </Constraints>


3. **OpenMM serialized integrator**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``<Integrator>`` tag contains parameters that specify the integration method to be used to simulate dynamics, such as the type of integrator, simulation time step and temperature:

.. code-block:: xml

    <Integrator type="LangevinIntegrator" constraintTolerance="1e-05" friction="4" randomSeed="0" stepSize=".0005" temperature="300" version="1" />

More details on integrators can be found `here <http://docs.openmm.org/latest/userguide/theory/04_integrators.html>`_.

Usage
-----

The :mod:`nanover.openmm.serializer` module provides the ``serialize_simulation`` and ``deserialize_simulation`` functions which allow saving and loading OpenMM simulations to/from XML files. The serialization captures the complete simulation state including:

- Structure coordinates and topology (as PDBx/PDB)
- OpenMM System definition
- Integrator configuration

Serializing a simulation
^^^^^^^^^^^^^^^^^^^^^^^^

To save a simulation to an Openmm XML::

    xml_string = nanover.openmm.serializer.serialize_simulation(simulation)

    with open("sim.xml", "w") as f:
        f.write(xml_string)

Deserializing a simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^

To load a simulation from an Openmm XML::

    with open("sim.xml", "r") as f:
        simulation = nanover.openmm.serializer.deserialize_simulation(f.read())

The ``deserialize_simulation`` function accepts optional arguments:

- ``imd_force``: A CustomExternalForce for interactive molecular dynamics
- ``platform_name``: The OpenMM platform to use (e.g. "CUDA", "OpenCL")

For example::

    simulation = nanover.openmm.serializer.deserialize_simulation(
        xml_string,
        platform_name="CUDA"
    )


