======
OpenMM
======

.. contents:: Contents
    :depth: 2
    :local:

----

##########################
Jupyter notebook tutorials
##########################

A set of tutorials that demonstrate how to use NanoVer to run interactive molecular
dynamics simulations using OpenMM directly.

The Jupyter notebook tutorials that demonstrate how to run interactive molecular
dynamics simulations by interfacing NanoVer with OpenMM directly can be found in
the `examples <https://github.com/IRL2/nanover-server-py/tree/main/examples/openmm>`_
folder of the GitHub repository. It contains:

* `openmm_polyalanine`: A notebook that demonstrates how to set up an interactive
  OpenMM simulation from scratch with NanoVer, use features of OpenMM in conjunction
  with NanoVer, and record & playback simulations directly using NanoVer.
* `openmm_nanotube`: A notebook that demonstrates how to interact with an OpenMM
  NanoVer simulation using a python client.
* `openmm_neuraminidase`: A notebook that demonstrates how to set up an interactive
  OpenMM simulation from scratch with NanoVer and change the visualisations of
  different atom selections for a protein-ligand system.

|

----

########################
NanoVer OpenMM XML files
########################

File format
###########

The NanoVer OpenMM XML file format described herein is used for saving and loading NanoVer OpenMM simulations.
These files consist of a root element, ``<OpenMMSimulation>``, which contains three mandatory components
and an optional fourth:

1. **Starting structure**: enclosed in either ``<pdbx>`` or ``<pdb>`` tags
2. **OpenMM serialized System**: enclosed in the ``<System>`` tag
3. **OpenMM serialized Integrator**: enclosed in the ``<Integrator>`` tag
4. **OpenMM serialized State**: enclosed in the ``<State>`` tag (optional)

E.g. a file that includes the OpenMM serialized State will have the following structure:

.. code-block:: text

    <OpenMMSimulation>
        <pdbx>
            <!-- Content of the PDBx file -->
        </pdbx>
        <System ...>
            <!-- XML content of the OpenMM serialized System -->
        </System>
        <Integrator ...>
            <!-- XML content of the OpenMM serialized Integrator -->
        </Integrator>
        <State ...>
            <!-- XML content of the OpenMM serialized State -->
        </State>
    </OpenMMSimulation>

.. note::
    XML files used by OpenMM differ from those used to run OpenMM via NanoVer.
    Although the serialized objects contained in the NanoVer OpenMM XML files are identical to those defined by OpenMM,
    the overall contents and structure of the files are specific to NanoVer and cannot be read by OpenMM directly.


Expand the following dropdowns for further details of each component:

.. dropdown:: 1. **Starting structure**

   * Tag: ``<pdbx>`` (preferred) or ``<pdb>`` (for backward compatibility)
   * Content: the entire PDBx or PDB file content


.. dropdown:: 2. **OpenMM serialized System**

    Within this tag, you'll find:

        **Particles:** each particle is represented with a ``<Particle>`` tag, containing:

            - Mass
            - Charge (if using a `NonbondedForce`)

        **Forces:** the force components, each represented by specific tags (a detailed list can be found in
        this `link <http://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#standard-forces>`_),
        for example:

            - ``<HarmonicBondForce>``: for bond stretching
            - ``<HarmonicAngleForce>``: for angle bending
            - ``<PeriodicTorsionForce>``: for dihedral angles
            - ``<NonbondedForce>``: for electrostatic and van der Waals interactions
            - ``<CustomNonbondedForce>``: for user-defined nonbonded interactions

            Each force tag contains parameters specific to that force type. For example:

            .. code-block:: xml

               <HarmonicBondForce>
                 <Bond p1="0" p2="1" length="0.1" k="1000"/>
               </HarmonicBondForce>

        **Constraints:** If present, constraints are listed under the ``<Constraints>`` tag:

            .. code-block:: xml

               <Constraints>
                 <Constraint p1="0" p2="1" distance="0.1"/>
               </Constraints>


.. dropdown:: 3. **OpenMM serialized Integrator**

    The ``<Integrator>`` tag contains parameters that specify the integration method to be used to simulate dynamics,
    such as the type of integrator, simulation time step, and temperature:

    .. code-block:: xml

        <Integrator type="LangevinIntegrator" constraintTolerance="1e-05" friction="4" randomSeed="0" stepSize=".0005" temperature="300" version="1" />

    More details on integrators can be found `here <http://docs.openmm.org/latest/userguide/theory/04_integrators.html>`_.

.. dropdown:: 4. **OpenMM serialized State**

    The ``<State>`` tag contains the serialized state of the simulation, including:

    - Particle velocities, ``<Velocities>``
    - Adjustable parameters that have been defined by Force objects in the System, ``<Parameters>``
    - Periodic box vectors (if periodic boundary conditions are used), ``<PeriodicBoxVectors>``
    - Integrator parameters, ``<IntegratorParameters>``

|

----

Creation and usage
##################

The :mod:`nanover.openmm.serializer` module provides the ``serialize_simulation`` and ``deserialize_simulation``
functions which allow saving and loading OpenMM simulations to/from XML files.
The serialization captures by default the complete simulation including:

- Structure coordinates and topology (as PDBx/PDB)
- OpenMM System definition
- Integrator configuration
- Serialized State (optional)

Serializing a simulation
~~~~~~~~~~~~~~~~~~~~~~~~

To save a simulation to a NanoVer OpenMM XML using Python:

.. code-block:: python

    xml_string = nanover.openmm.serializer.serialize_simulation(simulation)

    with open("sim.xml", "w") as f:
        f.write(xml_string)

The ``serialize_simulation`` function accepts optional arguments:

* ``save_state``: whether to include the serialized state in the XML (default: ``False``)

Deserializing a simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~

To load a simulation from a NanoVer OpenMM XML using Python:

.. code-block:: python

    with open("sim.xml", "r") as f:
        simulation = nanover.openmm.serializer.deserialize_simulation(f.read())

The ``deserialize_simulation`` function accepts optional arguments:

* ``imd_force``: a CustomExternalForce for interactive molecular dynamics
* ``platform_name``: the parallel computing platform for OpenMM to use (e.g. "CUDA", "OpenCL")
* ``ignore_state``: whether to ignore the serialized state in the XML (default: ``False``)

For example:

.. code-block:: python


    simulation = nanover.openmm.serializer.deserialize_simulation(
        xml_string,
        platform_name="CUDA"
    )

For more details, refer to our
`example notebook <https://github.com/IRL2/nanover-server-py/blob/main/examples/openmm/openmm_polyalanine.ipynb>`_
on saving OpenMM systems to NanoVer OpenMM XML files.

|
