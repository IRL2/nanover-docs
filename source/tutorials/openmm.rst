======
OpenMM
======

.. contents:: Contents
    :depth: 2
    :local:

OpenMM Tutorials
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

OpenMM XML Files
==============================================

The XML format described here is used specifically for saving and loading NanoVer OpenMM simulations. It consists of a root element ``<OpenMMSimulation>`` containing three main components:

1. **Starting Structure**: Enclosed in either ``<pdbx>`` or ``<pdb>`` tags
2. **OpenMM Serialized System**: Enclosed in the ``<System>`` tag
3. **OpenMM Serialized Integrator**: Enclosed in the ``<Integrator>`` tag
4. **OpenMM Serialized State**: Enclosed in the ``<State>`` tag (optional)

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
        <State ...>
            <!-- XML content of the OpenMM serialized state -->
        </State>
    </OpenMMSimulation>

.. note::
    There is a slight difference between the OpenMM format and the NanoVer format.
    NanoVer xml files for OpenMM simulations contain a PDB and a number of serialized objects.
    Although the serialized objects are identical to those used by OpenMM, the overall contents and structure of the files are specific to NanoVer and cannot be read by OpenMM on its own.


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

    **Forces:** Various force components are represented by specific tags (a detailed list could be found in this `link <http://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#standard-forces>`_), for example:

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

4. **OpenMM serialized state**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``<State>`` tag contains the serialized state of the simulation, including:

- Particle velocities ``<Velocities>``
- Adjustable parameters that have been defined by Force objects in the System ``<Parameters>``
- Periodic box vectors (if periodic boundary conditions are used) ``<PeriodicBoxVectors>``
- Integrator parameters ``<IntegratorParameters>``

Usage
-----

The :mod:`nanover.openmm.serializer` module provides the ``serialize_simulation`` and ``deserialize_simulation`` functions which allow saving and loading OpenMM simulations to/from XML files. The serialization captures by default the complete simulation including:

- Structure coordinates and topology (as PDBx/PDB)
- OpenMM System definition
- Integrator configuration
- Serialized state (optional)

Serializing a simulation
^^^^^^^^^^^^^^^^^^^^^^^^

To save a simulation to a NanoVer OpenMM XML::

    xml_string = nanover.openmm.serializer.serialize_simulation(simulation)

    with open("sim.xml", "w") as f:
        f.write(xml_string)

The ``serialize_simulation`` function accepts optional arguments:

- ``save_state``: Whether to include the serialized state in the XML (default: ``False``)

Deserializing a simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^

To load a simulation from a NanoVer OpenMM XML::

    with open("sim.xml", "r") as f:
        simulation = nanover.openmm.serializer.deserialize_simulation(f.read())

The ``deserialize_simulation`` function accepts optional arguments:

- ``imd_force``: A CustomExternalForce for interactive molecular dynamics
- ``platform_name``: The OpenMM platform to use (e.g. "CUDA", "OpenCL")
- ``ignore_state``: Whether to ignore the serialized state in the XML (default: ``False``)
For example::

    simulation = nanover.openmm.serializer.deserialize_simulation(
        xml_string,
        platform_name="CUDA"
    )

For more details, refer to the OpenMM example on saving systems to XML `files <https://github.com/openmm/openmm-cookbook/blob/main/notebooks/cookbook/Saving%20Systems%20to%20XML%20Files.ipynb>`_.
