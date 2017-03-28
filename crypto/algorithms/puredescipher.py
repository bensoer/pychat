__author__ = 'bensoer'
from crypto.algorithms.algorithminterface import AlgorithmInterface
from tools.argparcer import ArgParcer
from Crypto.Hash import SHA256
import tools.destools as destools
import math
import sys

class PureDESCipher(AlgorithmInterface):

    key = None
    subkeys = []

    def __init__(self, arguments):

        # if they pass an o parameter, use this as the offset value
        key = ArgParcer.getValue(arguments, "-k")
        if key == "":
            raise AttributeError("Key Is Required For DES")
        else:
            hasher = SHA256.new()
            hasher.update(bytes(key, 'utf-8'))
            hash = hasher.hexdigest()
            binaryKey = ''.join(format(int(x, 16), '04b') for x in hash[:16])
            self.key = binaryKey

            self.generateSubKeys()
            print(self.subkeys)
            print(len(self.subkeys))

    def generateSubKeys(self):

        keyList = list(self.key)
        ckey = ""
        dkey = ""

        # run through pc-1 + split
        for i in range(0, len(destools.KEYGEN.pc1[0])):
            replacebit = (destools.KEYGEN.pc1[0][i] - 1)
            ckey = ckey + keyList[replacebit]

        for i in range(0, len(destools.KEYGEN.pc1[1])):
            replacebit = (destools.KEYGEN.pc1[1][i] - 1)
            dkey = dkey + keyList[replacebit]

        #  for loop
        for i in range(0, 16):
            # c0 left shift
            clist = list(ckey)
            for j in range(0, destools.KEYGEN.leftshift[i]):
                first = clist.pop(0)
                clist.append(first)

            # d0 left shift
            dlist = list(dkey)
            for j in range(0, destools.KEYGEN.leftshift[i]):
                first = dlist.pop(0)
                dlist.append(first)

            # append
            ckey = ''.join(clist)
            dkey = ''.join(dlist)

            joinedKey = ckey + dkey
            joinedKeyList = list(joinedKey)

            subkey = ""
            # run through pc-2
            for k in range(0, len(destools.KEYGEN.pc2)):
                replacebit = (destools.KEYGEN.pc2[k] - 1)
                subkey = subkey + joinedKeyList[replacebit]

            # save key
            self.subkeys.append(subkey)

    def encryptString(self, unencryptedMessage):

        #convert message to binary
        binaryUnencryptedMessage = ''.join(format(ord(x), '08b') for x in unencryptedMessage)

        #pad message to fit inside 64 bit blocks
        while len(binaryUnencryptedMessage) % 64 != 0:
            binaryUnencryptedMessage = '0' + binaryUnencryptedMessage

        #split into blocks
        unencryptedMessageSegments = list()
        for i in range(0, len(binaryUnencryptedMessage), 64):
            unencryptedMessageSegments.append(binaryUnencryptedMessage[i: i + 64])

        totalMessage = bytearray()

        for index, segment in enumerate(unencryptedMessageSegments):

            #ip
            segmentList = list(segment)
            postip = ""
            for i in range(0, len(destools.IPTABLE.initialPermutation)):
                replacebit = (destools.IPTABLE.initialPermutation[i] - 1)
                postip = postip + segmentList[replacebit]

            #left right split
            postipList = list(postip)
            left = "".join(postipList[:32])
            right = "".join(postipList[32:])

            #for 15 cycles
            for i in range(0, 15):

                # calculate F
                f = self.calculateF(right, self.subkeys[i])

                # XOR left with F
                xorResult = int(f, 2) ^ int(left, 2)
                binaryString = bin(xorResult)[2:]
                while len(binaryString) % 32 != 0:
                    binaryString = '0' + binaryString

                # swap
                left = right
                right = binaryString

            # -- last cycle

            # calculate F
            f = self.calculateF(right, self.subkeys[15]) # the 16th and last subkey

            # XOR left with F
            xorResult = int(f, 2) ^ int(left, 2)
            binaryString = bin(xorResult)[2:]
            while len(binaryString) % 32 != 0:
                binaryString = '0' + binaryString

            # Left is left right is right
            # append together
            fullResult = binaryString + right

            # inverse IP
            result = ""
            for i in range(0, len(destools.IPTABLE.finalPermutation)):
                replacebit = (destools.IPTABLE.finalPermutation[i] - 1)
                result = result + fullResult[replacebit]

            # output made
            # - convert to bytearray
            # - append to total message

            byteArrayResult = int(result, 2).to_bytes(byteorder=sys.byteorder, length=math.ceil(len(result) / 8))
            totalMessage.append(byteArrayResult)

        return totalMessage

    def calculateF(self, right, key):
        '''
        :param right: 32-bit binary string of the in process of encryption message
        :param key: the subkey for the cycle
        :return: binary string of the calculated result
        '''

        # take right side and run through E table
        rightList = list(right)
        fourtyeight = ""
        for i in range(0, len(destools.FTABLES.etable)):
            replacebit = (destools.FTABLES.etable[i] - 1)
            fourtyeight = fourtyeight + rightList[replacebit]

        # xor results with the key
        xorResult = int(fourtyeight, 2) ^ int(key, 2)
        binaryString = bin(xorResult)[2:]
        while len(binaryString) % 48 != 0:
            binaryString = '0' + binaryString

        # prepare for s-table processing
        binaryStringSegments = list()
        for i in range(0, len(binaryStringSegments), 6):
            binaryStringSegments.append(binaryStringSegments[i: i + 6])

        preP = ""
        # run through s-tables
        for index, segment in enumerate(binaryStringSegments):
            stable = destools.STABLES.tables[index]

            ybin = segment[0] + segment[6]
            y = int(ybin, 2)

            xbin = segment[1:5]
            x = int(xbin, 2)

            replaceSegment = stable[x][y]
            binReplaceSegment = bin(replaceSegment)[2:]
            while len(binReplaceSegment) % 4 != 0:
                binReplaceSegment = '0' + binReplaceSegment

            preP += binReplaceSegment

        # run the final result through the p-table
        prePList = list(preP)
        postP = ""
        for i in range(0, len(destools.FTABLES.ptable)):
            replacebit = (destools.FTABLES.ptable[i] - 1)
            postP += prePList[replacebit]

        return postP



    def decryptString(self, encryptedMessage):

        encryptedMessage = encryptedMessage.decode()
        decryptedMessage = ""
        for letter in encryptedMessage:
            decryptedLetter = chr(ord(letter) - self.offset)
            decryptedMessage += decryptedLetter
        return decryptedMessage

