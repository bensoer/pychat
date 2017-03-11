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
        key = ArgParcer.getValue(arguments, "-k")
        if key == "":
            raise AttributeError("Key Is Required Parameter For Transposition Cipher")
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
        encryptedMessage = encryptedMessage.replace('*', '')
        #print(encryptedMessage)

        self.__clearMapper()
        return encryptedMessage.encode()


    def __insertLettersAtAlphabetIndex(self, index, letters):

        lettersList = list(letters)

        for pos, alphaIndex in enumerate(self.__mapper[1]):
            if alphaIndex == index:

                for position, letter in enumerate(lettersList):
                    self.__mapper[2+position][pos] = letter

                break



    def __fillEndSpaces(self, numberOfSpaces):

        endRow = len(self.__mapper) - 1
        rowlen = len(self.__mapper[endRow])

        for i in range(0, numberOfSpaces):
            #print("Inserting star into index: " + str(endRow) + str((rowlen-1)-i))
            self.__mapper[endRow][(rowlen - 1) - i] = '*'

    def __getSegmentForColumn(self, message, mappos, msgStartIndex):

        mappos = mappos + 1
        letters = self.__getLettersUnderAlphabetIndex(int(mappos))

        numOfStars = 0
        if letters is not None:
            numOfStars = letters.count('*')

        endpos = msgStartIndex + len(letters) - numOfStars
        segment = message[msgStartIndex:endpos]
        return segment


    def decryptString(self, encryptedMessage):
        strEncryptedMessage = encryptedMessage.decode()

        keyLength = len(self.__key)
        messageLength = len(strEncryptedMessage)

        #figure out how many stars need to be added to the message
        stars = messageLength - keyLength
        if stars <= 0:
            # means the message is smaller then the key
            stars = abs(stars)
        else:
            # means the message is larger then the key
            largeEnoughKey = keyLength

            #so largen our key in increments of our key length to find something large enough
            while messageLength > largeEnoughKey:
                largeEnoughKey = largeEnoughKey + keyLength

            stars = messageLength - largeEnoughKey
            stars = abs(stars)

        # if there is more then 0 stars needed, add them as part of the message length
        totalMessageLength = messageLength
        if stars > 0:
            totalMessageLength = messageLength + stars

        #print(totalMessageLength)

        # now determine how many rows will be needed to store this entire message
        rows = int(totalMessageLength) / int(keyLength)
        extra = int(totalMessageLength) % int(keyLength)

        # if there is extra letters to be included add a row for it
        if extra > 0:
            #print("There is extra: " + str(extra))
            rows = rows + 1

        # create the appropriate number of rows needed on the mapper to hold the message
        for row in range(0, int(rows)):
            newRow = [None] * keyLength
            self.__mapper.append(newRow)

        # fill extra spaces at the end with stars
        self.__fillEndSpaces(stars)

        #print(self.__mapper)

        # insert the message into the mapper
        msgpos = 0
        mappos = 0
        while msgpos < messageLength:
            segment = self.__getSegmentForColumn(strEncryptedMessage, mappos, msgpos)
            #print(segment)

            # put this letter segment in the column of the alphabet index
            self.__insertLettersAtAlphabetIndex(mappos + 1, segment)

            mappos = mappos + 1
            msgpos = msgpos + len(segment)

        #print(self.__mapper)

        # reconstruct from the message from each row in the mapper
        fullLists = list()
        for i in range(2, len(self.__mapper)):
            #print("loop " + str(i))
            mapRow = self.__mapper[i]
            #print(mapRow)
            fullLists = fullLists + mapRow


        fullSegment = ''.join(fullLists)
        fullSegment = fullSegment.replace('*', '')

        # cleanup the mapper for next message
        self.__clearMapper()

        return fullSegment
