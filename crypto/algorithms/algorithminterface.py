from abc import ABCMeta, abstractmethod
import logging
__author__ = 'bensoer'

'''
This will mimmick an interface using python's Abstract Base Class module
https://dbader.org/blog/abstract-base-classes-in-python
'''

'''
AlgorithmInterface is the basic interface that defines all requirements needed to be implemented by a crypto
algorithm running on the PyChat program. Although not largely enforcable, all encryption algorithms must inherit
from this abstract class to ensure appropriate methods needed are implemented. Failing to do so may cause failure
in the ability to find the module
'''
class AlgorithmInterface(metaclass=ABCMeta):

    logger = logging.getLogger("pychat")

    @abstractmethod
    def encryptString(self, unencryptedMessage):
        '''
        encryptString is in charge of encrypting the passed in unencryptedMessage and applying whatever encryption
        algorithm that the abstract class is implementing
        :param unencryptedMessage: String - the message before it is encrypted
        :return: Bytes - the encrypted message, the result of applying the encryption process to the unencryptedMessage
        variable and converting it to Bytes
        '''
        raise NotImplementedError()

    @abstractmethod
    def decryptString(self, encryptedMessage):
        '''
        decryptString is in charge of decrypting the passed in encryptedMessage and applying whatever decryption
        algorithm that the class is implementing
        :param encryptedMessage: Bytes  - the encrypted message needing to be decrypted
        :return: String - the decrypted message, the result of applying the decryption process to the encryptedMessage
        variable and converting it to a String
        '''
        raise NotImplementedError()

    def sendFirstMessage(self):
        '''
        This method sends the first message over to the receiving system. pychat does not care if this message is
        encrypted or not, only that bytes of the message to be sent are returned if there is a message to be sent
        :return: Bytes - if returned bytes length is > 0, then it will be sent as is over the connection
        '''

        self.logger.debug("No Implementation Provided For Sending First Message. Default Functionality Assumed")
        return ""

    def receiveFirstMessage(self, firstMessage):
        '''
        receiveFirstMessage is called upon pychat recieving the first message from the listenerprocess.
        :param: firstMessage: Bytes - the first message in bytes - this may be encrypted - depending on procedure used
        by sending system when sendFirstMessage is executed on that system
        :return: Boolean - status as to whether to print the firstMessage to console after calling this method.
        Default returns True = first message will be written to console assuming it is a regular message. Return True
        will be run through the decyption algorithm
        '''

        self.logger.debug("No Implementation Provided For Receving The First Message. " +
                          "First Message Is Assumed Actual Data")
        return True

    def receiveNextMessageThroughFirstMessage(self):
        '''
        sendNextMessageThroughFirstMessage is a general override for controlling at what point to stop sending messages
        to the receiveFirstMessage method. The receiveFirstMessage functionality is the exact same as stated in its method
        but by overriding this method, the algorithm can force future methods to continue being send and evaluated
        through the receiveFirstMessage until sendNextMessageThroughFirstMessage returns false. This is useful for
        designing algorithms which require multiple data transfers before executing their encryption and decryption
        methods
        :return: Boolean - whether or not to send the next received message through receiveFirstMessage. Default value
        is false. True means the next message received will be passed to receiveFirstMessage and evaluated there
        before potentially passed to the decryption algorithm. receiveNextMessageThroughFirstMessage is always called
        first before receiveFirstMessage is called BUT only AFTER the initial first message has been received.

        NOTES:
         - By setting this value to true, pychat will no longer filter duplicate received FirstMessages. During normal
         initialization the first terminal to launch receives the first message twice. The pychat framework keeps track
         of this and does not send the duplicate to the loaded algorithm. By setting
         receiveNextMessageThroughFirstMessage to true, pychat will send all received messages to the algorithm,
         regardless of duplication.
        '''
        return False

    def callSendFirstMessageAgain(self):
        '''
        callSendFirstMessageAgain allows the algorithm to dictate how many times the sendFirstMessage method will be called.
        Under normal use, sendFirstMessage gets calls twice - once at initialization, and once again after receiveFirstMessage.
        If the algorithm though needs to send additional initialization information before the encrypt and decrypt methods
        are called. Returning true to callSendFirstMessageAgain will allow this functionality to occur.
        :return: Boolean - whether or not to call sendFirstMessage. This method is called ONLY after the first 2 typical
        startup calls are made. After these first 2, it is then called BEFORE EVERY TIME sendFirstMessage is called.
        callSendFirstMessage will be triggered whenever an incoming message arrives after the first 2 typical startup
        calls are made. Order is as follows to a received message:
            1) - message received -
            2) IF receiveNextMessageThroughFirstMessage() == TRUE: receiveFirstMessage() ELSE: decryptString()
            3) IF callSendFirstMessageAgain == TRUE: sendFirstMessage()
        '''
        return False

    @abstractmethod
    def __init__(self, arguments):
        '''
        for these algorithms to function, key parameters may need to be passed to the class in order for encryption and
        decryption to be successful. Whatever class implementing the AglorithmInterface will need to have a constructor
        that takes an arguments parameter. The arguments parameter is a copy of the arguments passed to the program upon
        initialization
        :param arguments: Array - The system initializations array containing argument passed and program start
        :return: void
        '''
        raise NotImplementedError()