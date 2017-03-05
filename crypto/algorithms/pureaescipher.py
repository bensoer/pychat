__author__ = 'kbohlen'

from crypto.algorithms.algorithminterface import AlgorithmInterface

import os
import math

from tools.argparcer import ArgParcer

''' 
Description of PureAESCipher

BLOCK_SIZE:
The block size for the cipher object; must be 16 bytes per FIPS-197 aka the
Federal Information Processing Standards Publication 197.

KEY_SIZE:
The key size for the cipher object; can be 128, 192, or 256 bits as defined
per FIPS-197; this is equivalent to 16, 24, or 32 bytes. The size of the key is
proportional to the strength of the cipher, this implementation uses only uses
the most secure key size of 256 bits (AES-256) requiring only 1 sbox.

IV:
Most block cipher modes require a unique binary sequence called an 
initialization vector, for each encryption operation. The IV has to be
non-repeating and, for some modes, random as well. The initialization vector
is used to ensure distinct ciphertexts are produced even when the same
plaintext is encrypted multiple times independently with the same key.

PADDING:
Block ciphers work only on units of data of a fixed length (BLOCK_SIZE), but
message length can vary. So some modes (namely ECB and CBC) require that the
final block be padded before encryption. This is done by adding null bytes to
the plaintext to increase it's length to a multiple of the BLOCK_SIZE, keeping
in mind that the original length of the plaintext must be recovered.

MODES:
The mode of operation describes how to repeatedly apply a cipher's single
block operation to securely transform amounts of data larger than a block.
https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation

ALGORITHM:
AES is an iterative cipher. It comprises of a series of operations performing
substitutions and shuffling bits around. AES uses 10 rounds for 128-bit keys,
12 rounds for 192-bit keys, and 14 rounds for 256-bit keys.

ENCRYPTION PROCESS:

   Cipher Key         Plaintext
   (256 bit)          (128 bit)
       |                  |
       V                  V
   Round Key0  --->  AddRoundKey
   (128 bit)     ------------------
                 |   SubBytes     |
        Round1 ->|   ShiftRows    |
                 |   MixColumns   |
    Round Key1 ->|   AddRoundKey  |
                 ------------------
                        ... x14
SubBytes- 
The 16 input bytes are substituted by looking up a fixed table (sbox). The
result is a matrix of four rows and four columns.

ShiftRows-
Performs a circular shift or rotate to each row of the 4x4 matrix. Each row is
rotated by N-1 positions to the left, where N is the Nth row.

MixColumns-
Performs Galois Multiplication on each column of the 4x4 matrix. The result is
completely new bytes in each of the columns. This step is not performed in the
last round.

AddRoundKey-
All 128 bits of the matrix are XORed with the 128-bit RoundKey.

DECRYPTION PROCESS:
The inverse of the encryption process.
'''

class PureAESCipher(AlgorithmInterface):

    def __init__(self, arguments):
        ''' 
        Initialize mode of operation object
        Verify that key and mode are correctly configured
        '''
        self.moo = AESModeOfOperation()

        # if they pass a k parameter, use as the key; otherwise default 32bit key
        key = ArgParcer.getValue(arguments, '-k')
        validKey = 0
        while(not validKey):
            if len(key) == 16:
                self.cypherkey = list(bytes(key,'utf-8'))
                self.keylen = self.moo.aes.keySize['SIZE_128']
                validKey = 1
            elif len(key) == 24:
                self.cypherkey = list(bytes(key,'utf-8'))
                self.keylen = self.moo.aes.keySize['SIZE_192']
                validKey = 1
            elif len(key) == 32:
                self.cypherkey = list(bytes(key,'utf-8'))
                self.keylen = self.moo.aes.keySize['SIZE_256']
                validKey = 1
            else:
                print('ERROR: Key not correct size')
                key = input('Enter key of size 16,24,32:')

        #if they pass a m parameter, use as the mode; otherwise default CBC mode
        mode = ArgParcer.getValue(arguments, '-m')
        if mode == 'OFB':
            self.mode = self.moo.modeOfOperation['OFB']
        elif mode == 'CFB':
            self.mode = self.moo.modeOfOperation['CFB']
        else:
            self.mode = self.moo.modeOfOperation['CBC']
        

    def encryptString(self, unencryptedMessage):
        ''' 
        Process to encrypt string:
        Generate a random 16 byte IV
        Encrypt unencryptedMessage using mode and key defined in init
        Return plaintext IV and encrypted cipher
        '''
        iv = self._generateRandomKey(16)

        ciph = self.moo.encrypt(unencryptedMessage, 
                                     self.mode, 
                                     self.cypherkey, 
                                     self.keylen, 
                                     iv)

        return iv + bytes(ciph)

    def decryptString(self, encryptedMessage):
        ''' 
        Process to decrypt string:
        Pull IV transmitted in plaintext to use in decryption process
        Decrypt cipher from remaining message
        Return just he unencrypted message
        '''
        iv = encryptedMessage[:16]

        decr = self.moo.decrypt(encryptedMessage[16:],  
                                     self.mode, 
                                     self.cypherkey, 
                                     self.keylen, 
                                     iv)

        return decr
    
    def _generateRandomKey(self, keysize):
        '''
        Generates a key from random data of length `keysize`
        The returned key is a string of bytes
        '''
        if keysize not in (16, 24, 32):
            print('ERROR: Invalid keysize, %s. Should be one of (16, 24, 32).')
        return os.urandom(keysize)


