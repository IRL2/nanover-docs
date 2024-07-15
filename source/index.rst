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

Highlights
----------

----

NanoVer lets you **enter virtual reality and steer molecular dynamics simulations in real time**. Explore rare events and try docking poses.

* :ref:`Install the server software <Installation>`.
* Interact with molecules in virtual reality by `downloading the VR client <https://github.com/IRL2/nanover-imd/releases/download/nightly/StandaloneWindows64.zip>`_
* Check out the :ref:`tutorials <Tutorials>`.

.. raw:: html

   <div align="center">
     <video width="320" height="240" controls>
       <source src="/_static/nanotube_mixed_reality.mp4" type="video/mp4">
     </video>
   </div>

----

**Integrate NanoVer into your existing workflow!** NanoVer uses a customisable python server and provides an API for integrating different physics engines.
Check out the :ref:`tutorials here <Tutorials>`.

----

Use python to control molecular representations and **create insightful visuals**.
`Read the documentation on representations here. <https://github.com/IRL2/nanover-protocol/blob/main/examples/fundamentals/visualisations.ipynb>`_

.. image:: /_static/Renderers.gif
    :alt: A gif showing a protein within the NanoVer VR environment cycling through several visual states.
    :align: center
    :scale: 30%

----

**Develop with NanoVer!** Contribute to the code or develop your own custom applications with NanoVer.

* `Get the source code for the server <https://github.com/IRL2/nanover-protocol>`_
* `Get the source code of the VR client <https://github.com/IRL2/nanover-imd>`_

NanoVer is distributed under the `MIT <https://github.com/IRL2/nanover-protocol/blob/main/LICENSE>`_ license.

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
