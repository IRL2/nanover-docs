===================================
ASE: Interactive Molecular Dynamics
===================================

Running an ASE OpenMM server from the command line
==================================================

When `nanover-ase` is installed, it provides the `nanover-omm-ase`
command in the command line. When provided with the description of an
OpenMM simulation as an XML file serialised as described in the `NanoVer OpenMM documentation <https://github.com/IRL2/nanover-protocol/tree/main/python-libraries/nanover-openmm>`_ 
, `nanover-omm-ase` runs an interactive simulation. 
The host address and port can be set with
the ``--address`` and the ``--port`` option, respectively.


Running a server from python
==================================================

The `nanover-ase` module provides the
:class:`nanover.ase.ASEImdServer` class. Given an ASE simulation set up with an 
`ASE molecular dynamics runner <https://wiki.fysik.dtu.dk/ase/ase/md.html>`_, this class will 
attach interactive molecular dynamics functionality and frame serving to the dynamics. 
An example is given below, assuming an ASE Atoms object has been set up, named `atoms`:

.. code-block:: python

    from ase import units
    from ase.md import Langevin
    from nanover.ase.imd_server import ASEImdServer

    # Given some ASE atoms object appropriately set up, set up dynamics.
    dyn = Langevin(atoms, 1 * units.fs, 300, 0.1)

    # Attach the IMD calculator and server to the dynamics object. 
    imd = ASEImdServer(dyn)
    while True:
        imd.run(100)


Full examples are given in the `examples <https://github.com/IRL2/nanover-protocol/tree/main/examples/ase>`_ folder, which additionally
contains several Jupyter notebooks that explore how NanoVer can be used with OpenMM:

* `basic_example`: A notebook showing how one can run the server for an OpenMM simulation,  connect a client to it, and render a simple visualisation. 
* `openmm_nanotube`: A notebook that runs a simulation of a carbon nanotube, then applies interactive forces to it from the notebook.
* `nanover_nglview`: A notebook that assumes a server is already running, and visualises it with `NGLView <https://github.com/arose/nglview>`_. To run this notebook, ensure NGLView is installed with:

.. code-block:: python

    conda install nglview -c conda-forge
    # might need: jupyter-nbextension enable nglview --py --sys-prefix

    # if you already installed nglview, you can `upgrade`
    conda upgrade nglview --force
    # might need: jupyter-nbextension enable nglview --py --sys-prefix


