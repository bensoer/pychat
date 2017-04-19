=======================
Verification Algorithms
=======================

Verification Algorithms are hashing algorithms that are generated and sent with every message from pychat. In order to
use verification algorithms, the ``-v`` flag must be set on all clients along with the same verification algorithm being
selected on each system. When each message is sent, a hash will be generated and appended to the beginning of each
message. Upon receival, pychat will decrypt and verify the message against the hashing algorithm. If the hashing fails
a warning message will be printed to console before the original message is printed. Regardless of whether the
hash is valid or not, the original message will always be printed.

Below lists all options that are currently implemented in pychat

MD2
===
Verify message integrity using MD2 hashing algorithm

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v MD2


MD4
===
Verify message integrity using MD4 hashing algorithm

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v MD4


MD5
===
Verify message integrity using MD5 hashing algorithm

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v MD5


SHA1
====
Verify message integrity using SHA1 hashing algorithm

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v SHA1


SHA224
======
Verify message integrity using SHA224 hashing algorithm

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v SHA224


SHA256
======
Verify message integrity using SHA256 hashing algorithm

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v SHA256


SHA384
======
Verify message integrity using SHA384 hashing algorithm

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v SHA384


SHA512
======
Verify message integrity using SHA512 hashing algorithm

Example
-------
.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v SHA512

HMAC
====
Verify message integrity using MAC algorithm. This MAC algorithm incorporates a hashing function and a password
to generate a verifiable signature by both parties

Only the `-hk` parameter listed below is **required**

+-----------+-------------------------------------------------------------------------------------------------------+
| Parameter | Description                                                                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -hk       || The shared password used for generating the hash signature                                           |
+-----------+-------------------------------------------------------------------------------------------------------+
| -hm       || The hashing mode to be used. Default is SHA1.                                                        |
|           || Values can be SHA1, SHA224, SHA256, SHA384, SHA512, MD5                                              |
+-----------+-------------------------------------------------------------------------------------------------------+

Example
-------
Set the hash password to `spaghetti` and the mode to `SHA256`

.. code-block:: bash

   python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher -v HMAC -hp spaghetti -hm SHA256
