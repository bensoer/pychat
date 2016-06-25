__author__ = 'bensoer'
from threading import Thread
import select

class ListenerThread(Thread):

    __keepListening = True

    __connections = {}
    __firstMessageReceived = False
    __firstMessage = b''
    __rejectFirstMessageMatches = False
    __replySent = False
    __epoll = None

    def __init__(self, socket, decryptor):
        Thread.__init__(self)
        self.__socket = socket
        self.__socket.setblocking(0)
        self.__decryptor = decryptor

        fileno = self.__socket.fileno()
        self.__connections[fileno] = self.__socket

        print("Listener Thread Initialized")

    def stopThread(self):
        self.__keepListening = False
        #self.__epoll.unregister(self.__socket.fileno())
        #self.__socket.close()
        #self.__epoll.close()
        self._stop()

    def run(self):

        self.__epoll = select.epoll()
        self.__epoll.register(self.__socket, (select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP | select.EPOLLET))

        while self.__keepListening:
            events = self.__epoll.poll()
            for fd, eventType in events:
                if eventType & (select.EPOLLHUP|select.EPOLLERR):
                    print("SystemError Recieving Message. Epoll Errored. Closing Descriptor")
                    self.__epoll.unregister(fd)
                else:
                    socket = self.__connections[fd]
                    message, address = socket.recvfrom(2048)

                    encryptedMessage = message

                    #if we haven't recieved the first message yet then this one is it
                    if self.__firstMessageReceived == False:
                        self.__firstMessageReceived = True
                        # give the message first to the algorithm to determine whether we print it or not
                        writeToConsole = self.__decryptor.giveFirstMessage(encryptedMessage)

                        # check if a reply has been sent
                        if self.__replySent == False:
                            firstMessageToBeSent = self.__decryptor.getInitializationMessage()
                            # if first message does exist then send it
                            if len(firstMessageToBeSent) > 0:
                                socket.sendto(firstMessageToBeSent, address)
                            self.__replySent = True

                            # keep track of this first message
                            self.__firstMessage = encryptedMessage

                        if writeToConsole == True:
                            # if you wanted to write to console, then everything should be able to write to console
                            self.__rejectFirstMessageMatches = False
                            #if we are to write to console then decrypt the message using algorithms decryptor
                            decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                            #if the message is empty though don't bother printing it
                            if decryptedMessage != "":
                                print(decryptedMessage)
                        else:
                            # if you don't want firstMessage to write to console, assume u never want it to
                            self.__rejectFirstMessageMatches = True
                    else:
                        # drop anything that looks like the first message if rejection is set
                        if self.__rejectFirstMessageMatches:
                            if encryptedMessage != self.__firstMessage:
                                decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                                print(decryptedMessage)
                        else:
                            decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                            print(decryptedMessage)