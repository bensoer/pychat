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

        #print(positionsList)
        self.__mapper.append(positionsList)

        #print(self.__mapper)

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
        messageLength = len(message)
        rows = messageLength / keyLength
        extra = messageLength % keyLength

        #print("key length: " + str(keyLength))
        #print("message length: " + str(messageLength))
        #print("rows needed: " + str(rows))
        #print("extra bits: " + str(extra))

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

        #print(self.__mapper)
        #print("mooving on")

        keyLength = len(self.__key)
        joinedLists = list()
        encryptedMessage = ""

        for i in range(1, keyLength+1):
            listOfLetters = self.__getLettersUnderAlphabetIndex(i)
            #print("index: " + str(i) + " has letters: ")
            #print(listOfLetters)
            joinedLists = joinedLists + listOfLetters

        #print(joinedLists)
        encryptedMessage = ''.join(joinedLists)
        #print(encryptedMessage)

        self.__clearMapper()
        return encryptedMessage.encode()


    def __insertLettersAtAlphabetIndex(self, index, letters):

        lettersList = list(letters)
        #print(lettersList)
        for position, letter in enumerate(lettersList):
            self.__mapper[2+position][index] = letter


    def decryptString(self, encryptedMessage):
        strEncryptedMessage = encryptedMessage.decode();

        #print(self.__mapper)

        keyLength = len(self.__key)
        messageLength = len(strEncryptedMessage)
        rows = int(messageLength) / int(keyLength)
        extra = messageLength % keyLength

        if extra > 0:
            rows = rows + 1

        for row in range(0, int(rows)):
            newRow = [None] * keyLength

            self.__mapper.append(newRow)

        #print(self.__mapper)

        for i in range(0, messageLength, int(rows)):
            segment = strEncryptedMessage[i:(i+int(rows))]

            index = (i / int(rows)) + 1

            for pos, value in enumerate(self.__mapper[1]):
                if index == value:
                    #print("inserting segment: >" + str(segment) + "< into index: " + str(int(pos)))
                    self.__insertLettersAtAlphabetIndex(int(pos), segment)



        #print(self.__mapper)

        fullLists = list()
        for i in range(2, len(self.__mapper)):
            #print("loop " + str(i))
            mapRow = self.__mapper[i]
            #print(mapRow)
            fullLists = fullLists + mapRow

        #print(fullLists)

        fullSegment = ''.join(fullLists)
        fullSegment = fullSegment.replace('*', '')

        self.__clearMapper()
        return fullSegment



