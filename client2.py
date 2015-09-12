__author__ = 'bensoer'
from socket import *
import threading
import sys

bufferSize = 2048

serverName = 'localhost'
serverPort = 1200
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))


def checkForReceiving():
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    print "Response: " + message
    threading.Timer(1, checkForReceiving).start()


clientPort = 1400
clientName = 'localhost'
threading.Timer(1, checkForReceiving).start()
print "Server is ready to recieve"




while True:
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = raw_input()
    if message == '-1':
        sys.exit(0)

    clientSocket.sendto(message, (clientName, clientPort))
    #response, serverAddress = clientSocket.recvfrom(2048)
    clientSocket.close()