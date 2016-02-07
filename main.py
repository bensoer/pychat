from socket import *
import sys
import random
import os
import signal
from tools.argparcer import ArgParcer
from client.listenerprocess import ListenerProcess
from crypto.encryptor import Encryptor
from crypto.decryptor import Decryptor
__author__ = 'bensoer'

'''
PARAMETERS

-h host to connect to
-p port to connect to host on

-lp port to listen on

-u [optional] set the username of the user. default is a random generated number
-a set encryption and decrytion algorithm
'''

arguments = sys.argv
'fetch the arguments we need'
host = ArgParcer.getValue(arguments, "-h")
port = int(ArgParcer.getValue(arguments, "-p"))
listeningPort = int(ArgParcer.getValue(arguments, "-lp"))
username = ArgParcer.getValue(arguments, "-u")
algorithm = ArgParcer.getValue(arguments, "-a")

'configure username if it was defined'
if username == "":
    username = str(random.random())

'create the socket to communicate over'
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('localhost', listeningPort))

'setup encryptor'
encryptor = Encryptor()
encryptor.setArguments(arguments)
encryptor.setAlgorithm(algorithm)
if encryptor.testAlgorithm():
    encryptor.loadAlgorithm()

'setup decryptor'
decryptor = Decryptor()
decryptor.setArguments(arguments)
decryptor.setAlgorithm(algorithm)
if decryptor.testAlgorithm():
    decryptor.loadAlgorithm()

'now fork to put the listener on a seperate process that won\'t block us'
pid = os.fork()
if pid <= 0:

    if pid < 0:
        'in case this is the error condition'
        print("SystemError Generating Child Process. Terminating")
        exit(1)
    elif pid == 0:
        'else we are in the child then'
        listenerProcess = ListenerProcess(clientSocket, decryptor)
        listenerProcess.start()
        'although this line will never be hit. its good to have as insurance'
        exit(0)
else:
    'now start allowing user to type'

    print("Setup Configured. Chat has Been Configured")

    while True:
        message = input()

        if message == "exit":
            'honey i killed the kids...'
            os.kill(pid, signal.SIGTERM)
            break
        else:
            message = username + ": " + message
            encryptedMessage = encryptor.encrypt(message)
            clientSocket.sendto(encryptedMessage.encode(), (host, port))