class AES(object):

    # valid key size dictionary
    keySize = dict(SIZE_128=16, SIZE_192=24, SIZE_256=32)

    sbox = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    ]

    sboxInv = [
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
    ]

    rcon = [
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 
        0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 
        0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 
        0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 
        0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 
        0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d
    ]

    def _pad(self, s):
        '''
        return s padded to a multiple of 16-bytes by PKCS7 padding
        '''
        numpads = 16 - (len(s)%16)
        return s + numpads*chr(numpads)

    def _unpad(self, s):
        '''
        return s stripped of PKCS7 padding
        '''
        if len(s)%16 or not s:
            raise ValueError("String of len %d can't be PCKS7-padded" % len(s))
        numpads = ord(s[-1])
        if numpads > 16:
            raise ValueError("String ending with %r can't be PCKS7-padded" % s[-1])
        return s[:-numpads]

    def _getSBoxValue(self, num):
        '''
        Retrieves a given S-Box Value
        '''
        return self.sbox[num]

    def _getSBoxInvert(self, num):
        '''
        Retrieves a given Inverted S-Box Value
        '''
        return self.sboxInv[num]

    def _getrconValue(self, num):
        '''
        Retrieves a given rcon Value
        '''
        return self.rcon[num]

    def _rotate(self, word):
        '''
        Rijndael's key schedule rotate operation.

        Rotate a word eight bits to the left: eg, rotate(1d2c3a4f) == 2c3a4f1d
        Word is an char list of size 4 (32 bits overall).
        '''
        return word[1:] + word[:1]

    def _core(self, word, iteration):
        '''
        Key schedule core
        '''
        # rotate the 32-bit word 8 bits to the left
        word = self._rotate(word)
        # apply S-Box substitution on all 4 parts of the 32-bit word
        for i in range(4):
            word[i] = self._getSBoxValue(word[i])
        # XOR the output of the rcon operation with i to the first part
        # (leftmost) only
        word[0] = word[0] ^ self._getrconValue(iteration)
        return word

    def _expandKey(self, key, size, expandedKeySize):
        '''
        Rijndael's key expansion

        Expands an 128,192,256 key into an 176,208,240 bytes key

        expandedKey is a char list of large enough size,
        key is the non-expanded key.
        '''
        # current expanded keySize, in bytes
        currentSize = 0
        rconIteration = 1
        expandedKey = [0] * expandedKeySize

        # set the 16, 24, 32 bytes of the expanded key to the input key
        for j in range(size):
            expandedKey[j] = key[j]
        currentSize += size

        while currentSize < expandedKeySize:
            # assign the previous 4 bytes to the temporary value t
            t = expandedKey[currentSize-4:currentSize]

            # every 16,24,32 bytes we apply the core schedule to t
            # and increment rconIteration afterwards
            if currentSize % size == 0:
                t = self._core(t, rconIteration)
                rconIteration += 1
            # For 256-bit keys, we add an extra sbox to the calculation
            if size == self.keySize["SIZE_256"] and ((currentSize % size) == 16):
                for l in range(4): t[l] = self._getSBoxValue(t[l])

            # We XOR t with the four-byte block 16,24,32 bytes before the new
            # expanded key.  This becomes the next four bytes in the expanded
            # key.
            for m in range(4):
                expandedKey[currentSize] = expandedKey[currentSize - size] ^ \
                        t[m]
                currentSize += 1

        return expandedKey

    def _addRoundKey(self, state, roundKey):
        '''
        Adds (XORs) the round key to the state
        '''
        for i in range(16):
            state[i] ^= roundKey[i]
        return state

    def _createRoundKey(self, expandedKey, roundKeyPointer):
        '''
        Create a round key.
        Creates a round key from the given expanded key and the
        position within the expanded key.
        '''
        roundKey = [0] * 16
        for i in range(4):
            for j in range(4):
                roundKey[j*4+i] = expandedKey[roundKeyPointer + i*4 + j]
        return roundKey

    def _galoisMul(self, a, b):
        '''
        Galois multiplication of 8 bit characters a and b
        '''
        p = 0
        for counter in range(8):
            if b & 1: p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            # keep a 8 bit
            a &= 0xFF
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p

    def _subBytes(self, state, isInv):
        '''
        substitute all the values from the state with the value in the SBox
        using the state value as index for the SBox
        '''
        if isInv: getter = self._getSBoxInvert
        else: getter = self._getSBoxValue
        for i in range(16): state[i] = getter(state[i])
        return state

    def _shiftRows(self, state, isInv):
        '''
        iterate over the 4 rows and call _shiftRow() with that row
        '''
        for i in range(4):
            state = self._shiftRow(state, i*4, i, isInv)
        return state

    def _shiftRow(self, state, statePointer, nbr, isInv):
        '''
        each iteration shifts the row to the left by 1
        '''
        for i in range(nbr):
            if isInv:
                state[statePointer:statePointer+4] = \
                        state[statePointer+3:statePointer+4] + \
                        state[statePointer:statePointer+3]
            else:
                state[statePointer:statePointer+4] = \
                        state[statePointer+1:statePointer+4] + \
                        state[statePointer:statePointer+1]
        return state

    def _mixColumns(self, state, isInv):
        '''
        galois multiplication of the 4x4 matrix
        '''
        # iterate over the 4 columns
        for i in range(4):
            # construct one column by slicing over the 4 rows
            column = state[i:i+16:4]
            # apply the _mixColumn on one column
            column = self._mixColumn(column, isInv)
            # put the values back into the state
            state[i:i+16:4] = column

        return state

    def _mixColumn(self, column, isInv):
        '''
        galois multiplication of 1 column of the 4x4 matrix
        '''
        if isInv: mult = [14, 9, 13, 11]
        else: mult = [2, 1, 1, 3]
        cpy = list(column)
        g = self._galoisMul

        column[0] = g(cpy[0], mult[0]) ^ g(cpy[3], mult[1]) ^ g(cpy[2], mult[2]) ^ g(cpy[1], mult[3])
        column[1] = g(cpy[1], mult[0]) ^ g(cpy[0], mult[1]) ^ g(cpy[3], mult[2]) ^ g(cpy[2], mult[3])
        column[2] = g(cpy[2], mult[0]) ^ g(cpy[1], mult[1]) ^ g(cpy[0], mult[2]) ^ g(cpy[3], mult[3])
        column[3] = g(cpy[3], mult[0]) ^ g(cpy[2], mult[1]) ^ g(cpy[1], mult[2]) ^ g(cpy[0], mult[3])
        return column

    def _aesRound(self, state, roundKey):
        '''
        applies the 4 operations of the forward round in sequence
        '''
        state = self._subBytes(state, False)
        state = self._shiftRows(state, False)
        state = self._mixColumns(state, False)
        state = self._addRoundKey(state, roundKey)
        return state

    def _aesRoundInv(self, state, roundKey):
        '''
        applies the 4 operations of the inverse round in sequence
        '''
        state = self._shiftRows(state, True)
        state = self._subBytes(state, True)
        state = self._addRoundKey(state, roundKey)
        state = self._mixColumns(state, True)
        return state

    def _aesMain(self, state, expandedKey, nbrRounds):
        '''
        Perform the initial operations, the standard round, and the final
        operations of the forward aes, creating a round key for each round
        '''
        state = self._addRoundKey(state, self._createRoundKey(expandedKey, 0))
        i = 1
        while i < nbrRounds:
            state = self._aesRound(state, self._createRoundKey(expandedKey, 16*i))
            i += 1
        state = self._subBytes(state, False)
        state = self._shiftRows(state, False)
        state = self._addRoundKey(state, self._createRoundKey(expandedKey, 16*nbrRounds))
        return state

    def _aesMainInv(self, state, expandedKey, nbrRounds):
        '''
        Perform the initial operations, the standard round, and the final
        operations of the inverse aes, creating a round key for each round
        '''
        state = self._addRoundKey(state, self._createRoundKey(expandedKey, 16*nbrRounds))
        i = nbrRounds - 1
        while i > 0:
            state = self._aesRoundInv(state, self._createRoundKey(expandedKey, 16*i))
            i -= 1
        state = self._shiftRows(state, True)
        state = self._subBytes(state, True)
        state = self._addRoundKey(state, self._createRoundKey(expandedKey, 0))
        return state

    def _encryptBlock(self, iput, key, size):
        '''
        encrypts a 128 bit input block against the given key of size specified
        '''
        output = [0] * 16
        # the number of rounds
        nbrRounds = 0
        # the 128 bit block to encode
        block = [0] * 16
        # set the number of rounds
        if size == self.keySize["SIZE_128"]: nbrRounds = 10
        elif size == self.keySize["SIZE_192"]: nbrRounds = 12
        elif size == self.keySize["SIZE_256"]: nbrRounds = 14
        else: return None

        # the expanded keySize
        expandedKeySize = 16*(nbrRounds+1)

        # Set the block values, for the block:
        # a0,0 a0,1 a0,2 a0,3
        # a1,0 a1,1 a1,2 a1,3
        # a2,0 a2,1 a2,2 a2,3
        # a3,0 a3,1 a3,2 a3,3
        # the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3
        #
        # iterate over the columns
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                block[(i+(j*4))] = iput[(i*4)+j]

        # expand the key into an 176, 208, 240 bytes key
        # the expanded key
        expandedKey = self._expandKey(key, size, expandedKeySize)

        # encrypt the block using the expandedKey
        block = self._aesMain(block, expandedKey, nbrRounds)

        # unmap the block again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k*4)+l] = block[(k+(l*4))]
        return output

    def _decryptBlock(self, iput, key, size):
        '''
        decrypts a 128 bit input block against the given key of size specified
        '''
        output = [0] * 16
        # the number of rounds
        nbrRounds = 0
        # the 128 bit block to decode
        block = [0] * 16
        # set the number of rounds
        if size == self.keySize["SIZE_128"]: nbrRounds = 10
        elif size == self.keySize["SIZE_192"]: nbrRounds = 12
        elif size == self.keySize["SIZE_256"]: nbrRounds = 14
        else: return None

        # the expanded keySize
        expandedKeySize = 16*(nbrRounds+1)

        # Set the block values, for the block:
        # a0,0 a0,1 a0,2 a0,3
        # a1,0 a1,1 a1,2 a1,3
        # a2,0 a2,1 a2,2 a2,3
        # a3,0 a3,1 a3,2 a3,3
        # the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3

        # iterate over the columns
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                block[(i+(j*4))] = iput[(i*4)+j]
        # expand the key into an 176, 208, 240 bytes key
        expandedKey = self._expandKey(key, size, expandedKeySize)
        # decrypt the block using the expandedKey
        block = self._aesMainInv(block, expandedKey, nbrRounds)
        # unmap the block again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k*4)+l] = block[(k+(l*4))]
        return output


