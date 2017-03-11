#PyChat

PyChat is a UDP based terminal chatting program that allows multiple devices to communicate together over a secure connection using an algorithm of their choice. The purpose of the project is to explore encryption algorithms and sending data back and forth securely and minimizing options for external sources to decrypt the data. The project is maintained by [Ben Soer](https://github.com/bensoer) and [Kurtis Bohlen](https://github.com/kbohlen).

#Setup

## Prerequisites
You must have python 3.4 installed on your system. On linux this is available on most distros as `python3`. You can check by typing `python3 --version` into your linux bash

You will need to have pip installed aswell in order to download the `pycrypto` library needed for some of the algorithms

## Installation/Quickstart

For the rest of the app:
 1. Download the latest release from [https://github.com/bensoer/pychat/releases](https://github.com/bensoer/pychat/releases)
 2. Execute `sudo pip3 install -r requirements.txt`
 3. Start the program by calling
```python
python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher
```
This will start PyChat on `localhost` calling another user on port `7000` and listening for responses on `8000`.
The converstion will be encrypted with a `CaesarCipher`. Your username for the other user will appear in this example as `bert`.
Note that the CaesarCipher has additional optional parameters.
Since we did not use them, default CaesarCipher setings were used.

For full documentation see [https://pychat.readthedocs.io](htpps://pychat.readthedocs.io)

# Developer Notes
_Apr 28/2016_ - Three new ciphers have been added! Second Release is coming!
_March 10/2017_ - Pure AES, RSA algorithms along with added Hashing functionality
