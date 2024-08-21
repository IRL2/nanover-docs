Welcome to NanoVer's documentation!
===================================

NanoVer is a free, open-source and flexible software that can be used as:

(1) A **framework** for building **multi-user virtual reality applications** for molecular systems.
(2) A **client-server** application for **collaborative interactive molecular dynamics simulations in virtual reality** (iMD-VR).

Nanover is distributed under the `MIT <https://github.com/IRL2/nanover-protocol/blob/main/LICENSE>`_ license.

----

As a client-server application, NanoVer consists of:

(1) **The NanoVer server**: the server communicates with a physics engine, e.g. OpenMM, to facilitate interactive MD simulations.
(2) **Nanover IMD**: a client that can connect to a NanoVer server to access simulation data and facilitate user interaction with the molecular system. This can be done using:

    * A **python client**: a python script, e.g. a Jupyter notebook. Check out the :ref:`tutorials <Tutorials>` for further information.
    * A **VR client**: an instance of the NanoverIMD program (see the `latest releases here <https://github.com/IRL2/nanover-imd/releases>`_) that enables a user to visualise and interact with the real-time MD simulation in VR.

----

################
Current sponsors
################

.. image:: /_static/erc_text.png
    :width: 225
    :target: https://cordis.europa.eu/project/id/866559

.. image:: /_static/erc_logo.png
    :width: 225
    :target: https://cordis.europa.eu/project/id/866559

.. image:: /_static/xunta_de_galicia_logo.png
    :width: 225
    :target: https://www.xunta.gal/portada

----

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   highlights.rst
   installation.rst
   tutorials/tutorials.rst
   concepts/concepts.rst
   modules.rst
   citations.rst

----

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
