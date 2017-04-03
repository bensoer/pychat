__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import MD5 as libmd5
import math
import sys

# https://www.ietf.org/rfc/rfc1321.txt
# https://en.wikipedia.org/wiki/MD5 - example implementation




class PureMD5(HashInterface):


    shiftRounds = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    k = []



    def __init__(self):
        # generate k table
        for i in range(0, 63):
            self.k[i] = math.floor(((2 ** 32) * abs(math.sin(i + 1))))

    def leftrotate(self, x, c):
        return (x << c) | (x >> (32-c))

    def pad(self, bitStringMessage):

        originalBitStringMessage = bitStringMessage
        extraAppendLength = len(originalBitStringMessage) % (2**64)
        extraAppendStringMessage = originalBitStringMessage[0:extraAppendLength]

        bitStringMessage = '1' + bitStringMessage
        while (len(bitStringMessage) - 488) % 512 != 0:
            bitStringMessage = '0' + bitStringMessage

        bitStringMessage += extraAppendStringMessage

        return bitStringMessage

    def hashString(self, stringMessage):

        bitStringMessage = ''.join(format(ord(x), '08b') for x in stringMessage)
        bitStringMessage = self.pad(bitStringMessage)

        a0 = 0x67452301
        b0 = 0xefcdab89
        c0 = 0x98badcfe
        d0 = 0x10325476

        for i in range(0, len(bitStringMessage), 512):
            segment = bitStringMessage[i: i+512]

            M = []
            for j in range(0, 512, 32):
                M.append(segment[j:j+32])



            a = a0
            b = b0
            c = c0
            d = d0

            F = 0
            g = 0

            for j in range(0, 63):
                if 0 <= i and i <= 15:
                    F = (b & c) | ((~b) & d)
                    g = i
                elif 16 <= i and i <= 31:
                    F = (d & b) | ((~d) & c)
                    g = (5*i + 1) % 16
                elif 32 <= i and i <= 47:
                    F = b ^ c ^ d
                    g = (3*i + 5) % 16
                elif 48 <= i and i <= 63:
                    F = c ^ (b | (~d))
                    g = (7*i) % 16

                dtemp = d
                d = c
                c = b
                b = b + self.leftrotate((a + F + self.k[i] + int(M[g], 2)), self.shiftRounds[i])
                a = dtemp

            a0 += a
            b0 += b
            c0 += c
            d0 += d

            aHash = a0.to_bytes(4, sys.byteorder)
            bHash = b0.to_bytes(4, sys.byteorder)
            cHash = c0.to_bytes(4, sys.byteorder)
            dHash = d0.to_bytes(4, sys.byteorder)

            hash = bytearray()
            for byte in aHash:
                hash.append(byte)

            for byte in bHash:
                hash.append(byte)

            for byte in cHash:
                hash.append(byte)

            for byte in dHash:
                hash.append(byte)

            return hash

    def getDigestSize(self):
        return 16

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes
