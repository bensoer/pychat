from socket import *
import sys
import random
from tools.argparcer import ArgParcer
from client.listenerthread import ListenerThread
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
encryptor.setAlgorithm(algorithm)
encryptor.testAlgorithm()

'setup decryptor'
decryptor = Decryptor()
decryptor.setAlgorithm(algorithm)
decryptor.testAlgorithm()


'create the listener socket for incoming messages'
listenerThread = ListenerThread(clientSocket, decryptor)
listenerThread.start()

'now start allowing user to type'

print("Setup Configured. Chat has Been Configured")
while True:
    message = input()

    if message == "exit":
        listenerThread.stopThread()
        break
    else:
        message = username + ": " + message
        encryptedMessage = encryptor.encrypt(message)
    clientSocket.sendto(encryptedMessage.encode(), (host, port))
