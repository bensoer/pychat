__author__ = 'kbohlen'

from crypto.algorithms.algorithminterface import AlgorithmInterface

from Crypto.PublicKey import RSA

''' 
Description of RSAPublicKey

RSA is a public key cryptosystem, also called asymmetric ctyptography. It uses
a pair of keys, one public and one private for encryption. The benefit of this
is that it does not require shared information like a symmetric key to create
a secure channel. 

A user of RSA creates and then publishes a public key based on two large prime
numbers, along with an auxiliary value. The prime numbers must be kept secret.
Anyone can use the public key to encrypt a message, but with currently
published methods, if the public key is large enough, only someone with
knowledge of the prime numbers can feasibly decode the message.
'''
class RSAPublicKey(AlgorithmInterface):

    def __init__(self, arguments):
        ''' 
        generate the public / private key pair to be used
        '''
        keySize = 2048
        self.key = RSA.generate(keySize)
        self.publicKey = self.key.publickey()
        self.otherPublicKey = None

    def sendFirstMessage(self):
        ''' 
        we need to send the other person our own public key
        '''
        return self.publicKey.exportKey(passphrase='pychat')
    
    def receiveFirstMessage(self, firstMessage):
        ''' 
        we should recieve the other persons public key
        '''
        self.otherPublicKey = RSA.importKey(firstMessage, passphrase='pychat')
        return False #returning True attempts to decrypt the message

    def encryptString(self, unencryptedMessage):
        ''' 
        must encrypt with other users public key (self.otherPublicKey)
        '''
        encryptedTuple = self.otherPublicKey.encrypt(bytes(unencryptedMessage,'utf-8'), 'pychat')
        encryptedMessage = encryptedTuple[0]
        return encryptedMessage

    def decryptString(self, encryptedMessage):
        ''' 
        assuming that the encrypted message was encrypted with self.publicKey
        generated above we can decrypt with our private key (self.key)
        '''
        decryptedMessage = self.key.decrypt(encryptedMessage)
        return decryptedMessage.decode('utf-8')
