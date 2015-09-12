__author__ = 'bensoer'
from socket import *
import threading
import sys

bufferSize = 2048

serverName = 'localhost'
serverPort = 1400
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))

canCheck = 1



def checkForReceiving():
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    print "Response: " + message
    if canCheck == 1:
        t = threading.Timer(1, checkForReceiving)
        t.start()




clientPort = 1200
clientName = 'localhost'

#child = threading.Thread(target=timerManager)
#child.start()
t = threading.Timer(1, checkForReceiving)
t.start()
print "Server is ready to recieve"


while True:
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = raw_input()
    if '-1' in message:
        print "Quiting..Bye"
        canCheck = 0
        clientSocket.close()
        t.cancel()
        break
    else:
        clientSocket.sendto(message, (clientName, clientPort))
        #response, serverAddress = clientSocket.recvfrom(2048)
        clientSocket.close()

print "made it here"
canCheck = 0
t.cancel()
