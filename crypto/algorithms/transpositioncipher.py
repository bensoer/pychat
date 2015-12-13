__author__ = 'bensoer'

from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer
from collections import deque
import sys
import string

class TranspositionCipher(AlgorithmInterface):

    __key = ""

    '''
    __mapper stores the dynamic mapping of letters and values for encryption and decryption
    Index Information:
    [0] A Character list of the key
    [1] An Integer list giving the alphabetical order index of the key. Note this list is ordered in order of
        appearance in the character array so although the numbers are alphabetical order, they themselves may not
        be in order
    [2+] Messages being encoded or decoded. Depending on length and the length of the key this may spant several
        rows
    '''
    __mapper = None



    def __init__(self, arguments):
        key = ArgParcer.getValue(arguments, "-k");
        if key == "":
            raise AttributeError("Key Is Required Parameter For Transposition Cipher");
        else:
            self.__key = key

        # add the key as a list
        self.__mapper = list()
        self.__mapper.append(list(self.__key))

        positionsList = self.__createAlphabeticalIndexListOfKey(self.__key)

        print(positionsList)
        self.__mapper.append(positionsList)

        print(self.__mapper)

    def __createAlphabeticalIndexListOfKey(self, key):

        alphabet = "abcdefghijklmnopqrstuvwxyz"

        positions = [None] * len(key)

        letterValue = 1
        for letter in alphabet:
            for kIndex, kLetter in enumerate(key):
                #print(letter + " vs " + kLetter.lower())
                if letter == kLetter.lower():
                    #print("Found Match: " + letter + " is given position: " + str(letterValue))
                    positions[kIndex] = letterValue
                    letterValue = letterValue + 1

        return positions

    def __buildMapperWithMessage(self, message):

        keyLength = len(self.__key)

        messageIndex = 0
        while (messageIndex * keyLength) < len(message):
            segment = list()

            for i in range(keyLength):
                if (i + (messageIndex * keyLength)) >= len(message):
                    segment.append("*")
                else:
                    segment.append(message[i + (messageIndex * keyLength)])

            self.__mapper.append(segment)
            messageIndex = messageIndex + 1


    def __clearMapper(self):

        for i in range(2, len(self.__mapper)):
            self.__mapper.pop(2)

    def __getLettersUnderAlphabetIndex(self,index):
        numOfRows = len(self.__mapper)
        for position, alphaIndex in enumerate(self.__mapper[1]):
            if alphaIndex == index:

                letters = list()
                for i in range(2, numOfRows):
                    letters.append(self.__mapper[i][position])
                return letters


    def encryptString(self, unencryptedMessage):

        self.__buildMapperWithMessage(unencryptedMessage)

        keyLength = len(self.__key)
        encryptedMessage = ""

        for i in range(1, keyLength+1):
            listOfLetters = self.__getLettersUnderAlphabetIndex(i)
            encryptedMessage = encryptedMessage.join(listOfLetters)

        self.__clearMapper()
        return encryptedMessage

    def __buildMapperWithEncryptedMessage(self, encryptedMessage):
        pass


    def decryptString(selfs, encryptedMessage):
        return encryptedMessage



