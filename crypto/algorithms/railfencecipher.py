__author__ = 'bensoer'

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

    def initializeRails(self, unencryptedMessage):
        railList = list()

        if self.__rails == -1:
            # dynamic rails
            railCount = int((len(unencryptedMessage) / 2) - 1)
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
            increment = True
            railIndex = 0
            for index, letter in enumerate(unencryptedMessage):
                railList[railIndex].append(letter)

                if increment:
                    railIndex += 1
                    if railIndex >= len(railList)-1:
                        increment = False
                else:
                    railIndex -= 1
                    if railIndex <= 0:
                        increment = True

            print(railList)


            # read out the message rail by rail
            encryptedMessage = ""
            for rail in railList:
                for letter in rail:
                    encryptedMessage += letter

        return encryptedMessage.encode()

    def decryptString(self, encryptedMessage):
        encryptedMessageText = encryptedMessage.decode()
        # print(encryptedMessageText)

        railList = self.initializeRails(encryptedMessageText)
        if len(railList) == 0:
            return encryptedMessageText
        else:

            # place letters back into their rails

            increment = True
            railIndex = 0 # resolves to the rail which the letter will be placed in
            letterIndex = 0 # resolves to the letter in the encryptedMessageText we are trying to find its home to
            for lap in range(0, len(railList)):
                # lap resolves to the rail we are currently finding letters that belong to it
                railIndex = lap

                for travelIndex in range(lap, len(encryptedMessageText)):
                    # travelIndex resolves to which letter through the rails we are on - it mostly has no use
                    # but ensures that the railIndex does not keep going past as many letters as there are in the
                    # message

                    if lap == railIndex:

                        '''print(lap)
                        print(railIndex)
                        print(len(encryptedMessageText))
                        print(letterIndex)
                        print(travelIndex)
                        print(railList)'''
                        railList[lap].append(encryptedMessageText[letterIndex])
                        '''print("MATCH MADE. ASSIGNING LETTER: " + str(
                            encryptedMessageText[letterIndex]) + " TO LAP: " + str(lap))'''
                        letterIndex += 1

                        if letterIndex >= len(encryptedMessageText):
                            break


                    if increment:
                        railIndex += 1
                        if railIndex >= len(railList) - 1:
                            increment = False
                    else:
                        railIndex -= 1
                        if railIndex <= 0:
                            increment = True

            print(railList)


            # run through rails to reassemble
            unencryptedMessage = ""
            increment = True
            railIndex = 0
            for letterCount in range(0, len(encryptedMessageText)):
                unencryptedMessage += railList[railIndex].pop(0)

                if increment:
                    railIndex += 1
                    if railIndex >= len(railList) - 1:
                        increment = False
                else:
                    railIndex -= 1
                    if railIndex <= 0:
                        increment = True

        return unencryptedMessage