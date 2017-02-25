from abc import ABCMeta, abstractmethod
import logging


'''
HashInterface is the basic interface used by the framework to access hashing algorithms to be used on a given message
'''
class HashInterface(metaclass=ABCMeta):

    logger = logging.getLogger('pychat')

    @abstractmethod
    def hashString(self, stringMessage):
        '''
        hashString is the main method used in the HashInterface to generate the hash value for the given string. The
        passed in string has a hash generated from it, which is then returned
        :param stringMessage: the string plaintext that will have a hash generated from it
        :return: Bytes - The hash as a Byte Array of the plaintext string passed in
        '''
        raise NotImplementedError