class AESModeOfOperation(object):

    aes = AES()

    # structure of supported modes of operation
    modeOfOperation = dict(OFB=0, CFB=1, CBC=2)

    # converts a 16 character string into a number array
    def convertString(self, string, start, end, mode):
        if end - start > 16: end = start + 16
        if mode == self.modeOfOperation["CBC"]: ar = [0] * 16
        else: ar = []

        i = start
        j = 0
        while len(ar) < end - start:
            ar.append(0)
        while i < end:
            ar[j] = ord(string[i])
            j += 1
            i += 1

        return ar

    # Mode of Operation Encryption
    # stringIn - Input String
    # mode - mode of type modeOfOperation
    # hexKey - a hex key of the bit length size
    # size - the bit length of the key
    # hexIV - the 128 bit hex Initilization Vector
    def encrypt(self, stringIn, mode, key, size, IV):
        if len(key) % size:
            return None
        if len(IV) % 16:
            return None
        # the AES input/output
        plaintext = []
        iput = [0] * 16
        output = []
        ciphertext = [0] * 16
        # the output cipher string
        cipherOut = []
        # char firstRound
        firstRound = True
        if stringIn != None:
            for j in range(int(math.ceil(float(len(stringIn))/16))):
                start = j*16
                end = j*16+16
                if  end > len(stringIn):
                    end = len(stringIn)
                plaintext = self.convertString(stringIn, start, end, mode)
                if mode == self.modeOfOperation["CFB"]:
                    if firstRound:
                        output = self.aes._encryptBlock(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes._encryptBlock(iput, key, size)
                    for i in range(16):
                        if len(plaintext)-1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output)-1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext)-1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]
                    for k in range(end-start):
                        cipherOut.append(ciphertext[k])
                    iput = ciphertext
                elif mode == self.modeOfOperation["OFB"]:
                    if firstRound:
                        output = self.aes._encryptBlock(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes._encryptBlock(iput, key, size)
                    for i in range(16):
                        if len(plaintext)-1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output)-1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext)-1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]
                    for k in range(end-start):
                        cipherOut.append(ciphertext[k])
                    iput = output
                elif mode == self.modeOfOperation["CBC"]:
                    for i in range(16):
                        if firstRound:
                            iput[i] =  plaintext[i] ^ IV[i]
                        else:
                            iput[i] =  plaintext[i] ^ ciphertext[i]
                    firstRound = False
                    ciphertext = self.aes._encryptBlock(iput, key, size)
                    # always 16 bytes because of the padding for CBC
                    for k in range(16):
                        cipherOut.append(ciphertext[k])
        return cipherOut

    # Mode of Operation Decryption
    # cipherIn - Encrypted String
    # mode - mode of type modeOfOperation
    # key - a number array of the bit length size
    # size - the bit length of the key
    # IV - the 128 bit number array Initilization Vector
    def decrypt(self, cipherIn, mode, key, size, IV):
        # cipherIn = unescCtrlChars(cipherIn)
        if len(key) % size:
            return None
        if len(IV) % 16:
            return None
        # the AES input/output
        ciphertext = []
        iput = []
        output = []
        plaintext = [0] * 16
        # the output plain text string
        stringOut = ''
        # char firstRound
        firstRound = True
        if cipherIn != None:
            for j in range(int(math.ceil(float(len(cipherIn))/16))):
                start = j*16
                end = j*16+16
                if j*16+16 > len(cipherIn):
                    end = len(cipherIn)
                ciphertext = cipherIn[start:end]
                if mode == self.modeOfOperation["CFB"]:
                    if firstRound:
                        output = self.aes._encryptBlock(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes._encryptBlock(iput, key, size)
                    for i in range(16):
                        if len(output)-1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext)-1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output)-1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]
                    for k in range(end-start):
                        stringOut += chr(plaintext[k])
                    iput = ciphertext
                elif mode == self.modeOfOperation["OFB"]:
                    if firstRound:
                        output = self.aes._encryptBlock(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes._encryptBlock(iput, key, size)
                    for i in range(16):
                        if len(output)-1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext)-1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output)-1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]
                    for k in range(end-start):
                        stringOut += chr(plaintext[k])
                    iput = output
                elif mode == self.modeOfOperation["CBC"]:
                    output = self.aes._decryptBlock(ciphertext, key, size)
                    for i in range(16):
                        if firstRound:
                            plaintext[i] = IV[i] ^ output[i]
                        else:
                            plaintext[i] = iput[i] ^ output[i]
                    firstRound = False
                    for k in range(end-start):
                        stringOut += chr(plaintext[k])
                    iput = ciphertext
        return stringOut
