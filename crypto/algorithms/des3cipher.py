__author__ = 'kbohlen'

from crypto.algorithms.algorithminterface import AlgorithmInterface

from Crypto.Cipher import DES3
from Crypto import Random

from tools.argparcer import ArgParcer

'''
Description of DES3Cipher

BLOCK_SIZE:
The block size for the cipher object; must be 8 bytes. Block size is
defined as a variable in the DES3 class (DES3.block_size = 8)

ALGORITHM:
Triple DES uses a "key bundle" that comprises three DES keys: K1, K2, and K3,
each of 56 bits.
The encryption algorithm is:
    ciphertext = E_K3(D_K2(E_K1(plaintext)))
(DES encrypt with K1, DES decrypt with K2, then DES encrypt with K3)
The decryption is the reverse:
    plaintext = D_K1(E_K2(D_K3(ciphertext)))
(decrypt with K3, encrypt with K2, then decrypt with K1)

KEY_SIZE:
The key size for the cipher object; can be 56, 112, or 168 bits, this is
equivalent to 7, 14, or 21 bytes. The size of the key is proportional to
the strength of the cipher.

KEY_OPTIONS:
The standards define three keying options:
Keying option 1:
    All three keys are independent.
Keying option 2:
    K1 and K2 are independent, and K3 = K1.
Keying option 3:
    All three keys are identical, i.e. K1 = K2 = K3.
Keying option 1 is the strongest, with 3 × 56 = 168 independent key bits.

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
'''
class DES3Cipher(AlgorithmInterface):
    
    def __init__(self, arguments):
        # if they pass a k parameter, use as the password
        key = ArgParcer.getValue(arguments, "-k")
        while key == "":
            key = input("DES3 needs a 16 char long key: ")
        self.key = bytes(key, 'utf-8')

    def _pad(self, s):
        return s + (DES3.block_size - len(s) % DES3.block_size) * str(chr(DES3.block_size - len(s) % DES3.block_size))

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def encryptString(self, unencryptedMessage):
        #'''
        #this is a comment
        #'''
        paddedMessage = self._pad(unencryptedMessage)
        iv = Random.new().read(DES3.block_size)
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv)
        encryptedMessage = iv + cipher.encrypt(paddedMessage)
        return encryptedMessage

    def decryptString(self, encryptedMessage):
        #'''
        #The IV is the first block
        #'''
        iv = encryptedMessage[:DES3.block_size]
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv)
        decryptedMessage = cipher.decrypt(encryptedMessage[DES3.block_size:])
        return self._unpad(decryptedMessage).decode('utf-8')
