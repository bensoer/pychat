__author__ = 'kbohlen'

from crypto.algorithms.algorithminterface import AlgorithmInterface

#import base64
from Crypto.Cipher import AES
from Crypto import Random

from tools.argparcer import ArgParcer

'''
Description of AESCipher

BLOCK_SIZE:
The block size for the cipher object; must be 16 bytes per FIPS-197 aka the
Federal Information Processing Standards Publication 197. Block size is
defined as a variable in the AES class (AES.block_size = 16)

KEY_SIZE:
The key size for the cipher object; can be 128, 192, or 256 bits as defined
per FIPS-197; this is equivalent to 16, 24, or 32 bytes. The size of the key is
proportional to the strength of the cipher

IV:
Most block cipher modes require a unique binary sequence called an 
initialization vector, for each encryption operation. The IV has to be
non-repeating and, for some modes, random as well. The initialization vector
is used to ensure distinct ciphertexts are produced even when the same
plaintext is encrypted multiple times independently with the same key.

PADDING:
Block cuphers work only on units of data of a fixed length (BLOCK_SIZE), but
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
class AESCipher(AlgorithmInterface):
    
    def __init__(self, arguments):
        self.key = b'this is a 16 bit'
        ## if they pass a k parameter, use as the key
        #key = ArgParcer.getValue(arguments, "-k")
        #if key == "":
        #    # this should throw an error as they need to pass a symetric key
        #else:
        #    self.key = bytes(unencryptedMessage, encoding='utf-8')
        #    # either check for required length
        #    # or compute a hash of required length

    def _pad(self, s):
        return s + (AES.block_size - len(s) % AES.block_size) * str(chr(AES.block_size - len(s) % AES.block_size))

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def encryptString(self, unencryptedMessage):
        #'''
        #this is a comment
        #'''
        print('plaintext: ' + unencryptedMessage + " length: " + str(len(unencryptedMessage)))
        paddedMessage = self._pad(unencryptedMessage)
        print('padded length: ' + str(len(paddedMessage)))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encryptedMessage = iv + cipher.encrypt(paddedMessage)
        print('encrypted: ' + str(encryptedMessage))
        return encryptedMessage

    def decryptString(self, encryptedMessage):
        #'''
        #The IV is the first block
        #'''
        iv = encryptedMessage[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        print(type(encryptedMessage))
        print(str(len(encryptedMessage[AES.block_size:])))
        decryptedMessage = cipher.decrypt(encryptedMessage[AES.block_size:])
        return str(decryptedMessage)
