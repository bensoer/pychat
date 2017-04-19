__author__ = 'bensoer'

from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer
import math

class RailFenceCipher(AlgorithmInterface):

    __rails = -1


    def __init__(self, arguments):

        key = ArgParcer.getValue(arguments, "-k")
        if key != "":
            self.__rails = int(key)

        # otherwise no key means dynamic rails:  rails = (messageLength/2)-1
        # at minimum there must be 1/2 - 1 rails so as to ensure some letters are scrambled
        # note this comes an issue if the message only has 2 letters in it :s - just send it plain in that case

    def initializeRails(self, unencryptedMessage):
        railList = list()

        if self.__rails == -1:
            # dynamic rails
            railCount = int((len(unencryptedMessage) / 2) - 1)
            self.logger.debug("Dynamic Rails Selected. RailCount: " + str(railCount))
            for i in range(0, railCount):
                railList.append(list())
        else:
            # set rails
            for i in range(0, self.__rails):
                railList.append(list())

        return railList


    def encryptString(self, unencryptedMessage):
        railList = self.initializeRails(unencryptedMessage)
        if len(railList) == 0:
            return unencryptedMessage.encode()
        else:

            # scamble letters into their rails
            for index, letter in enumerate(unencryptedMessage):
                railList[index % len(railList)].append(letter)
            self.logger.debug("Rails: " + str(railList))

            encryptedMessage = ""
            for rail in railList:
                for letter in rail:
                    encryptedMessage += letter

            return encryptedMessage.encode()

    def decryptString(self, encryptedMessage):
        encryptedMessageText = encryptedMessage.decode()

        railList = self.initializeRails(encryptedMessageText)
        if len(railList) == 0:
            return encryptedMessageText
        else:

            # determine needed box size
            messageLength = len(encryptedMessageText)
            rowLength = math.ceil(messageLength / len(railList))
            extraLetters = (messageLength % len(railList))
            extraSpaces = len(railList) - extraLetters
            self.logger.debug("Message Length: " + str(messageLength) + " Row Length: " + str(rowLength) + " Extra Spaces: " + str(extraSpaces))

            letterIndex = 0
            for index, rail in enumerate(railList):
                for i in range(0, rowLength):
                    if extraLetters > 0 and index >= extraLetters and i >= rowLength - 1:
                        self.logger.debug("Break Point Hit")
                        break

                    rail.append(encryptedMessageText[letterIndex])
                    letterIndex += 1
                    self.logger.debug(railList)


            self.logger.debug("RECREATED RAILS: " + str(railList))
            unencryptedMessage = ""
            for i in range(0, len(encryptedMessageText)):
                unencryptedMessage += railList[i % len(railList)].pop(0)

            return unencryptedMessage