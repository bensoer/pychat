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
