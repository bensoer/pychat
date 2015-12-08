__author__ = 'bensoer'
from threading import Thread


class ListenerThread(Thread):

    def __init__(self, socket):
        Thread.__init__(self)
        self.__socket = socket
        print("Listener Thread Initialized")


    def run(self):
        while True:
            message, clientAddress = self.__socket.recvfrom(2048)
            print(message.decode())




