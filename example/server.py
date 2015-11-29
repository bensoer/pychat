__author__ = 'bensoer'
from socket import *
serverPort = 1200
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print "Server is ready to recieve"
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print "Response: " + message
    message = raw_input('Send: ')
    serverSocket.sendto(message, clientAddress)