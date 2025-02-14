====================
Recording in NanoVer
====================

.. _Rust server: https://github.com/IRL2/nanover-server-rs

For a NanoVer session to be useful beyond the time the users spend in VR, it needs to be recorded.
This recording can then be analysed or played back to get insight. In this document, we describe how to record a NanoVer session and how to visualise the recording using inbuilt methods.

.. contents:: Contents
    :depth: 2
    :local:

----

############
Introduction
############

NanoVer data streams
####################

NanoVer can record the following data streams:

* the stream of simulation frames
* the stream of updates of the shared state

Recorded streams are identical to the data streams sent to clients during a live simulation,
with the addition of a timestamp that enables synchronisation of the streams during playback.

Each stream is stored in a separate file.
By convention, recordings of the frame stream have the ``.traj`` file extension,
while recordings of the shared state stream have the ``.state`` file extension.

.. warning::

   In order to pass the trajectory and state files to a NanoVer server via the
   :class:`PlaybackSimulation` class in the :mod:`nanover.omni.playback` module,
   they must adopt the above file extension conventions.

----

Recording file format
#####################

Each NanoVer recording file contains a header and a sequence of records:

* The header contains two fields, stored as little endian 8 bytes unsigned integers:

    * **a magic number, its value is 6661355757386708963**. This value was chosen arbitrarily and needs to be the first
      8 bytes of the file to indicate it is indeed a NanoVer recording. A file without this magic number is not a NanoVer
      recording, however one should keep in mind that a file that starts with that value could still not be a valid
      recording and should handle errors accordingly.
    * **the version of the file format**. This version number dictates how the rest of the file will be written or parsed.
      Any change to the file format needs to increment this file format version. The current version is 2.

* Each record contains:

    * a timestamp encoded as a little endian 16 bytes unsigned integer that indicates the time, in microseconds,
      since the beginning of the recording.
      This timestamp indicates the timing of the records and allows synchronisation of a NanoVer trajectory and a state recording.
    * the size, in bytes, of the record; encoded as an 8 bytes little endian unsigned integer.
    * a :ref:`StateUpdate <state-updates>` (NanoVer *shared state* recordings **only**), as a protobuf message.
    * a ``GetFrameResponse`` (NanoVer *trajectory* recordings **only**) as a protobuf message, comprising:

        * The **frame index**: this is generally an integer that gets incremented each time the server register a frame to broadcast.
          However, its value is only significant when it is 0 as it means the frame needs to be reset,
          for instance because the server loaded a new simulation.
        * The **frame** itself: this is an instance of the :ref:`FrameData <traj-and-frames>` class.

|

----

#####################
Recording with Python
#####################

via the terminal
################

The `nanover-record` command-line utility can be used to quickly start and stop multiple spans of recording
without writing any code.

The default is to connect to a local server on the default port, but more connectivity and output options
can be found with the help option:

.. code-block::

    nanover-record --help

----

via a Python script
###################

NanoVer sessions can be also recorded using the :mod:`nanover.omni.record` module.
Here is an example of how to define the file names and paths for the recording and pass them to the recording function:

.. code:: python

    from nanover.omni.record import record_from_server
    # Define the .traj and .state file names and paths
    traj_path = 'path/to/simulation_recording.traj'
    state_path = 'path/to/simulation_recording.state'
    # create a recording from a server and save it to the files
    record_from_server("localhost:38801", traj_path, state_path)

----

Visualising recordings
######################

Visualising and playing back recordings can be done using :mod:`nanover.omni.playback` module.
The Python Server can stream recorded NanoVer streams read by a ``PlaybackSimulation`` object to a client.
The client then plays back the recording as if it were a live stream.
The server sends the frame and state updates whilst trying to respect the timing dictated by the timestamps stored
in the file.

.. code:: python

    from nanover.omni import OmniRunner
    from nanover.omni.playback import PlaybackSimulation
    simulation_recording = PlaybackSimulation(name='simulation-recording',
                                           traj='path/to/recording.traj',
                                           state='path/to/recording.state')
    # Create a runner for the simulation
    recording_runner = OmniRunner.with_basic_server(simulation_recording,
                                                    name='simulation-recording-server')
    # Start the runner
    recording_runner.next()
    # Close the runner
    recording_runner.close()

