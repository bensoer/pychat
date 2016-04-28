#pychat

pychat is a UDP based terminal chatting program that allows multiple devices to communicate together over a secure
connection using an algorithm of their choice. The purpose of the project is to explore encryption algorithms and
sending data back and forth securely and minimizing options for external sources to decrypt the data

#Setup

## Prerequisites
You must have python 3.4 installed on your system. On linux this is available on most distros as `python3`. You can check by typing
`python3 --version` into your linux bash

You will need to have pip installed aswell in order to download the `pycrypto` library needed for some of the algorithms

## Installation

For the rest of the app:
 1. Download the latest release from [https://github.com/bensoer/pychat/releases](https://github.com/bensoer/pychat/releases)
 2. Execute `pip install -r requirements.txt`
 3. Start the program by calling
```python
python3 pychat.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher
```
This will start PyChat on `localhost` calling another user on port `7000` and listening for responses on `8000`. The converstion
will be encrypted with a `CaesarCipher`. Your username for the other user will appear in this example as `bert`. Note that
the CaesarCipher has additional optional parameters. Since we did not use them, default CaesarCipher setings were used. For details
on these optional parameters to this example, see the `CaesarCipher` section in the `Available Encryption/Decryption Algorithms` 
section of the readme.

See the `Parameters` section for all common valid parameters

## Parameters
| Parameter | Description |
|-----------|-------------|
| -h | Set the host PyChat will be communicating with |
| -p | Set the port PyChat will be communicating with |
| -lp | Set the port PyChat will listen for incoming messages from |
| -u | Set the username for this user. Default is a random number |
| -a | Set the encryption / decryption algorithm used to secure messages in transit |

## Available Encryption/Decryption Algorithms
Pass the value to the `-a` parameter exactly as listed below to use the encryption algorithm


### Implemented
* CaesarCipher
* RandomCaesarCipher
* TranspositionCipher

#### CaesarCipher
In addition to the above mentioned parameters. 1 other parameter can be passed to alter this algorithm. It is an optional parameter

|Parameter | Description|
|----------|------------|
| -o | Set the offset value of how many letters down in the caesarcipher translation the algorithm should go|

#### RandomCaesarCipher
In addition to the above mentioned parameters. 2 other parameters can be passed to alter this algorithm. Neither parameter is requires

|Parameter | Description|
|----------|------------|
| -s | Set the seed value for the rand. Used for generating the scrambled alphabet|
| -o | Set the offset value of how many letters down in the caesarcipher translation the algorithm should go|

#### NotImplemented
* RSA

# Developer Notes
_Apr 28/2016_ - Three new ciphers have been added! Second Release is coming!