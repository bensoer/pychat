from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer

class KamasutraCipher(AlgorithmInterface):

    __key = ""
    __top_alphabet = ""
    __bottom_alphabet = ""


    def __init__(self, arguments):

        key = ArgParcer.getValue(arguments, "-k")
        if key == "" :
            raise AttributeError("A key value is required for the KamasutraCipher. The key must be a randomized alphabet")
        else:
            self.__key = key
            self.__key.upper()

            self.__top_alphabet = self.__key[0:13]
            self.__bottom_alphabet = self.__key[13:]

            print(self.__top_alphabet)
            print(self.__bottom_alphabet)

    def encryptString(self, unencryptedMessage):

        encryptedMessage = ""
        for index, letter in enumerate(unencryptedMessage):
            uppercase_letter = letter.upper()

            tindex = self.__top_alphabet.find(uppercase_letter)
            bindex = self.__bottom_alphabet.find(uppercase_letter)

            if tindex > -1:
                encryptedMessage += self.__bottom_alphabet[tindex]
            elif bindex > -1:
                encryptedMessage += self.__top_alphabet[bindex]
            else:
                encryptedMessage += letter

        return encryptedMessage.encode()

    def decryptString(self, encryptedMessage):

        plaintextMessage = ""
        encryptedMessage = encryptedMessage.decode()
        for index, letter in enumerate(encryptedMessage):

            tindex = self.__top_alphabet.find(letter)
            bindex = self.__bottom_alphabet.find(letter)

            if tindex > -1:
                plaintextMessage += self.__bottom_alphabet[tindex]
            elif bindex > -1:
                plaintextMessage += self.__top_alphabet[bindex]
            else:
                plaintextMessage += letter

        return plaintextMessage