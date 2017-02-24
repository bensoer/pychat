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
        will be run through the descyption aglorithm
        '''

        self.logger.debug("No Implementation Provided For Receving The First Message. " +
                          "First Message Is Assumed Actual Data")
        return True

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