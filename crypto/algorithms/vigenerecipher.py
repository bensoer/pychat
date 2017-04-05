__author__='bensoer'
from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer

class VigenereCipher(AlgorithmInterface):

    __key = ""


    def __init__(self, arguments):

        key = ArgParcer.getValue(arguments, "-k")
        if key == "":
            raise AttributeError("Key Is Required Parameter For Vigenere Cipher")
        else:
            self.__key = key
            self.__key.upper()

    def encryptString(self, unencryptedMessage):

        encryptedMessage = ""
        for index, letter in enumerate(unencryptedMessage):
            keyIndex = index % len(self.__key)
            keyLetter = self.__key[keyIndex]
            offset = abs(ord(keyLetter) - ord('A'))
            encryptedLetter = chr(ord(letter) + offset)
            encryptedMessage += encryptedLetter

        return encryptedMessage.encode()

    def decryptString(self, encryptedMessage):

        plaintextMessage = ""
        encryptedMessage = encryptedMessage.decode()
        for index, letter in enumerate(encryptedMessage):
            keyIndex = index % len(self.__key)
            keyLetter = self.__key[keyIndex]
            offset = abs(ord(keyLetter) - ord('A'))
            plaintextLetter = chr(ord(letter) - offset)
            plaintextMessage += plaintextLetter

        return plaintextMessage