=================================================================
LAMMPS: Large scale Atomic/Molecular Massively Parallel Simulator
=================================================================

.. warning::

    We are aware that the current tutorials for
    interfacing LAMMPS with NanoVer are incomplete
    (see `Issue #84 <https://github.com/IRL2/nanover-protocol/issues/184>`_), and are
    working to resolve these problems.

Installing LAMMPS
#################

NanoVer can interact with the `LAMMPS <https://lammps.sandia.gov/>`_ simulation engine.
If you want to use this specific feature, you need to:

* install LAMMPS with python capabilities
* install mpy4py:

            * ``conda install -c conda-forge mpi4py`` on Linux and MacOS
            * ``python -m pip install mpi4py`` on Windows

* install nanover-lammps: ``conda install -c irl -c conda-forge nanover-lammps``


Jupyter notebook tutorials
##########################

A tutorial that demonstrates how to use NanoVer to run interactive molecular
dynamics simulations using LAMMPS.

* `lammps_client_server`: A notebook showing how to run an interactive molecular dynamics LAMMPS simulation.
