__author__ = 'kbohlen'

from crypto.algorithms.algorithminterface import AlgorithmInterface

from Crypto.PublicKey import RSA
#from Crypto import Random

#from tools.argparcer import ArgParcer

'''
Description of RSAPublicKey
'''
class RSAPublicKey(AlgorithmInterface):
    
    def __init__(self, arguments):
        '''
        generate the public / private key pair to be used
        '''
        key_size = 1024
        self.key = RSA.generate(key_size)
        self.publickey = self.key.publickey()

    def sendFirstMessage(self):
        return self.publickey.exportKey(format='DER', passphrase=None, pkcs=1)
    
    def receiveFirstMessage(self, firstMessage):
        self.other_publickey = firstMessage
        return False #return true for debug to display public key

    def encryptString(self, unencryptedMessage):
        '''
        must encrypt with other users public key
        '''
        encryptedMessage = other_publickey.encrypt(unencryptedMessage)
        return encryptedMessage

    def decryptString(self, encryptedMessage):
        '''
        assuming that the encrypted message was encrypted with self.publickey generated above
        '''
        decryptedMessage = self.key.decrypt(encryptedMessage)
        return self._unpad(decryptedMessage).decode('utf-8')
