__author__ = 'bensoer'
from threading import Thread

class ListenerThread(Thread):

    __keepListening = True

    def __init__(self, socket):
        Thread.__init__(self)
        self.__socket = socket
        self.__socket.setblocking(0)
        print("Listener Thread Initialized")

    def stopThread(self):
        self.__keepListening = False

    def run(self):
        while self.__keepListening:
            try:
                message, address = self.__socket.recvfrom(2048)
                print(message.decode())
            except Exception:
                pass








