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
This code uses CBC or Cipher Block Chaining as it is the same implimentation
that OpenVPN uses.

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
         Round1->|   ShiftRows    |
                 |   MixColumns   |
   Round Key1 -> |   AddRoundKey  |
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
Simply the inverse of the encryption process. Just do everything backwards with
the inverse processes. 
'''
class PureAESCipher(AlgorithmInterface):

    block_size = 16

    sbox = 
    [
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

    sboxInv = 
    [
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

    rcon =
    [
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
    
    def __init__(self, arguments):
        ''' 
        # if they pass a k parameter, use as the password
        password = ArgParcer.getValue(arguments, "-k")
        while password == "":
            password = input("AES needs a passkey: ")
        # this is not actually going to be used as the passkey for AES
        # we are going to create a 256bit key from the given secret password
        h = hashlib.sha256()
        h.update(bytes(password, 'utf-8'))
        self.key = h.digest()
        '''

    def encryptString(self, unencryptedMessage):
        ''' 
        paddedMessage = self._pad(unencryptedMessage)
        iv =
        cipher =
        encryptedMessage = iv + cipher.encrypt(paddedMessage)
        return encryptedMessage
        '''

    def decryptString(self, encryptedMessage):
        ''' 
        The IV is the first block
        iv = encryptedMessage[:self.block_size]
        cipher =
        decryptedMessage = cipher.decrypt(encryptedMessage[self.block_size:])
        return self._unpad(decryptedMessage).decode('utf-8')
        '''

    def _pad(self, s):
        ''' 
        return s padded to a multiple of 16-bytes following PCKS7 padding
        '''
        return s + (16 - len(s)%16) * chr(16 - len(s)%16)

    def _unpad(self, s):
        ''' 
        return s stripped of PKCS7 padding
        '''
        return s[:-ord(s[len(s)-1:])]

    def _subBytes(self, state):
        ''' 
        sub the sbox value for each of the values in the matrix (state)
        '''
        for i in range(16):
            state[i] = sbox[state[i]]
        return state

    def _subBytesInv(self, state):
        ''' 
        sub the sbox_inv value for each of the values in the matrix (state)
        '''
        for i in range(16):
            state[i] = sboxInv[state[i]]
        return state

    def _rotate(self, row, n):
        ''' 
        return the original row circular shifted by n bytes to the left
        '''
        return row[n:]+row[0:n]

    def _shiftRows(self, state):
        ''' 
        for each row in the state call _rotate() with the appropiate offset to
        the left
        '''
        for i in range(4):
            state[i*4:i*4+4] = self._rotate(state[i*4:i*4+4],i)
        return state

    def _shiftRowsInv(self, state):
        ''' 
        for each row in the state call _rotate() with the appropiate offset to
        the right
        '''
        for i in range(4):
            state[i*4:i*4+4] = self._rotate(state[i*4:i*4+4],-i)
        return state

    def _galoisMul(self, a, b):
        ''' 
        Galois Multiplication of 8 bit characters a and b
        Used in the column mixing
        TBH not really sure what this does
        '''
        p = 0
        for i in range(8):
            if b & 1 == 1:
                p ^= a
            hiBitSet = a & 0x80
            a <<= 1
            s &= 0xFF
            if hiBitSet:
                a ^= 0x1b
            b >>= 1
        return p

    def _mixColumn(self, column):
        ''' 
        calls _galoisMul for 1 column of the state XORing results
        makes a copy of column by recasting it as a list
        uses encrypttion multiplication values
        TBH I am not sure why this works
        '''
        temp = list(column)
        g = self._galoisMul
        column[0] = g(temp[0],2) ^ g(temp[3],1) ^ g(temp[2],1) ^ g(temp[1],3)
        column[1] = g(temp[1],2) ^ g(temp[0],1) ^ g(temp[3],1) ^ g(temp[2],3)
        column[2] = g(temp[2],2) ^ g(temp[1],1) ^ g(temp[0],1) ^ g(temp[3],3)
        column[3] = g(temp[3],2) ^ g(temp[2],1) ^ g(temp[1],1) ^ g(temp[0],3)
        return column

    def _mixColumnInv(self, column):
        ''' 
        calls _galoisMul for 1 column of the state XORing results
        makes a copy of column by recasting it as a list
        uses decryption multiplication values
        TBH I am not sure why this works
        '''
        temp = list(column)
        g = self._galoisMul
        column[0] = g(temp[0],14) ^ g(temp[3],9) ^ g(temp[2],13) ^ g(temp[1],11)
        column[1] = g(temp[1],14) ^ g(temp[0],9) ^ g(temp[3],13) ^ g(temp[2],11)
        column[2] = g(temp[2],14) ^ g(temp[1],9) ^ g(temp[0],13) ^ g(temp[3],11)
        column[3] = g(temp[3],14) ^ g(temp[2],9) ^ g(temp[1],13) ^ g(temp[0],11)
        return column

    def _mixColumns(self, state):
        ''' 
        calls _mixColumn for each column in state
        iterates over the 4 columns
        constructs column taking every 4th byte of state
        '''
        for i in range(4):
            column = state[i:i+16:4]
            column = self.mixColumn(column)
            state[i:i+16:4] = column
        return state

    def _mixColumnsInv(self, state):
        ''' 
        wrapper for mixColumnInv
        iterates over the 4 columns
        constructs column taking every 4th byte of state
        '''
        for i in range(4):
            column = state[i:i+16:4]
            column = self.mixColumnInv(column)
            state[i:i+16:4] = column
        return state

    def _core(self, word, iteration):
        ''' 
        Rijndael key schedule core
        '''
        # rotate the 32-bit word 8 bits(1 byte) to the left
        word = self._rotate(word, 1)
        # apply sbox substitution on all 4 bytes of the 32-bit word
        for i in range(4):
            word[i] = self.sbox[word[i]]
        # XOR the output of the rcon operation with i to the first part
        # (leftmost) only
        word[0] = word[0] ^ self.rcon[iteration]
        return word

    def _expandKey(self, key, size, expandedKeySize):
        ''' 
        Rijndael's key expansion
        Expands an 128,192,256 key into an 176,208,240 bytes key
        expandedKey is a char list of appropiate size
        key is the non-expanded key
        '''
        # current expanded keySize, in bytes
        currentSize = 0
        rconIteration = 1
        expandedKey = [0] * expandedKeySize
        # set the 16, 24, 32 bytes of the expanded key to the input key
        for i in range(size):
            expandedKey[i] = key[i]
        currentSize += size

        while currentSize < expandedKeySize:
            # assign the previous 4 bytes to the temporary value t
            t = expandedKey[currentSize-4:currentSize]
            # every 16,24,32 bytes we apply the core schedule to t
            # and increment rconIteration afterwards
            if currentSize % size == 0:
                t = self._core(t, rconIteration)
                rconIteration += 1
            # for 256-bit keys, we add an extra sbox to the calculation
            if (size == 32) and ((currentSize % size) == 16):
                for l in range(4):
                    t[l] = self.sbox[t[l]]
            # XOR t with the four-byte block 16,24,32 bytes before the new expanded key
            # this becomes the next four bytes in the expanded key
            for m in range(4):
                expandedKey[currentSize] = expandedKey[currentSize - size] ^ t[m]
                currentSize += 1
        return expandedKey

    def _createRoundKey(self, expandedKey, n):
        ''' 
        creates a round key from the given expanded key and the round number
        '''
        return expandedKey[(n*16):(n*16+16)]

    def _addRoundKey(self, state, roundKey):
        ''' 
        XORs the round key to the state
        '''
        for i in range(16):
            state[i] ^= roundKey[i]
        return state

    def _aesRound(self, state, roundKey):
        ''' 
        a single round of AES encryption in order
        '''
        state = self._subBytes(state)
        state = self._shiftRows(state)
        state = self._mixColumns(state)
        state = self._addRoundKey(state, roundKey)
        return state

    def _aesRoundInv(self, state, roundKey):
        ''' 
        a single round of AES decryption in order
        '''
        state = self._shiftRowsInv(state)
        state = self._subBytesInv(state)
        state = self._addRoundKey(state, roundKey)
        state = self._mixColumnsInv(state)
        return state

    def _aesMain(self, state, expandedKey, numRounds):
        ''' 
        perform initial AES encryption operations, the standard rounds, and then the final operations
        it recreates a round key each round
        '''
        state = self._addRoundKey(state, self._createRoundKey(expandedKey, 0))
        i = 1
        while i < numRounds:
            state = self._aesRound(state, self._createRoundKey(expandedKey, 16*i))
            i += 1
        state = self._subBytes(state)
        state = self._shiftRows(state)
        state = self._addRoundKey(state, self._createRoundKey(expandedKey, 16*numRounds))
        return state

    def _aesMainInv(self, state, expandedKey, numRounds):
        ''' 
        perform initial AES decryption operations, the standard rounds, and the$
        it recreates a round key each round
        '''
        state = self._addRoundKey(state, self._createRoundKey(expandedKey, 16*numRounds))
        i = numRounds - 1
        while i > 0:
            state = self._aesRoundInv(state, self._createRoundKey(expandedKey, 16*i))
            i -= 1
        state = self._subBytesInv(state)
        state = self._shiftRowsInv(state)
        state = self._addRoundKey(state, self._createRoundKey(expandedKey, 0)
        return state

    def _encryptBlock(self, block, key, size):
        ''' 
        encrypts a 128 bit input block of data with key and size given
        AES operates on a 4 × 4 column-major order matrix
        thus we need to transpose the input data
        '''
        output = [0] * 16
        # the number of rounds
        numRounds = 0
        # the 128 bit block to encode refered to as 'state'
        state = [0] * 16
        # set the number of rounds
        if size == 16: numRounds = 10
        elif size == 24: numRounds = 12
        elif size == 32: numRounds = 14
        else: return None

        # the expanded keySize
        expandedKeySize = 16*(numRounds+1)

        # Set the state values, for the state:
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
                state[(i+(j*4))] = block[(i*4)+j]

        # expand the key into an 176, 208, 240 bytes key
        expandedKey = self._expandKey(key, size, expandedKeySize)

        # encrypt the state using the expandedKey
        state = self._aesMain(state, expandedKey, numRounds)

        # unmap the state again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k*4)+l] = state[(k+(l*4))]
        return output

    def _decryptBlock(self, block, key, size):
        ''' 
        decrypts a 128 bit input block of data with key and size given
        '''
        output = [0] * 16
        # the number of rounds
        numRounds = 0
        # the 128 bit block to decode
        state = [0] * 16
        # set the number of rounds
        if size == 16: numRounds = 10
        elif size == 24: numRounds = 12
        elif size == 32: numRounds = 14
        else: return None

        # the expanded keySize
        expandedKeySize = 16*(numRounds+1)

        # iterate over the columns
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                state[(i+(j*4))] = block[(i*4)+j]

        # expand the key into an 176, 208, 240 bytes key
        expandedKey = self._expandKey(key, size, expandedKeySize)

        # decrypt the block using the expandedKey
        state = self.aes_invMain(state, expandedKey, numRounds)

        # unmap the block again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k*4)+l] = state[(k+(l*4))]
        return output
