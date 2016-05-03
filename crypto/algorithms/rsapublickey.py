__author__ = 'kbohlen'

from crypto.algorithms.algorithminterface import AlgorithmInterface

from Crypto.PublicKey import RSA
from Crypto import Random

from tools.argparcer import ArgParcer

'''
Description of RSAPublicKey
'''
class RSAPublicKey(AlgorithmInterface):
    
    def __init__(self, arguments):
	key_size = 1024
        # generate the public / private key pair to be used
        self.key = RSA.generate(key_size)
        self.publickey = self.key.publickey()

    def encryptString(self, unencryptedMessage):
        '''
        must encrypt with other users public key
        '''
        encryptedMessage = other_publickey.encrypt()
        return encryptedMessage

    def decryptString(self, encryptedMessage):
        '''
        assuming that the encrypted message as encrypted with self.publickey generated above
        '''
        decryptedMessage = self.key.decrypt(encryptedMessage)
        return self._unpad(decryptedMessage).decode('utf-8')
