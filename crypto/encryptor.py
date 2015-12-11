__author__ = 'bensoer'

from crypto.cryptor import Cryptor

class Encryptor(Cryptor):

    def __init__(self):
        Cryptor.__init__(self)
        self.setName("Encryptor")

    def encrypt(self, message):
        return self._loadedAlgorithm.encryptString(message)
