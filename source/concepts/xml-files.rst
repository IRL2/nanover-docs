XML Files
==============================================

The XML format for serializing OpenMM simulations consists of a root element ``<OpenMMSimulation>`` containing three main components:

1. **Starting Structure**: Enclosed in either ``<pdbx>`` or ``<pdb>`` tags
2. **OpenMM Serialized System**: Enclosed in the ``<System>`` tag
3. **OpenMM Serialized Integrator**: Enclosed in ``<Integrator>`` tags

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

   * Tag: ``<pdbx>`` (preferred) or ``<pdb>`` (for backward compatibility)
   * Content: The entire PDBx or PDB file content

2. **OpenMM Serialized System**:

   * Tag: ``<System>``
   * Content: XML representation of the OpenMM serialized system
   * Attributes: May include system-specific attributes

3. **OpenMM Serialized Integrator**:

   * Tag: ``<Integrator>``
   * Content: XML representation of the OpenMM serialized integrator
   * Attributes: May include integrator-specific attributes

Usage
-----

This XML format serves two primary purposes:

1. **Serialization**: Converting an existing OpenMM simulation instance into an XML file
2. **Deserialization**: Creating an OpenMM simulation instance from an XML file

The format allows for efficient storage and exchange of OpenMM simulation data, including the starting structure, system configuration, and integrator settings.