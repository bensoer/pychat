.. _algorithms_reference_label:

==========
Algorithms
==========
Below lists all available algorithms on pychat including additional parameters and usages

CaesarCipher
============
Parameters listed below are **optional**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| | -o      | | Set the offset value of how many letters down in the caesarcipher                                   |
| |         | | translation the algorithm should go                                                                 |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
Set the offset value to 13 (Commonly known as ROTL13 encryption)

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -o 13


RandomCaesarCipher
==================
Parameters listed below are **optional**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -s        || Set the seed value for the rand. Used for generating the scrambled alphabet                          |
+-----------+-------------------------------------------------------------------------------------------------------+
|  -o       || Set the offset value of how many letters down in the caesarcipher translation                        |
|           || the algorithm should go                                                                              |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
Set the offset value to 5 and a randomization seed to 20

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a RandomCaesarCipher -o 5 -s 20

TranspositionCipher
===================
Parameters listed below are **required**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -k        || Set the key used for generating the transposition table                                              |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
Set the key value to 'spaghetti'

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a TranspositionCipher -k spaghetti

VigenereCipher
==============
Parameters listed below are **required**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -k        || Set the key word used for encryption                                                                 |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a VigenerCipher -k spaghetti

BeaufortCipher
==============
Parameters listed below are **required**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -k        || Set the key word used for encryption                                                                 |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a BeaufortCipher -k spaghetti

AESCipher
=========
Parameters listed below are **required**

This does not do a secure Diffie-Hellman Key Exchange of a randomly generated AES key, it uses SHA256 to hash the
password passed by the user

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -k        || Set the password which is then turned into the 256bit key for encryption                             |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
Set the key password to 'spaghetti'

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a AESCipher -k spaghetti

PureAESCipher
=============
PureAESCipher differs from AESCipher in being a pure implementation written by Kurtis Bohlen. Use of the `pycrypto`
library is not incorporated in this implementation

Parameters listed below are **required**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -k        || Set the key for encryption (must be 16,24, or 32 bytes long)                                         |
+-----------+-------------------------------------------------------------------------------------------------------+
| -m        || Set the block cipher mode of operation (default is CBC)                                              |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
Set the key to 'asixteenbyteword` and the mode to 'CBC' (default mode)

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a PureAESCipher -k asixteenbyteword -m CBC


DESCipher
=========
Parameters listed below are **required**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -k        || Set the key for encryption. It must be 16 characters long.                                           |
|           || Both users must enter the same key                                                                   |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
Set the key password to 'spaghetti'

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a DESCipher -k spaghetti

PureRSA
=======
PureRSA differs from a normal RSA implementation as it is a pure implementation written by Ben Soer. The `pycrypto`
library is not incorporated in the implementation of this algorithm

Parameters listed below are **required**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -p1       || Set first prime number for generating the public/private key pair                                    |
+-----------+-------------------------------------------------------------------------------------------------------+
| -p2       || Set second prime number for generating the public/private key pair                                   |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
Set the prime numbers to 5 and 11

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a PureRSA -p1 5 -p2 11
