Recording data
==============

.. _Rust server: https://github.com/IRL2/nanover-rs

For a NanoVer session to be useful beyond the time the users spend in VR, it needs to be recorded.
This recording can then be analysed or played back to get insight.

.. contents:: Contents
    :depth: 2
    :local:

What is recorded
----------------

NanoVer can record two different streams:

* the stream of simulation frame,
* and the stream of updates of the shared state.

These two streams are identical to the streams sent to the clients during the live recording,
with the addition of a timestamp that allows synchronisation of the streams during playback.
Each stream is stored in a separate file.

By convention, recordings of the frame stream have the ``.traj`` file extension,
while recordings of the shared state stream  have the ``.state`` file extension.

Recording format
----------------

The current version of the file format is version 2.
Each recording file contains a header and a sequence of records.

The header contains two fields, stored as little endian 8 bytes unsigned integers:

* **a magic number, its value is 6661355757386708963**. This value was chosen arbitrarily and needs to be the first
  8 bytes of the file to indicate it is indeed a NanoVer recording. A file without this magic number is not a NanoVer
  recording, however one should keep in mind that a file that starts with that value could still not be a valid
  recording and should handle errors accordingly.
* **the version of the file format**. This version number dictates how the rest of the file will be written or parsed.
  Any change to the file format needs to increment this file format version. The current version is 2.

A record contains:

* a timestamp encoded as a little endian 16 bytes unsigned integer that indicates the time, in microseconds,
  since the beginning of the recording.
  This timestamp indicates the timing of the records and allows synchronisation of a trajectory and a state recording.
* the size, in bytes, of the record; encoded as an 8 bytes little endian unsigned integer.
* the record itself as a protobuf message.

In the case of a trajectory recording, each record contains a ``GetFrameResponse`` message.
This message contains two fields: the frame index and the frame itself.
The frame index is generally an integer that gets incremented each time the server register a frame to broadcast.
However, its value is only significant when it is 0 as it means the frame needs to be reset;
for instance because the server loaded a new simulation. The frame is a :ref:`FrameData <traj-and-frames>`.

In the case of a shared state recording, each record contains a :ref:`StateUpdate <state-updates>` message.


Recording with Python
--------------------------------

How to record
~~~~~~~~~~~~~

NanoVer sessions can be recorded using the :mod:`nanover.omni.record` module.
Here is an example of how to define the file names and paths for the recording and pass them to the recording function:

.. code:: python

    from nanover.omni.record import record_from_server
    # Define the .traj and .state file names and paths
    traj_path = 'simulation_recording.traj'
    state_path = 'simulation_recording.state'
    # create a recording from a server and save it to the files
    record_from_server("localhost:38801", traj_path, state_path)

How to visualise recordings
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Visualising and playing back recordings can be done using :mod:`nanover.omni.playback` module.
The Python Server can stream recorded NanoVer streams read by a ``PlaybackSimulation`` object to a client. The client then plays back the recording as if it were
a live stream.
The server sends the frames and state updates whilst trying to respect the timing dictated by the timestamps stored
in the file.

.. code:: python

    from nanover.omni import OmniRunner
    from nanover.omni.playback import PlaybackSimulation
    simulation_recording = PlaybackSimulation(name='simulation-recording', traj='files/simulation_recording.traj',
                                           state='files/simulation_recording.state')
    # Create a runner for the simulation
    recording_runner = OmniRunner.with_basic_server(simulation_recording, name='simulation-recording-server')
    # Start the runner
    recording_runner.next()
    # Close the runner
    recording_runner.close()

.. note::

    Further instructions and information on how to record and replay using the NanoVer Python module can be found in this notebook `recording_and_replaying.ipynb <https://github.com/IRL2/nanover-protocol/blob/main/examples/basics/recording_and_replaying.ipynb>`_.

Recording with the Rust Server
------------------------------

How to record
~~~~~~~~~~~~~

The Rust Server takes a snapshot of the streams 30 times a second (although this may change with
issues `#200 <https://github.com/IRL2/nanover-rs/issues/200>`_ and
`#201 <https://github.com/IRL2/nanover-rs/issues/201>`_).

When using the ``nanover-cli`` command via the command line, use the ``--trajectory`` argument to specify the file that
will store the recording of the frame stream, and the ``--state`` argument to specify the file that will store
the recording of the shared state updates.

.. code-block::

    # For Windows Powershell
    .\nanover-cli.exe "simulation.xml" --trajectory "my-trajectory.traj" --state "my-state.state"

On the graphical interface, the files are specified in the ``Recording`` section before starting the server
(see :ref:`rust_server_via_the_gui`).

How to visualise recordings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Using the the command line**, providing only a ``.traj`` file will stream the frames only,
and providing only a ``.state`` file will stream the state updates only.
In order to send both streams together, provide the two file paths separated by a colon:

.. code-block::

    # For Windows Powershell
    .\nanover-cli.exe "my-trajectory.traj:my-state.state"


**Using the graphical interface**, add a recording to the list of simulations using the ``+ Recording`` button,
then choose the files.


Reading recordings using mdanalysis in python
-------------------------------

Recordings can be read and manipulated using the NanoVer python library.

The :py:mod:`nanover.mdanalysis` module allows to read a trajectory recording as an
`MDAnalysis Universe <https://userguide.mdanalysis.org/stable/universe.html#universe>`_.
As MDAnalysis does not support time-dependant topologies, only frames that correspond to the first topology in the
recording are read as part of the Universe.
If the topology changes throughout the recording, for instance because another simulation was loaded,
the library issues a warning and the frames with the new topology are ignored.

See the example code below, or check out the
`mdanalysis_nanover_recording <https://github.com/IRL2/nanover-protocol/blob/main/examples/mdanalysis/mdanalysis_nanover_recording.ipynb>`_
jupyter notebook tutorial for further information.

.. code:: python

    import MDAnalysis as mda
    from nanover.mdanalysis import NanoverParser, NanoverReader
    import matplotlib.pyplot as plt

    u = mda.Universe(
        'hello.traj',
        format=NanoverReader,
        topology_format=NanoverParser,
    )

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


Lower level methods are available in :py:mod:`nanover.mdanalysis.recordings` to read the content of the files directly.
This module is used in the `state-utils <https://github.com/IRL2/nanover-utils>`_ utility that allows to read shared
state recordings in a python script or with the command line.