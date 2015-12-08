from socket import *
import sys
from tools.argparcer import ArgParcer
from client.listenerthread import ListenerThread
__author__ = 'bensoer'


'''
PARAMETERS

-h host to connect to
-p port to connect to host on

-lp port to listen on
'''

arguments = sys.argv
'fetch the arguments we need'
host = ArgParcer.getValue(arguments, "-h")
port = int(ArgParcer.getValue(arguments, "-p"))
listeningPort = int(ArgParcer.getValue(arguments, "-lp"))

'create the socket to communicate over'
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('localhost', listeningPort))

'create the listener socket for incoming messages'
listenerThread = ListenerThread(clientSocket)
listenerThread.start()

'now start allowing user to type'

print("Setup Configured. Chat has Been Configured")
while True:
    message = input()

    if message == "exit":
        listenerThread.stopThread()
        break
    clientSocket.sendto(message.encode(), (host, port))
