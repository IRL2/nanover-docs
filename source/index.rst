Welcome to Narupa's documentation!
======================================

This site provides documentation and tutorials on the use of Narupa,
a framework for interactive molecular simulation, with a particular
focus on virtual reality applications.

Narupa is free, open source and distributed under the
`GNU GPLv3 <https://gitlab.com/intangiblerealities/narupa-protocol/blob/master/License>`_ license.
You can look at and contribute to the code for building server applications `here <https://gitlab.com/intangiblerealities/narupa-protocol/>`_,
and our VR applications such as `iMD-VR <https://gitlab.com/intangiblerealities/narupa-applications/narupa-imd/>`_ and 
`Narupa Builder <https://gitlab.com/intangiblerealities/narupa-applications/narupa-builder/>`_.

It is a complete re-write of the original `Narupa <https://gitlab.com/intangiblerealities/narupa-server>`_,
designed to be more extendible, robust and easier to use.

Narupa allows interactive simulation with several packages,
including:

* `ASE <https://wiki.fysik.dtu.dk/ase/>`_ - Python simulation framework, particularly good for QM,
  semi-empirical and machine learned potentials.
* `OpenMM <http://openmm.org/>`_ - GPU accelerated molecular mechanics, supporting AMBER, GROMACS and CHARMM.
* `SCINE Sparrow <https://scine.ethz.ch/download/sparrow>`_ - semi-empirical potentials.
* `LAMMPS <https://lammps.sandia.gov/>`_ - Materials and molecular mechanics.


Citation
###################

If you find Narupa useful, please cite the following
`paper <https://aip.scitation.org/doi/10.1063/1.5092590>`_:

M. O’Connor, S.J. Bennie, H.M. Deeks, A. Jamieson-Binnie, A.J. Jones,
R.J. Shannon, R. Walters, T. Mitchell, A.J. Mulholland, D.R. Glowacki,
“Interactive molecular dynamics from quantum chemistry to drug binding:
an open-source multi-person virtual reality framework”,
J. Chem Phys 150, 224703 (2019)

Bib file:

.. literalinclude:: narupa.bib

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation.rst
   tutorials/tutorials.rst
   concepts/concepts.rst
   python/modules.rst




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
