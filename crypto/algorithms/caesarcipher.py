__author__ = 'bensoer'

from .algorithminterface import AlgorithmInterface

class CaesarCipher(AlgorithmInterface):

    def __init__(self):
        self.offset = 3

    def encryptString(self, unencryptedMessage):
        encryptedMessage = ""
        for letter in unencryptedMessage:
            encryptedLetter = chr(ord(letter) + self.offset)
            encryptedMessage += encryptedLetter
        return encryptedMessage

    def decryptString(self, encryptedMessage):
        decryptedMessage = ""
        for letter in encryptedMessage:
            decryptedLetter = chr(ord(letter) - self.offset)
            decryptedMessage += decryptedLetter
        return decryptedMessage

