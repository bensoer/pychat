__author__ = 'bensoer'

from socket import *
import sys
from tools import ArgParcer
from client import ListenerThread


'''
PARAMETERS

-h host to connect to
-p port to connect to host on
'''

arguments = sys.argv
'fetch the arguments we need'
host = ArgParcer.getValue(arguments, "-h")
port = int(ArgParcer.getValue(arguments, "-p"))

'create the socket to communicate over'
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind((host, port))

'create the listener socket for incoming messages'
listenerThread = ListenerThread(clientSocket)
listenerThread.start()




'join the thread so it won\'t exit before we do'
listenerThread.join()