from abc import ABCMeta, abstractmethod
__author__ = 'bensoer'

'''
This will mimmick an interface using python's Abstract Base Class module
https://dbader.org/blog/abstract-base-classes-in-python
'''

class AlgorithmInterface(metaclass=ABCMeta):

    @abstractmethod
    def encryptString(self, unencryptedMessage):
        raise NotImplementedError()

    @abstractmethod
    def decryptString(self, encryptedMessage):
        raise NotImplementedError()