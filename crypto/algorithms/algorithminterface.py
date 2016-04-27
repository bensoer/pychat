from abc import ABCMeta, abstractmethod
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

    @abstractmethod
    def encryptString(self, unencryptedMessage):
        '''
        encryptString is in charge of encrypting the passed in unencryptedMessage and applying whatever encryption
        algorithm that the abstract class is implementing
        :param unencryptedMessage: String - the message before it is encrypted
        :return: String - the encrypted message, the result of applying the encryption process to the unencryptedMessage
        variable
        '''
        raise NotImplementedError()

    @abstractmethod
    def decryptString(self, encryptedMessage):
        '''
        decryptString is in charge of decrypting the passed in encryptedMessage and applying whatever decryption
        algorithm that the class is implementing
        :param encryptedMessage: String - the encrypted message needing to be decrypted
        :return: String - the decrypted message, the result of applying the decryption process to the encryptedMessage
        variable
        '''
        raise NotImplementedError()

    def sendFirstMessage(self):
        '''

        :return: String - if returned value is not "", then it will be sent as is over the connection
        '''

        return ""

    def receiveFirstMessage(self, firstMessage):
        '''
        receiveFirstMessage is called upon pychat recieving the first message from the listenerprocess.
        :return: Boolean - status as to whether to print the firstMessage to console after calling this method.
        Default returns True = first message will be written to console assuming it is a regular message. Return True
        will be run through the descyption aglorithm
        '''

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