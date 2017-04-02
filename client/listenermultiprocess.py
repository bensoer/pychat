__author__ = 'bensoer'
import select
from tools.commandtype import CommandType

class ListenerMultiProcess:

    __keepListening = True
    __connections = {}
    __firstMessageReceived = False
    __firstMessage = b''
    __rejectFirstMessageMatches = False
    __replySent = False

    def __init__(self, socket, decryptor, child_conn_pipe):
        '''
        constructor. This sets up all attributes needed for the listener process to function
        :param socket: Socket - the socket the listener process will listen on
        :param decryptor: Decryptor - the decryption instance the recieved message will be put through before
        printing to screen
        :return: void
        '''

        self.__socket = socket
        self.__socket.setblocking(0)
        self.__decryptor = decryptor
        self.__child_conn_pipe = child_conn_pipe

        'in python this is apparently the only way to remember what file descriptor belongs to what socket'

        fileno = self.__socket.fileno()
        self.__connections[fileno] = self.__socket

        print("Listener Process Initialized")


    def start(self):
        '''
        start is called by the parent process to initialize the child process task. This method is simply the kickoff
        point of the child process, and auto contains it within a managed object
        :return: void
        '''

        epoll = select.epoll()
        epoll.register(self.__socket, (select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP | select.EPOLLET))

        while self.__keepListening:
            events = epoll.poll()
            for fd, eventType in events:
                if eventType & (select.EPOLLHUP|select.EPOLLERR):
                    print("SystemError Recieving Message. Epoll Errored. Closing Descriptor")
                    epoll.unregister(fd)
                else:
                    socket = self.__connections[fd]
                    message, address = socket.recvfrom(2048)

                    encryptedMessage = message

                    #if we haven't recieved the first message yet then this one is it
                    if self.__firstMessageReceived == False:
                        self.__firstMessageReceived = True
                        # give the message first to the algorithm to determine whether we print it or not

                        #writeToConsole = self.__decryptor.giveFirstMessage(encryptedMessage)
                        self.__child_conn_pipe.send([CommandType.GiveFirstMessage, encryptedMessage])
                        writeToConsole = self.__child_conn_pipe.recv()[0]

                        # check if a reply has been sent
                        if self.__replySent == False:
                            #firstMessageToBeSent = self.__decryptor.getInitializationMessage()
                            self.__child_conn_pipe.send([CommandType.GetInitializationMessage])
                            firstMessageToBeSent = self.__child_conn_pipe.recv()[0]
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
                            #decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                            self.__child_conn_pipe.send([CommandType.Decrypt, encryptedMessage])
                            decryptedMessage = self.__child_conn_pipe.recv()[0]
                            #if the message is empty though don't bother printing it
                            if decryptedMessage != "":
                                print(decryptedMessage)
                        else:
                            # if you don't want firstMessage to write to console, assume u never want it to
                            self.__rejectFirstMessageMatches = True
                    else:

                        #check if receiveNextMessageThroughFirstMessage is true
                        self.__child_conn_pipe.send([CommandType.ReceiveMessageThroughFirst, encryptedMessage])
                        receiveNextMessageThroughFirstMessage = self.__child_conn_pipe.recv()[0]
                        if receiveNextMessageThroughFirstMessage:
                            self.__child_conn_pipe.send([CommandType.GiveFirstMessage, encryptedMessage])
                            writeToConsole = self.__child_conn_pipe.recv()[0]

                            # check the original reply has been sent
                            if self.__replySent == True:
                                # check if the algo wants us to resend original message
                                self.__child_conn_pipe.send([CommandType.SendFirstMessageAgain])
                                sendFirstMessageAgain = self.__child_conn_pipe.recv()[0]
                                if sendFirstMessageAgain:

                                    # firstMessageToBeSent = self.__decryptor.getInitializationMessage()
                                    self.__child_conn_pipe.send([CommandType.GetInitializationMessage])
                                    firstMessageToBeSent = self.__child_conn_pipe.recv()[0]
                                    # if first message does exist then send it
                                    if len(firstMessageToBeSent) > 0:
                                        socket.sendto(firstMessageToBeSent, address)

                            if writeToConsole:
                                # if you wanted to write to console, then everything should be able to write to console
                                self.__rejectFirstMessageMatches = False
                                #if we are to write to console then decrypt the message using algorithms decryptor
                                #decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                                self.__child_conn_pipe.send([CommandType.Decrypt, encryptedMessage])
                                decryptedMessage = self.__child_conn_pipe.recv()[0]
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
                                    #decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                                    self.__child_conn_pipe.send([CommandType.Decrypt, encryptedMessage])
                                    decryptedMessage = self.__child_conn_pipe.recv()[0]
                                    print(decryptedMessage)
                            else:
                                # decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                                self.__child_conn_pipe.send([CommandType.Decrypt, encryptedMessage])
                                decryptedMessage = self.__child_conn_pipe.recv()[0]
                                print(decryptedMessage)

