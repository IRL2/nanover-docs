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

######################
NanoVer message stream
######################

A NanoVer server communicates to connected clients via a stream of messages. The standard server uses messages of three
types: ``command```, ``state``, ``frame`` for requests, shared data, and simulation information respectively. A NanoVer
recording is a record of this stream of messages and the times they arrived.

.. note::

   Previously, NanoVer recordings were a pair of files ending in ``.traj`` and ``.state`` respectively.
   This format is now obsolete and can be converted using `a simple command line tool <https://github.com/IRL2/nanover-recording-converter>`_.

----

#####################
Recording file format
#####################

Overview
########

The recording file is an uncompressed `zip archive <https://en.wikipedia.org/wiki/ZIP_(file_format)>`_ comprised of
at least two files:

* **The messages file**, ``messages.msgpack``, which contains the sequence of messages, each individually encoded with MessagePack and
  concatenated into a single binary file.

* **The index file**, ``index.msgpack``, which is a list of metadata entries for each frame, specifying at the minimum their position in
  the ``messages.msgpack`` file, the timestamp of their arrival, and the types of message contained. This binary file
  is a single list encoded with MessagePack.

Index file
##########

The index file exists to provide an overview of the content of the recording file and allow efficient access to
individual messages. It is a list of objects, each representing a message present in the recording, with the following
fields:

* The ``offset`` in bytes where the MessagePack data of the message begins in the messages file.
* The ``length`` in bytes of the MessagePack data of the message.
* A ``metadata`` object pertaining to the message, with at least the following fields:

  * The ``timestamp`` for when the message was received.
  * The ``types`` list, noting the types the message contains (e.g ``frame``, ``state``, ``command``).

.. code:: python

    # example index data
    [
        {
            "offset": 0,
            "length": 64,
            "metadata": {
                "timestamp": 0,
                "types": ["frame"],
            },
        },
        {
            "offset": 64,
            "length": 64,
            "metadata": {
                "timestamp": 100,
                "types": ["state"],
            },
        }
    ]

|
