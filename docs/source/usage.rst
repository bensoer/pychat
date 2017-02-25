=====
Usage
=====

Parameters
==========
There are a number of basic parameters used in pychat by every algorithm. Each individual algorithm has additional
parameters that can be set, and are specified in the Algorithms section.

+----------------+----------------------------------------------------------------------------------+
| Parameter      | Description                                                                      |
+================+==================================================================================+
| -h             | Set the host pychat will be communicating with                                   |
+----------------+----------------------------------------------------------------------------------+
| -p             | Set the port pychat will be communicating with                                   |
+----------------+----------------------------------------------------------------------------------+
| -lp            | Set the port PyChat will listen for incoming messages from                       |
+----------------+----------------------------------------------------------------------------------+
| -u             | Set the username for this user. Default is a random number                       |
+----------------+----------------------------------------------------------------------------------+
| -a             | Set the encryption / decryption algorithm used to secure messages in transit     |
+----------------+----------------------------------------------------------------------------------+
| -v             | Set optionaly the verification algorithm to be used on each message              |
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
| ---GUI         | Starts pychat in GUI mode, launching the GUI to interact with the app (not implemented) |
+----------------+-----------------------------------------------------------------------------------------+