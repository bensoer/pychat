from socket import *
import sys
import random
import os
import signal
from tools.argparcer import ArgParcer
from client.listenerprocess import ListenerProcess
from crypto.cryptor import Cryptor
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

'setup cryptor'
cryptor = Cryptor()
cryptor.setArguments(arguments)
cryptor.setAlgorithm(algorithm)
if cryptor.testAlgorithm():
    cryptor.loadAlgorithm()

'now fork to put the listener on a seperate process that won\'t block us'
pid = os.fork()
if pid <= 0:

    if pid < 0:
        'in case this is the error condition'
        print("SystemError Generating Child Process. Terminating")
        exit(1)
    elif pid == 0:
        'else we are in the child then'
        listenerProcess = ListenerProcess(clientSocket, cryptor)
        listenerProcess.start()
        'although this line will never be hit. its good to have as insurance'
        exit(0)
else:

    'if program makes it here. We must be in the parent'
    def signal_handler(signo, frame):
        print('Terminating Chat Engine')
        os.kill(pid, signal.SIGTERM)
        print('Successsfuly Terminated Listener Process')
        print('Now Self Terminating')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    'get and send the initialization message'
    initMessage = cryptor.getInitializationMessage()
    if initMessage != "":
        clientSocket.sendto(initMessage.encode(), (host, port))

    print("Setup Configured. Chat has Been Configured")

    'now start allowing user to type'
    while True:
        message = input()

        if message == "exit":
            'honey i killed the kids...'
            print('Terminaitng Chat Engine')
            os.kill(pid, signal.SIGTERM)
            print('Successfuly Terminated Listener Process')
            print('Now Self Terminating')
            break
        else:
            message = username + ": " + message
            encryptedMessage = cryptor.encrypt(message)
            clientSocket.sendto(encryptedMessage.encode(), (host, port))