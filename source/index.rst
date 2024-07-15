Welcome to NanoVer's documentation!
===================================

NanoVer is a free, open-source and flexible software that can be used as:

(1) A **framework** for building **multi-user virtual reality applications** for molecular systems.
(2) A **client-server** application for **collaborative interactive molecular dynamics simulations in virtual reality** (iMD-VR).

----

As a client-server application, NanoVer consists of:

(1) **The NanoVer server**: the server communicates with a physics engine, e.g. OpenMM or ASE, to facilitate interactive MD simulations.
(2) **Nanover IMD**: this is the front end, which allows users to connect to a NanoVer server to access simulation data and facilitate user interaction with the molecular system. This can be done using:

    * A **python client**: a python script, e.g. a Jupyter notebook. Check out the :ref:`tutorials <Tutorials>` for further information.
    * A **VR client**: the program (available `here <https://github.com/IRL2/nanover-imd/releases/download/nightly/StandaloneWindows64.zip>`_ as an executable) that enables a user to connect to a NanoVer server to visualise and interact with the real-time MD simulation in VR.

----

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   highlights.rst
   installation.rst
   tutorials/tutorials.rst
   concepts/concepts.rst
   python/modules.rst
   citations.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
