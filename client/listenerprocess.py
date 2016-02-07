__author__ = 'bensoer'
import select

class ListenerProcess:

    __keepListening = True
    __connections = {}

    def __init__(self, socket, decryptor):
        self.__socket = socket
        self.__socket.setblocking(0)
        self.__decryptor = decryptor

        'in python this is apparently the only way to remember what file descriptor belongs to what socket'
        fileno = self.__socket.fileno()
        self.__connections[fileno] = self.__socket

        print("Listener Thread Initialized")


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
                    encryptedMessage = message.decode()
                    decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                    print(decryptedMessage)

            '''
            try:
                message, address = self.__socket.recvfrom(2048)
                encryptedMessage = message.decode()
                decryptedMessage = self.__decryptor.decrypt(encryptedMessage)
                print(decryptedMessage)
            except Exception:
                pass
            '''