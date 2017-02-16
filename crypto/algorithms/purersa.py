__author__ = 'bsoer'

from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer
import tools.rsatools as RSATools
import math
import sys


class PureRSA(AlgorithmInterface):

    n = None
    totient = None
    e = None
    d = None

    publicKey = None
    privateKey = None

    other_publicKey = None
    other_e = 0
    other_n = 0

    def __init__(self, arguments):

        prime1 = ArgParcer.getValue(arguments, "-p1")
        prime2 = ArgParcer.getValue(arguments, "-p2")

        if prime1 == "" or prime2 == "":
            raise AttributeError("Two Prime Number Parameters -p1 and -p2 are required to use PureRSA Encryption")
        else:
            intPrime1 = int(prime1)
            intPrime2 = int(prime2)

            # calculate all components
            self.n = intPrime1 * intPrime2
            self.totient = (intPrime1 - 1)*(intPrime2-1)

            if intPrime1 > intPrime2:
                self.e = RSATools.findCoPrimeToTotient(self.totient, intPrime1)
            else:
                self.e = RSATools.findCoPrimeToTotient(self.totient, intPrime2)

            self.d = RSATools.findDFromTotientAndE(self.totient, self.e)

            # e and n make our public key
            # were going to arbitrarily format our public key
            # <eLength>:<eValue><nValue>
            strE = str(self.e)
            strELen = len(strE)
            self.publicKey = str(strELen) + ":" + strE + str(self.n)

            # d and n make our private key
            strD = str(self.d)
            strDLen = len(strD)
            self.privateKey = str(strDLen) + ":" + strD + str(self.n)

    def sendFirstMessage(self):
        # return self.publickey.exportKey(format='DER', passphrase=None, pkcs=1)
        # return bytes(self.publickey)
        return self.publicKey.encode()

    def receiveFirstMessage(self, firstMessage):
        self.other_publicKey = firstMessage.decode()
        colonIndex = self.other_publicKey.index(':')

        strELen = self.other_publicKey[0:colonIndex]
        eLen = int(strELen)

        strE = self.other_publicKey[colonIndex+1:colonIndex + 1 + eLen]
        self.other_e = int(strE)

        strN = self.other_publicKey[colonIndex+1+eLen:]
        self.other_n = strN

        print(self.other_n)

        return False  # return true for debug to display public key

    def encryptString(self, unencryptedMessage):
        print(self.other_n)
        plaintext_message_seg_length = int(math.floor(math.log(self.other_n), 2))
        encrypted_message_seg_length = int(math.ceil(math.log(self.other_n, 2)))

        # convert the message to all binary bits
        binaryUnencryptedMessage = ''.join(format(ord(x), 'b') for x in unencryptedMessage)
        # split it up into segments of plaintext_message_seg_length
        unencryptedMessageSegments = list()
        for i in range(0, len(binaryUnencryptedMessage), plaintext_message_seg_length):
            unencryptedMessageSegments.append(binaryUnencryptedMessage[i: i+plaintext_message_seg_length])
        #encrypt each segment using RSA
        encryptedMessageSegments = list()
        for i in unencryptedMessageSegments:
            segmentInt = int(i, 2)  # converts string to int, interpreting it as in base 2
            encryptedSegmentInt = (segmentInt ** self.other_e) % self.other_n

            encryptedSegmentBinary = format(encryptedSegmentInt, '0' + str(encrypted_message_seg_length))
            encryptedMessageSegments.append(encryptedSegmentBinary)

        encryptedMessageBinaryString = ''.join(encryptedMessageSegments)
        encryptedMessageInt = int(encryptedMessageBinaryString, 2)
        return encryptedMessageInt.to_bytes(byteorder=sys.byteorder)

    def decryptString(self, encryptedMessage):

        plaintext_message_seg_length = int(math.floor(math.log(self.n, 2)))
        encrypted_message_seg_length = int(math.ceil(math.log(self.n, 2)))

        # convert the message to all binary bits
        binaryEncryptedMessage = ''.join(format(ord(x), 'b') for x in encryptedMessage)
        # split it up into segments of plaintext_message_seg_length
        encryptedMessageSegments = list()
        for i in range(0, len(binaryEncryptedMessage), encrypted_message_seg_length):
            encryptedMessageSegments.append(binaryEncryptedMessage[i: i + encrypted_message_seg_length])
        # encrypt each segment using RSA
        unencryptedMessage = ""
        for i in encryptedMessageSegments:
            segmentInt = int(i, 2)  # converts string to int, interpreting it as in base 2
            unencryptedSegmentInt = (segmentInt ** self.d) % self.n

            unencryptedMessage += chr(unencryptedSegmentInt)

        return unencryptedMessage