from socket import *
import sys
import random
import os
import signal
from tools.argparcer import ArgParcer
#from client.listenerprocess import ListenerProcess
#from client.listenerthread import ListenerThread
from client.listenermultiprocess import ListenerMultiProcess
from crypto.cryptor import Cryptor
from multiprocessing import Process, Pipe
import threading
from tools.commandtype import CommandType

__author__ = 'bensoer'

'''
PARAMETERS

-h host to connect to
-p port to connect to host on

-lp port to listen on

-u [optional] set the username of the user. default is a random generated number
-a set encryption and decrytion algorithm
'''

arguments = sys.argv

'if no arguments passed. print help'
if len(arguments) <= 1:
    print("PyChat. A Console Chat Appliction Using Cryptographic Algorithms")
    print("Parameters:")
    print("\t -h : The host to connect to")
    print("\t -p : The port to the host to connect to")
    print("\t -lp : The port to receive messages over")
    print("\t -u : Username for this user when sending message (optional. default uses a number)")
    print("\t -a : Name of the Algorithm to be used in message transmission")
    exit(0)

'fetch the arguments we need'
host = ArgParcer.getValue(arguments, "-h")
port = int(ArgParcer.getValue(arguments, "-p"))
listeningPort = int(ArgParcer.getValue(arguments, "-lp"))
username = ArgParcer.getValue(arguments, "-u")
algorithm = ArgParcer.getValue(arguments, "-a")

'configure username if it was defined'
if username == "":
    username = str(random.random())

'create the socket to communicate over'
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('localhost', listeningPort))
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)

'setup cryptor'
cryptor = Cryptor()
cryptor.setArguments(arguments)
cryptor.setAlgorithm(algorithm)
if cryptor.testAlgorithm():
    cryptor.loadAlgorithm()

#listenerMultiProcess = ListenerMultiProcess(clientSocket, cryptor)
parent_conn, child_conn = Pipe()

'setup the listener multiprocess - passing it the pipe'
def bootstrapper(child_conn_pipe):
    components = child_conn_pipe.recv()
    #child_conn_pipe.close()
    listenerMultiProcess = ListenerMultiProcess(components[0], components[1], child_conn_pipe)
    listenerMultiProcess.start()
    # safety measure
    exit(0)

'''setup handler for pipe commands from the child multiprocess back to us. This is needed so as to keep the crypto
object in sync'''
def recv_handler():
    while True:
        back_command = parent_conn.recv()
        #print(back_command)
        command_code = back_command[0]

        # handler manipulation of cryptor here
        if command_code == CommandType.GiveFirstMessage:
            writeToConsole = cryptor.giveFirstMessage(back_command[1])
            parent_conn.send([writeToConsole])
        elif command_code == CommandType.GetInitializationMessage:
            message = cryptor.getInitializationMessage()
            parent_conn.send([message])
        elif command_code == CommandType.Decrypt:
            message = cryptor.decrypt(back_command[1])
            parent_conn.send([message])
        elif command_code == CommandType.Encrypt:
            message = cryptor.encrypt(back_command[1])
            parent_conn.send([message])
        else:
            print("Unknown Command Received")

'start the listener'
#listenerThread = ListenerThread(clientSocket, cryptor)
#listenerThread.start()
#multiprocess = Process(target=bootstrapper, args=(listenerMultiProcess))
multiprocess = Process(target=bootstrapper, args=(child_conn,))
multiprocess.start()

'start the thread to handle pipe commands'
parent_conn.send([clientSocket, cryptor])
t = threading.Thread(target=recv_handler)
t.daemon = True  # making it a daemon for some reason automatically deals with killing it once the main thread dies
t.start()


'now fork to put the listener on a seperate process that won\'t block us'
'''pid = os.fork()
if pid <= 0:

    if pid < 0:
        'in case this is the error condition'
        print("SystemError Generating Child Process. Terminating")
        exit(1)
    elif pid == 0:
        'else we are in the child then'
        listenerProcess = ListenerProcess(clientSocket, cryptor)
        listenerProcess.start()
        'although this line will never be hit. its good to have as insurance'
        exit(0)
else:
    'if program makes it here. We must be in the parent'
'''

'setup Ctrl+C handler'
def signal_handler(signo, frame):
    print('Terminating Chat Engine')
    #os.kill(pid, signal.SIGTERM)
    parent_conn.close()
    multiprocess.terminate()
    print('Successfully Terminated Listener Process')
    print('Now Self Terminating')
    exit(0)


signal.signal(signal.SIGINT, signal_handler)

'get and send the initialization message from the algorithm'
initMessage = cryptor.getInitializationMessage()
if len(initMessage) > 0:
    clientSocket.sendto(initMessage, (host, port))

print("Setup Configured. Chat has Been Configured")

'now start allowing user to type'
while True:
    message = input()

    if message == "exit":
        'honey i killed the kids...'
        print('Terminating Chat Engine')
        #os.kill(pid, signal.SIGTERM)
        #listenerThread.stopThread()
        parent_conn.close()
        multiprocess.terminate()
        print('Successfully Terminated Listener Process')
        print('Now Self Terminating')
        break
    else:
        message = username + ": " + message
        encryptedMessage = cryptor.encrypt(message)
        clientSocket.sendto(encryptedMessage, (host, port))