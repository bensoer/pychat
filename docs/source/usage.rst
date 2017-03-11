=====
Usage
=====
The documentation for usage has been spread out into two sections. Below lists all global information that
can be configured regardless of the algorithm chosen with pychat. Depending on the selected algorithm, additional
parameters may be required ontop of those listed below. For algorithm specific parameters see the
:ref:`algorithms_reference_label` section

For quickstart documentation see the bottom of the :ref:`installation_reference_label` section

Parameters
==========
Below lists all of the global parameters that can be used with any algorithm.

+----------------+----------------------------------------------------------------------------------+
| Parameter      | Description                                                                      |
+================+==================================================================================+
| -h             | Set the host pychat will be communicating with                                   |
+----------------+----------------------------------------------------------------------------------+
| -p             | Set the port pychat will be communicating with                                   |
+----------------+----------------------------------------------------------------------------------+
| -lp            | Set the port pychat will listen for incoming messages from                       |
+----------------+----------------------------------------------------------------------------------+
| -u             | Set the username for this user. Default is a random number                       |
+----------------+----------------------------------------------------------------------------------+
| -a             | Set the encryption / decryption algorithm used to secure messages in transit     |
+----------------+----------------------------------------------------------------------------------+
| -v             | Set optionally the verification algorithm to be used on each message             |
+----------------+----------------------------------------------------------------------------------+

Flags
=====
On top of the global parameters there are also flags that can be set. These will enable certain modes of pychat
and change how it will operate

+----------------+-----------------------------------------------------------------------------------------+
| Flag           | Description                                                                             |
+================+=========================================================================================+
| ---DEBUG       | Enable Debug Mode. Debug logging will be written to console                             |
+----------------+-----------------------------------------------------------------------------------------+

.. | ---GUI         | Starts pychat in GUI mode, launching the GUI to interact with the app (not implemented) |
   +----------------+-----------------------------------------------------------------------------------------+

Console Execution
=================
Running pychat uses the same setup for all end systems wanting to communicate through pychat. Starting a pychat client
is initiated in the console by simply running pychat with the appropriate parameters above along with any required
parameters with the selected algorithm in the following format:

.. code-block:: bash

    python3 ./pychat.py -h <host> -lp <listeningport> -p <connectionport> [-u <username>] -a <algorithm> [-v <verificationalgorithm>] [<FLAGS>]

Note that by executing the application with no parameters will print a simple help information to the console and terminate