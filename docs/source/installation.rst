============
Installation
============

Prerequisites
=============

You must have python 3.4 installed on your system. On linux this is available on most distros as `python3`. You can check by typing
`python3 --version` into your linux bash

You will need to have pip installed aswell in order to download the `pycrypto` library needed for some of the algorithms

Installation
============

For the rest of the app:
 1. Download the latest release from https://github.com/bensoer/pychat/releases
 2. Execute ``sudo pip3 install -r requirements.txt`` to install dependencies

Quickstart
==========
Start the program by calling

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher

This will start PyChat on `localhost` calling another user on port `7000` and listening for responses on `8000`. The converstion
will be encrypted with a `CaesarCipher`. Your username for the other user will appear in this example as `bert`. Note that
the CaesarCipher has additional optional parameters. Since we did not use them, default CaesarCipher setings were used. For details
on these optional parameters to this example, see the `CaesarCipher` section in the `Available Encryption/Decryption Algorithms`
section of the readme.

See the `Parameters` section for all common valid parameters


