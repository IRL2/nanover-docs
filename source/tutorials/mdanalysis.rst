==========
MDAnalysis
==========

A set of tutorials that demonstrate how NanoVer can be interfaced with MDAnalysis to visualise static structures and
trajectories in VR, and analyse the results of trajectories recorded using NanoVer.

The Jupyter notebook tutorials that showcase these features can be found in the
`examples <https://github.com/IRL2/nanover-server-py/tree/main/examples/mdanalysis>`_ folder of the GitHub repository.
It contains:

* `mdanalysis_lsd`: A notebook that demonstrates how to import a pdb into MDAnalysis and visualise this structure in VR,
  including changing the visualisation of different parts of the system, e.g. protein/ligands/lipids, using MDAnalysis
  selections.
* `mdanalysis_trajectory`: A notebook that demonstrates how to import a trajectory into MDAnalysis from the topology
  (pdb) and trajectory (dcd) files and show this in VR. Learn how to hook up python commands such as play/pause/reset to
  the corresponding buttons on the handheld menu in the VR application.
* `mdanalysis_nanover_recording`: A notebook that details how to use MDAnalysis to extract data from an iMD simulation
  recorded with NanoVer, and highlights some of the benefits of recording trajectories using the in-built recording
  functionality of NanoVer.