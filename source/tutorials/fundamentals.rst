====================
NanoVer Fundamentals
====================

A set of tutorials that introduce NanoVer as a framework to perform interactive molecular
dynamics simulations, and the fundamental concepts associated with the client-server
architecture that NanoVer uses. These tutorials can be used in conjunction with the
information in :ref:`concepts <Concepts>` to understand how NanoVer works.

The set of Jupyter notebook tutorials on the fundamentals of NanoVer can be found in the
`examples <https://github.com/IRL2/nanover-protocol/tree/main/examples/fundamentals>`_ folder
of the GitHub repository, which contains the following tutorials:

* `getting_started`: **New to NanoVer? Start here!** An introductory notebook that showcases how
  NanoVer can be used to run an interactive molecular dynamics (iMD) simulation for a
  pre-prepared methane & nanotube system.
* `frame`: A notebook that introduces the concept of the **frame**, the object sent by
  the NanoVer server to the client that contains data associated with the molecular system.
* `servers`: A notebook that introduces the concept of the **NanoVer server**, and
  explains its role within the client-server architecture of NanoVer.
* `commands_and_state`: A notebook that introduces the concepts of **commands**, and explains
  how NanoVer achieves synchronised multi-user interactive molecular simulations via the
  **shared state** dictionary.
* `visualisations`: A notebook that demonstrates how to change the **visualisation** of the
  interactive molecular simulation within the NanoVer iMD VR client.