__author__ = 'bensoer'
from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer

'''
CaesarCipher is an Algorithm using the CaesarCipher encryption techniques.

Letters are replaced with equivelent letters in the alphabet by a certain offset off. For example A is replaced with D
with an offset of 3. Decryption is simply reversing this process on the recieved string
'''
class PureDESCipher(AlgorithmInterface):

    def __init__(self, arguments):

        # if they pass an o parameter, use this as the offset value
        offset = ArgParcer.getValue(arguments, "-o")
        if offset == "":
            self.offset = 3
        else:
            self.offset = int(offset)

    def encryptString(self, unencryptedMessage):

        encryptedMessage = ""
        for letter in unencryptedMessage:
            encryptedLetter = chr(ord(letter) + self.offset)
            encryptedMessage += encryptedLetter
        return encryptedMessage.encode()

    def decryptString(self, encryptedMessage):

        encryptedMessage = encryptedMessage.decode()
        decryptedMessage = ""
        for letter in encryptedMessage:
            decryptedLetter = chr(ord(letter) - self.offset)
            decryptedMessage += decryptedLetter
        return decryptedMessage

