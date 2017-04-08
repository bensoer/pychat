__author__='bensoer'
from crypto.algorithms.algorithminterface import AlgorithmInterface
from crypto.algorithms.rsapublickey import RSAPublicKey
from crypto.algorithms.aescipher import AESCipher
from tools.argparcer import ArgParcer
import random


class RSAAESCipher(AlgorithmInterface):

    aesAlgo = None
    rsaAlgo = None

    receivedRSAKey = False
    RSASendCount = 0
    receivedAESKey = False

    def __init__(self, arguments):

        self.rsaAlgo = RSAPublicKey(arguments)
        self.aesAlgo = AESCipher(arguments)

    def encryptString(self, unencryptedMessage):
        return self.aesAlgo.encryptString(unencryptedMessage)

    def decryptString(self, encryptedMessage):
        return self.aesAlgo.decryptString(encryptedMessage)

    def receiveFirstMessage(self, firstMessage):

        # assume the first thing we get is always the RSA key
        if not self.receivedRSAKey:
            self.logger.debug("RSA Key Has Been Received")
            self.rsaAlgo.receiveFirstMessage(firstMessage)
            self.receivedRSAKey = True

        # now we can expect the AES Key to arrive sometime
        else:

            #print(type(self.rsaAlgo.otherPublicKey.exportKey(passphrase='pychat')))
            #print(type(firstMessage))
            if self.rsaAlgo.otherPublicKey.exportKey(passphrase='pychat') != firstMessage:
                # then this must be the AES key
                self.logger.debug("AES Key Has Been Received")
                self.aesAlgo.key = self.rsaAlgo.key.decrypt(firstMessage)
                self.receivedAESKey = True
            else:
                self.logger.debug("Duplicate RSA Key Was Received")
        return False

    def sendFirstMessage(self):
        if (not self.receivedRSAKey) or self.RSASendCount < 2:
            self.logger.debug("SENDING RSA")
            self.RSASendCount += 1
            return self.rsaAlgo.sendFirstMessage()
        else:
            self.logger.debug("SENDING AES")
            self.receivedAESKey = True
            return self.rsaAlgo.otherPublicKey.encrypt(self.aesAlgo.key, 'pychat')[0]

    def receiveNextMessageThroughFirstMessage(self):
        return not self.receivedAESKey

    def callSendFirstMessageAgain(self):
        return not self.receivedAESKey