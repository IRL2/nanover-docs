Recording data
==============

.. _Rust server: https://github.com/IRL2/nanover-rs

For a NanoVer session to be usefull beyond the time the users spend in VR, it needs to be recorded. This recorded can then be analysed or played back to get insight.

What is recorded
----------------

NanoVer can record two different streams:

* the stream of simulation frame,
* and the stream of updates of the shared state.

These two streams are the ones sent to the clients but they are supplemented with a timestamp that allows to synchronise the streams. Each stream is stored in a separate file.

How to record
-------------

Recording is done by the `Rust server`_. The server takes a snapshot of the streams 30 times a second (though, this may change with `issue #200 <https://github.com/IRL2/nanover-rs/issues/200>`_ and issue `#201 <https://github.com/IRL2/nanover-rs/issues/201>`_).

When using the `nanover-cli` command line, use the `--trajectory` argument to specify the file that will store the recording of the frame stream, and the `--state` argument to specify the file that will store the recording of the state updates. On the graphical interface, the files are specified in the "Recording" section before starting the server.

By convention, recordings of the frame stream end with the `.traj` file extension, while recordings of the shared state stream end with the `.state` file extension.


Visualise recordings
--------------------

Recordings can be visualised using the `Rust server`_. The server will send the recorded streams to the client that will be able to show it as if they were a live streams.

Using the the command line, providing a file with the `.traj` file extension will stream that frame stream only, providing a file with the `.state` extension will stream the state updates only. In order to send both streams together, provide the two file paths separated by a column, for instance: ``my-trajectory.traj:my-state.state``.

Using the graphical interface, add a recording to the list of simulations using the "+ Recording" button, then choose the files.

The server sends the frames and the state updates and tries to respect the timing dictated by the timestamps stored in the file.

Read recordings using python
----------------------------

Recordings can be read and manipulated using the NanoVer python library.

The :py:mod:`nanover.mdanalysis` module allows to read a trajectory recording as an `MDAnalysis Universe <https://userguide.mdanalysis.org/stable/universe.html#universe>`_. As MDAnalysis does not support time-dependant topologies, only frames that correspond to the first topology in the recording are read as partof the Universe. If the topology changes throughout the recording, for instance because another simulation was loaded, the library issues a warning and the frames with the new topology are ignored.

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


Lower level methods are available in :py:mod:`nanover.mdanalysis.recordings` to read the content of the files directly. This module is used in the `state-utils <https://github.com/IRL2/state-utils>`_ utility that allows to read shared state recordings in a python script or with the command line.

Recording format
----------------

The current version of the file format is version 2. A file contains a header and a sequence of records.

The header contains two fields, stored as little endian 8 bytes unsigned integers:

* a magic number, its value is 6661355757386708963. This value was chosen arbitrarily and needs to be the first 8 bytes of the file to indicate it is indeed a NanoVer recording. A file without this magic number is not a NanoVer recording, however one need to keep in mind that a file that starts with that value could still not be a valid recording and should handle errors accordingly.
* the version of the file format. This version number dictates how the rest of the file will be written or parsed. Any change to the file format needs to increment this file format version The current version is 2.

A record contains:

* a timestamp encoded as a little endian 16 bytes unsigned integer that indicates the time, in microseconds, since the beginning of the recording. This timestamp indicates the timing of the records and allows to synchronise a trajectory and a state recordings.
* the size, in bytes, of the record; encoded as an 8 bytes little endian unsigned integer.
* the record itself as a protobuf message.

In the case of a trajectory recording, each record contains a `GetFrameResponse` message. This message contains two fields: the frame index and the frame itself. The frame index is generally an integer that gets incremnted each time the server register a frame to broadcast. However, its value is only sognificant when it is 0 as it means the frame needs to be reset; for instance because the server loaded a new simulation. The frame is a :ref:`FrameData <traj-and-frames>`.

In the case of a shared state recording, each record contains a :ref:`StateUpdate <state-updates>` message.
