from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer

class GronsfeldCipher(AlgorithmInterface):

    __key = ""


    def __init__(self, arguments):

        key = ArgParcer.getValue(arguments, "-k")
        if key == "" :
            raise AttributeError("A key value is required for the GronsfeldCipher")
        else:
            self.__key = key

    def encryptString(self, unencryptedMessage):

        encryptedMessage = ""
        for index, letter in enumerate(unencryptedMessage):
            keyIndex = index % len(self.__key)
            offset = int(self.__key[keyIndex])
            encryptedLetter = chr(ord(letter) + offset)
            encryptedMessage += encryptedLetter

        return encryptedMessage.encode()

    def decryptString(self, encryptedMessage):

        plaintextMessage = ""
        encryptedMessage = encryptedMessage.decode()
        for index, letter in enumerate(encryptedMessage):
            keyIndex = index % len(self.__key)
            offset = int(self.__key[keyIndex])
            plaintextLetter = chr(ord(letter) - offset)
            plaintextMessage += plaintextLetter

        return plaintextMessage