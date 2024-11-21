==================================
ASE: Atomic Simulation Environment
==================================

A set of tutorials that demonstrate how to use NanoVer to run interactive molecular
dynamics simulations using ASE.

The Jupyter notebook tutorials that demonstrate how to run interactive molecular dynamics simulations
by interfacing NanoVer with ASE can be found in the
`examples <https://github.com/IRL2/nanover-protocol/tree/main/examples/ase>`_ folder fo the GitHub
repository. This folder also contains notebooks that explore how ASE can be used in NanoVer in
conjunction with OpenMM. It contains:

* `ase_basic_example`: A notebook showing how one can run the server for an ASE simulation,  connect a client to it, and render a simple visualisation.
* `ase_openmm_nanotube`: A notebook that runs a simulation of a carbon nanotube using ASE and OpenMM, then applies interactive forces to it from the notebook.
* `ase_openmm_graphene`: A notebook that runs a simulation of a graphene sheet using ASE and OpenMM, and demonstrates how parameters of the simulation can be controlled in real
  time through the Jupyter notebook interface.
* `ase_openmm_neuraminidase`: A notebook that demonstrates how to construct an input file for an OpenMM simulation of neuraminidase to run with NanoVer from scratch, and then
  runs the simulation using ASE with an OpenMM calculator.

