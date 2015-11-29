#pychat

pychat is a UDP based terminal chatting program that allows multiple devices to communicate together over a secure
connection using an algorithm of their choice. The purpose of the project is to explore encryption algorithms and
sending data back and forth securely and minimizing options for external sources to decrypt the data

#Setup

Currently there is only the example system which has been recently updated to work with `python3.4`. A `virtualenv` will
be added eventually allowing any user to use the system at any given time without having to upgrade system installed
python (Fedora and Ubuntu by default come with older python versions).

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