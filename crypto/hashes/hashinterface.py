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

    @abstractmethod
    def getDigestSize(self):
        '''
        getDigestSize is a helper function used in the parsing process for seperating the hash from the encrypted message.
        The passed in stringMessage is the same message passed into the hashString method and can be used to manually
        generate the hash and then count the number of bytes in the resulting hash. This can be used for dynamic digest
        sizes. For static sizes, a simple value can be returned.
        :return: Int - The number of bytes in the resulted hash
        '''
        raise NotImplementedError

    @abstractmethod
    def isValidHash(self, stringMessage, hashBytes):
        '''
        isValidHash is a verification method that determines whether the passed in message will generate the passed in
        hashBytes
        :param stringMessage: the string message being verified whether it equals the hash
        :param hashBytes: the hash as bytes that the stringMessage is being verified to match
        :return: Boolean - the state of whether the stringMessage generates the passed in hashBytes. True means they
        match
        '''
        raise NotImplementedError