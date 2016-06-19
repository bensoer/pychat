__author__ = 'bensoer'
from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer

'''
CaesarCipher is an Algorithm using the CaesarCipher encryption techniques.

Letters are replaced with equivelent letters in the alphabet by a certain offset off. For example A is replaced with D
with an offset of 3. Decryption is simply reversing this process on the recieved string
'''
class CaesarCipher(AlgorithmInterface):

    def __init__(self, arguments):

        # if they pass an o parameter, use this as the offset value
        offset = ArgParcer.getValue(arguments, "-o")
        if offset == "":
            self.offset = 3
        else:
            self.offset = int(offset)

    def encryptString(self, unencryptedMessage):
        '''
        encryptString with the CaesarCipher encrypts the message by finding the orignal value of the character in the
        ascii table and then offsetting the ordinal value by a set ammount. It then converts the offset ordinal value
        back into whatever ascii character represents this new ordinal. This then represents the encrypted letter. Each
        letter has this process applied to them before the completely encryptedMessage is returned
        :param unencryptedMessage: String - the unencrypted message
        :return:Bytes[] - the CaesarCipher encrypted message as bytes
        '''
        encryptedMessage = ""
        for letter in unencryptedMessage:
            encryptedLetter = chr(ord(letter) + self.offset)
            encryptedMessage += encryptedLetter
        return encryptedMessage.encode()

    def decryptString(self, encryptedMessage):
        '''
        decryptString with the CaesarCipher encrypts the message by finding the ordignal value of the character in the
        ascii table and then offsetting the ordinal value by the reverse set ammount as that applied in the encryptString
        method. It then converts the offset ordinal value back into whatever ascii character represents this new ordinal.
        This then represents the decrypted letter. Each letter has this process applied to them before the completely
        encryptedMessage is returned
        :param encryptedMessage: Bytes[] - the encrypted message as a byte array
        :return:String - the CaesarCipher unencrypted message
        '''
        encryptedMessage = encryptedMessage.decode()
        decryptedMessage = ""
        for letter in encryptedMessage:
            decryptedLetter = chr(ord(letter) - self.offset)
            decryptedMessage += decryptedLetter
        return decryptedMessage

