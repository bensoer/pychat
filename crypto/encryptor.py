__author__ = 'bensoer'

from crypto.cryptor import Cryptor

'''
Encryptor is an implementation of the Cryptor class and extends the functionality to allow encryption of messages.
The Encryptor takes the loaded algorithm from the Cryptor class and calls the decryptString methods on it
'''
class Encryptor(Cryptor):

    def __init__(self):
        Cryptor.__init__(self)
        self.setName("Encryptor")

    def encrypt(self, message):
        return self._loadedAlgorithm.encryptString(message)
