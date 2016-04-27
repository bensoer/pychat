#pychat

pychat is a UDP based terminal chatting program that allows multiple devices to communicate together over a secure
connection using an algorithm of their choice. The purpose of the project is to explore encryption algorithms and
sending data back and forth securely and minimizing options for external sources to decrypt the data

#Setup

The example system has been configured to work with `python3.4`. <br><br>
For the rest of the app:
 1. Install `virtualenv`
 2. Clone the project
 3. Create a local environment for `virtualenv`
 4. Import `requirements.txt` file into `virtualenv` to get all needed modules. PS: Currently there are none

Start the program by calling
```python
python main.py -h localhost -p 7000 -lp 8000 -u bert -a CaesarCipher
```
This will start PyChat on `localhost` calling another user on port `7000` and listening for responses on `8000`. The converstion
will be encrypted with a `CeasarCipher`. Your username for the other user will appear in this example as `bert`

See the `Parameters` section for all valid parameters

###Parameters
| Parameter | Description |
|-----------|-------------|
| -h | Set the host PyChat will be communicating with |
| -p | Set the port PyChat will be communicating with |
| -lp | Set the port PyChat will listen for incoming messages from |
| -u | Set the username for this user. Default is a random number |
| -a | Set the encryption / decryption algorithm used to secure messages in transit |

###Available Encryption/Decryption Algorithms
Pass the value to the `-a` parameter exactly as listed below to use the encryption algorithm
####Implemented
* CaesarCipher

####NotImplemented
* RandomCaesarCipher
* TranspositionCipher
* RSA

##Using the Example
After cloning the project you can start the example project simply by running `client.py` and then `client2.py`. Being
UDP no connection setup is needed so either client can be started first. The example is configured to run on localhost
on the same computer so you can watch a chat between two consoles. Thread management though has not been implemented
well and thus when you are done hitting `Ctrl+C` will cause the console to close and possibly crash close, which is
expected.

#File Structure

##Algorithms
The algorithms folder contains all algorithms for various forms of encrypting and decrypting messages. All of these
algorithm files must inherit from the `algorithminterface.py` file in order to conform to the application standards. The
`decrypt.py` and `encrypt.py` files located in the crypto folder rely on the conforming so as to ensure appropriate
methods are available to the client

##Crypto
The crypto folder contains the main `encryptor.py` and `decryptor.py` files which encrypt and decrypt data based on
passed in parameters determining which algorithm to use. These classes are the main entries used by the client to
encrypt and decrypt messages being sent

##Client
The client folder holds all logic for the client console's operations, including sending and recieving messages and then
communicating with the crypto library to parse messages.

The client is also in charge at initialization of taking in user parameters for the encryption and decryption algorithms.
These are used by the encryption and decryption classes to determine what algorithms to use and what are available
