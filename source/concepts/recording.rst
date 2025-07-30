.. _recordinginnanover:

====================
Recording in NanoVer
====================

This pages introduces: (a) the NanoVer data streams, which you can record to 'save' your NanoVer session; and (b) the
file format of the recorded data.
Head to the :ref:`basics` tutorial page for more information on how to
:ref:`record a NanoVer session <basicsrecordingasession>` and how to
:ref:`process NanoVer recordings <basicsprocessingnanoverrecordings>`.

.. contents:: Contents
    :depth: 2
    :local:

----

####################
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

#####################
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
