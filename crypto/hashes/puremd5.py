__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import MD5 as libmd5
import math
import sys
import base64

# https://www.ietf.org/rfc/rfc1321.txt
# https://en.wikipedia.org/wiki/MD5 - example implementation


class PureMD5(HashInterface):


    shiftRounds = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    k = []

    def __init__(self):
        # generate k table
        for i in range(0, 63):
            self.k.append(math.floor(((2 ** 32) * abs(math.sin(i + 1)))))

    def rotl(self, num, bits):
        bit = num & (1 << (bits - 1))
        num <<= 1
        if (bit):
            num |= 1
        num &= (2 ** bits - 1)

        return num


    def leftrotate(self, x, c):
        return (x << c) | (x >> (32-c))

    def pad(self, bitStringMessage):

        originalBitStringMessage = bitStringMessage
        extraAppendStringMessage = ""
        if len(originalBitStringMessage) > 64:
            extraAppendStringMessage = originalBitStringMessage[0:64]
        else:
            extraAppendStringMessage = originalBitStringMessage
            while len(extraAppendStringMessage) < 64:
                extraAppendStringMessage += '0'

        bitStringMessage = '1' + bitStringMessage
        while (len(bitStringMessage) - 448) % 512 != 0:
            bitStringMessage = '0' + bitStringMessage

        bitStringMessage += extraAppendStringMessage
        return bitStringMessage

    def hashString(self, stringMessage):

        bitStringMessage = ''.join(format(ord(x), '08b') for x in stringMessage)
        bitStringMessage = self.pad(bitStringMessage)

        print(len(bitStringMessage))

        a0 = 0x67452301
        print(a0)
        b0 = 0xefcdab89
        c0 = 0x98badcfe
        d0 = 0x10325476

        for i in range(0, len(bitStringMessage), 512):
            segment = bitStringMessage[i: i+512]

            M = []
            for j in range(0, 512, 32):
                M.append(segment[j:j+32])

            print(M)


            a = a0
            print("A Before: " + str(a))
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

                print("A Loop: " + str(j) + ": " + str(a))
                dtemp = d
                d = c
                c = b

                value = a + F + self.k[j] + int(M[g], 2)
                print("Pre Rotate Value: " + str(value) + " . " + bin(value))
                print("Rotate Amount: " + str(self.shiftRounds[j]))
                b = b + self.rotl(value, self.shiftRounds[j])
                print("Post Rotate Value: " + str(b) + " . " + bin(b))
                a = dtemp

            a0 += a
            b0 += b
            c0 += c
            d0 += d

            print(a0)
            print(a0.bit_length())
            aHash = a0.to_bytes(4, sys.byteorder, signed=False)

            bHash = b0.to_bytes(4, sys.byteorder, signed=False)
            cHash = c0.to_bytes(4, sys.byteorder, signed=False)
            dHash = d0.to_bytes(4, sys.byteorder, signed=False)

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
