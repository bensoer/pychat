from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer

class RailFenceCipher(AlgorithmInterface):

    __rails = -1


    def __init__(self, arguments):

        key = ArgParcer.getValue(arguments, "-k")
        if key != "":
            self.__rails = int(key)

        # otherwise no key means dynamic rails:  rails = (messageLength/2)-1
        # at minimum there must be 1/2 - 1 rails so as to ensure some letters are scrambled
        # note this comes an issue if the message only has 2 letters in it :s - just send it plain in that case

    def encryptString(self, unencryptedMessage):

        # TODO

        return unencryptedMessage.encode()

    def decryptString(self, encryptedMessage):

        #TODO

        return encryptedMessage.decode()