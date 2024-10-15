XML Files
==============================================

The XML format for serializing OpenMM simulations consists of a root element ``<OpenMMSimulation>`` containing three main components:

1. **Starting Structure**: Enclosed in either ``<pdbx>`` or ``<pdb>`` tags
2. **OpenMM Serialized System**: Enclosed in the ``<System>`` tag
3. **OpenMM Serialized Integrator**: Enclosed in the ``<Integrator>`` tag

An optional fourth component, the OpenMM serialized state, may also be included.

XML Structure
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

Components Description
----------------------

1. **Starting Structure**:
^^^^^^^^^^^^^^^^^^^^^^^^^^

   * Tag: ``<pdbx>`` (preferred) or ``<pdb>`` (for backward compatibility)
   * Content: The entire PDBx or PDB file content

2. **OpenMM Serialized System**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within this tag, you'll find:

    **Particles:** They are represented with ``<Particle>`` tags, each containing:
        - Mass
        - Charge (if using a `NonbondedForce`)

    **Forces:** Various force components are represented by specific tags:

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


3. **OpenMM Serialized Integrator**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``<Integrator>`` tag contains parameters specific to the integration method used, such as step size and temperature for a Langevin integrator:

.. code-block:: xml

    <Integrator type="LangevinIntegrator" constraintTolerance="1e-05" friction="4" randomSeed="0" stepSize=".0005" temperature="300" version="1" />

Usage
-----

This XML format serves two primary purposes:

1. **Serialization**: Converting an existing OpenMM simulation instance into an XML file
2. **Deserialization**: Creating an OpenMM simulation instance from an XML file

The format allows for efficient storage and exchange of OpenMM simulation data, including the starting structure, system configuration, and integrator settings.