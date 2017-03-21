__author__ = 'bensoer'

from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer

'''
http://www.cryptool-online.org/index.php?option=com_content&view=article&id=56&Itemid=66&lang=en

Note that this implementation is lazier and more error prone as it uses the entire ASCII alphabet but does
not limit it to its ceiling. giving a ceiling would involve incorporating modulus divide during encryption and
addition of values for decryption
'''

class MultiplicativeCipher(AlgorithmInterface):

    __key = ""

    def __init__(self, arguments):

        key = ArgParcer.getValue(arguments, "-k")
        if key == "" or (not key.isdigit()):
            raise AttributeError("A numerical key value is required for the MultiplicativeCipher")
        else:
            self.__key = int(key)

    def encryptString(self, unencryptedMessage):

        encryptedMessage = ""
        for index, letter in enumerate(unencryptedMessage):

            encryptedMessage += chr(ord(letter) * self.__key)

        return encryptedMessage.encode()

    def decryptString(self, encryptedMessage):

        plaintextMessage = ""
        encryptedMessage = encryptedMessage.decode()
        for index, letter in enumerate(encryptedMessage):

            plaintextMessage += chr(int(ord(letter) / self.__key))

        return plaintextMessage