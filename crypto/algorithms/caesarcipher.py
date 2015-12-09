__author__ = 'bensoer'

from .algorithminterface import AlgorithmInterface

'''
CaesarCipher is an Algorithm using the CaesarCipher encryption techniques.

Letters are replaced with equivelent letters in the alphabet by a certain offset off. For example A is replaced with D
with an offset of 3. Decryption is simply reversing this process on the recieved string
'''
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

