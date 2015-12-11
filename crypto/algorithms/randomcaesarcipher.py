__author__ = 'bensoer'

from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer
import random


class RandomCaesarCipher(AlgorithmInterface):

    __alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    __scrambledAlphabet = ""
    __seed = 5
    __offset = 3

    def __init__(self, arguments):
        seed = ArgParcer.getValue(arguments, "-s")
        offset = ArgParcer.getValue(arguments, "-o")

        'set the seet value if it was passed in'
        if(seed != ""):
            self.__seed = int(seed)

        'set the offset value if it was passed in'
        if(offset != ""):
            self.__offset = int(offset)

        'now generate our scrambled alphabet'
        self.__generateScrambledAlphabet()

    def __generateScrambledAlphabet(self):
        random.seed(self.__seed)

        i = 0
        while i < len(self.__alphabet):
            index = random.randrange(0, len(self.__alphabet))
            letterToBeAdded = self.__alphabet[index];
            if self.__letterIsAlreadyScrambled(letterToBeAdded) == False:
                self.__scrambledAlphabet += letterToBeAdded
                i = i + 1

        print("Scrambled Alphabet Generated: " + self.__scrambledAlphabet)

    def __letterIsAlreadyScrambled(self, letter):
        for scrambledLetter in self.__scrambledAlphabet:
            if scrambledLetter == letter:
                return True

        return False

    def __getIndexOfLetter(self, letter, alphabet):
        for index, alphabetLetter in enumerate(alphabet):
            if alphabetLetter == letter:
                return index


    def encryptString(self, unencryptedMessage):
        encryptedMessage = ""
        for letter in unencryptedMessage:

            'check if this is the colon or space'
            if letter == ":" or letter == " ":
                encryptedMessage += letter
                continue

            'anything else we encrypt with the random letters'
            index = self.__getIndexOfLetter(letter, self.__alphabet)

            'apply the offset'
            offsetIndex = index + self.__offset
            'correct the index in case it overflows. Do wrap around'
            correctedIndex = offsetIndex % (len(self.__alphabet))

            encryptedLetter = self.__scrambledAlphabet[correctedIndex]
            encryptedMessage += encryptedLetter
        return encryptedMessage

    def decryptString(self, encryptedMessage):
        decryptedMessage = ""
        for letter in encryptedMessage:

            'check if this is the colon or space'
            if letter == ":" or letter == " ":
                decryptedMessage += letter
                continue

            index = self.__getIndexOfLetter(letter, self.__scrambledAlphabet)

            'apply offset'
            offsetIndex = index - self.__offset
            'correct the index in case we go over'
            correctedIndex = 0
            if offsetIndex < 0:
                offsetIndex = offsetIndex * -1
                correctedIndex = (len(self.__alphabet)) - offsetIndex
            else:
                correctedIndex = offsetIndex

            decryptedLetter = self.__alphabet[correctedIndex]
            decryptedMessage += decryptedLetter

        return decryptedMessage