.. note::

    Further instructions and information on how to record and replay using the NanoVer Python module can be found in
    this notebook `recording_and_replaying.ipynb <https://github.com/IRL2/nanover-server-py/blob/main/examples/basics/recording_and_replaying.ipynb>`_.

|

----

##############################
Recording with the Rust Server
##############################

.. note::

    The Rust Server takes a snapshot of the streams 30 times a second (although this may change with
    issues `#200 <https://github.com/IRL2/nanover-server-rs/issues/200>`_ and
    `#201 <https://github.com/IRL2/nanover-server-rs/issues/201>`_).

via the terminal
################

When using the ``nanover-cli`` command via the command line, use the ``--trajectory`` argument to specify the file that
will store the recording of the frame stream, and the ``--state`` argument to specify the file that will store
the recording of the shared state updates.

.. code-block::

    # For Windows Powershell
    .\nanover-cli.exe "simulation.xml" --trajectory "path/to/recording.traj" --state "path/to/recording.state"

----

via the GUI
###########

On the graphical user interface (GUI), the files are specified in the ``Recording`` section before starting the server
(see :ref:`rust_server_via_the_gui`).

----

Visualising recordings
######################

**Using the the command line**, providing only a ``.traj`` file will stream the frames only,
and providing only a ``.state`` file will stream the state updates only.
In order to send both streams together, provide the two file paths separated by a colon:

.. code-block::

    # For Windows Powershell
    .\nanover-cli.exe "path/to/recording.traj:path/to/recording.state"


**Using the graphical interface**, add a recording to the list of simulations using the ``+ Recording`` button,
then choose the files.

|

----

##########################################
Reading NanoVer recordings with MDAnalysis
##########################################

Recordings can be read and manipulated using the NanoVer Python library.

The :py:mod:`nanover.mdanalysis` module enables us to convert NanoVer trajectory recordings into
`MDAnalysis Universes <https://userguide.mdanalysis.org/stable/universe.html#universe>`_, which are data structures used by the MDAnalysis library to handle molecular dynamics simulations.

A single NanoVer recording may include switching between multiple systems with differing topologies, whereas a single MDAnalysis universe is concerned only with single systems of constant topology. NanoVer provides a `universes_from_recording` function to extract each independent simulation run occurring with a recording.

See the example code below, or check out the
`mdanalysis_nanover_recording <https://github.com/IRL2/nanover-server-py/blob/main/examples/mdanalysis/mdanalysis_nanover_recording.ipynb>`_
Jupyter notebook tutorial for further information.

.. code:: python

    import MDAnalysis as mda
    from nanover.mdanalysis import universes_from_recording
    import matplotlib.pyplot as plt

    # read all universes and take the first one
    universes = universes_from_recording(traj='hello.traj')
    u = universes[0]

    times = []
    frames = []
    potential_energy = []
    kinetic_energy = []
    user_energy = []
    timestamps = []

    for timestep in u.trajectory:
        frames.append(timestep.frame)
        times.append(timestep.time)
        potential_energy.append(timestep.data["energy.potential"])
        kinetic_energy.append(timestep.data["energy.kinetic"])
        user_energy.append(timestep.data["energy.user.total"])
        timestamps.append(timestep.data["elapsed"])

    fig, axis = plt.subplots(1)
    axis.plot(frames, potential_energy, label='Potential energy')
    axis.plot(frames, kinetic_energy, label='Kinetic energy')
    axis.plot(frames, user_energy, label='User energy')
    axis.legend()
    axis.set_ylim(-1000, 10000)
    axis.set_xlabel("Frame index")
    axis.set_ylabel("Energy (kJ/mol)")


We also have a `Python script <https://github.com/IRL2/nanover-utils/tree/main/parsing-recordings/read_state.py>`_ located
in the `nanover-utils <https://github.com/IRL2/nanover-utils>`_ repository for parsing NanoVer shared state recordings.

|
