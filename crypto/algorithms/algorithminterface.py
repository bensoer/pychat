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
        raise NotImplementedError()

    @abstractmethod
    def decryptString(self, encryptedMessage):
        raise NotImplementedError()