 .. _installation:

==============================
Installation & Getting Started
==============================

NanoVer consists of two components: the python-based libraries
for running simulations, and the Unity3D libraries
and applications for visualising & interacting with simulations
in VR.

.. contents:: Contents
    :depth: 2
    :local:

----

.. _user_installation_guide:

#######################
User Installation Guide
#######################

This guide contains the information required to get NanoVer up and running on your computer! This includes
creating a conda environment and installing the server, which is required for setting up and running simulations. You
then have the option to install the iMD-VR client, which you can use for visualising and interacting with your simulations
inside VR.


.. _creating_conda_env:

Setting up conda
################

#. Install conda through whichever program you prefer, e.g. `Miniforge <https://github.com/conda-forge/miniforge>`_.
#. Open a terminal that you have conda installed in:

    * On Windows, this is Windows Powershell.
    * On Mac and Linux, this is the terminal.

At this point, you are ready to create your conda environment and install the NanoVer server! Please refer to
:ref:`installing_the_server`.


.. _installing_the_server:

Installing the server
#####################

We can create our conda environment and install the NanoVer packages all in one go!
Doing so ensures that we install the correct version of python for our packages.

#. Create your conda environment (here we call the environment "nanover") and install the NanoVer
   packages by running the following command in the terminal that you have conda installed in:

   .. code:: bash

        conda create -n nanover -c irl -c conda-forge nanover-server

#. To use your newly created NanoVer conda environment, activate it as follows:

   .. code:: bash

        conda activate nanover

For information on how to run NanoVer servers, check out the :ref:`tutorials <Tutorials>`.

Updating the conda package
~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Determine the currently installed version:

   .. code:: bash

        conda list nanover-server

#. Attempt to update to latest version:

   .. code:: bash

        conda update nanover-server

If you can't seem to update to the latest version of the NanoVer server, there may be some
issue with the dependencies of the packages. In this case, we recommend creating a new
conda environment and reinstalling :code:`nanover-server`, following the
:ref:`installation instructions<installing_the_server>`.


.. _installing_imdvr_client:

Installing the iMD-VR client
############################

To use NanoVer iMD, you have two options:

* **Conda installation of the NanoVer iMD package**. This is a good option if you are familiar with conda (or want to learn how to use it!), see :ref:`conda_installation_VR_client`.

* **Download the latest release of the NanoVer iMD executable**. This is a quick and easy option for those unfamiliar with conda, see :ref:`download_latest_release_VR_client`.

For more information on how to choose your installation method based on your VR setup, please check out the
:ref:`choosing your iMD-VR setup<choosing_setup_iMD-VR>` section on the NanoVer iMD tutorial page.


.. _conda_installation_VR_client:

Conda installation
~~~~~~~~~~~~~~~~~~

If you have not already created a NanoVer conda environment, please refer to
:ref:`creating_conda_env` and :ref:`installing_the_server`.

#. Activate your NanoVer conda environment:

   .. code:: bash

        conda activate nanover

#. Install the NanoVer iMD package:

   .. code:: bash

        conda install -c irl nanover-imd

#. Set up your VR headset.

#. To start the program, run the following command:

   .. code:: bash

        NanoveriMD


.. _download_latest_release_VR_client:

Download the latest release
~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Download the latest release from the git repo `here <https://github.com/IRL2/nanover-imd/releases>`_.

#. Extract the downloaded zip file.

#. The next steps depend on your chosen VR setup:

.. _using_pc-vr:

.. dropdown:: **Using PC-VR** (wireless or tethered)

    This includes
    `Meta Quest Link & AirLink <https://www.meta.com/en-gb/help/quest/articles/headsets-and-accessories/oculus-link/connect-with-air-link/>`_,
    `SteamVR <https://store.steampowered.com/app/250820/SteamVR/>`_, and `Steam Link <https://store.steampowered.com/app/353380/Steam_Link/>`_:

    #. Set up your headset according to your chosen setup (see the links above).
    #. Navigate to the ``windows`` directory in the extracted folder, and launch ``NanoVer iMD.exe``.
    #. The first time you run this, Windows will likely prompt you with a warning about the executable not being signed.
       If this happens, click on the **"More info"** button, then **"Run anyway"**.
       You will also likely be prompted by the Windows firewall, **allow NanoVer to access the network**.

.. _running_locally_on_meta_quest_wireless:

.. dropdown:: **Running locally on a Meta Quest headset** (wireless)

    #. Ensure that you have developer mode enabled on your headset (search online for up-to-date instructions).
    #. Connect your headset to your computer with a cable and sideload the ``nanover-imd.apk`` from the extracted zip
       file onto your device. You can use `SideQuest <https://sidequestvr.com>`_ or the
       `Meta Quest Developer Hub <https://developer.oculus.com/meta-quest-developer-hub/>`_ for this.
    #. Inside the VR headset, open Apps and filter ``Unknown Sources`` from the drop-down menu in the top right corner.
       Locate and run ``NanoVer IMD``.


.. _running_locally_on_meta_quest_developer_hub:

.. dropdown:: **Running locally on a Meta Quest headset via the Meta Developer Hub** (tethered)

    #. First, follow the :ref:`above instructions<running_locally_on_meta_quest_wireless>` for sideloading the apk onto your headset.
    #. Connect your headset to your computer with a cable. A notification may appear inside your headset stating
       ``USB Detected: click on this notification to allow the connected device to access files``. Allow this.
    #. On your computer, open the `Meta Quest Developer Hub <https://developer.oculus.com/meta-quest-developer-hub/>`_
       and go to the ``Device Manager`` menu on the left sidebar.
    #. Look for the NanoverIMD app under ``Apps``. It should be called ``com.IntangibleRealitiesLaboratory.NanoVeriMD``
       (hover over it with your cursor to see the full name).
    #. Click on the three dots (on the far right) for this app and select ``Launch App``.

.. admonition:: Key point

    For a **wireless setup** you will need to have a strong and stable internet connection that allows communication over the network.
    This option is often incompatible with public / institutional networks.

.. admonition:: Key definition

    \ **Tethered**: using a cable to connect your VR headset to your computer.

----


.. _developer_installation_guide:

############################
Developer Installation Guide
############################

We refer developers to the relevant code bases:

* If you want to create your own custom server, connect a different physics engine or create a custom client,
  you can do this via modification of the NanoVer protocol. To download and install the source code, please follow the
  `developer installation instructions
  <https://github.com/IRL2/nanover-server-py?tab=readme-ov-file#developer-installation>`_
  in the README of the `nanover-server-py repository <https://github.com/IRL2/nanover-server-py>`_ on GitHub.

* If you want to customise the NanoVer iMD Unity3D application, instructions for obtaining the source code are available
  in the `nanover-imd repository <https://github.com/IRL2/nanover-imd>`_ on GitHub .

* If you want to build your own VR application that interfaces with NanoVer, the NanoVer Unity3D libraries are available
  in the `NanoverUnityPlugin repository <https://github.com/IRL2/NanoverUnityPlugin>`_ on GitHub .
