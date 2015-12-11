__author__ = 'bensoer'

from crypto.cryptor import Cryptor

class Decryptor(Cryptor):

    def __init__(self):
        Cryptor.__init__(self)
        self.setName("Decryptor")

    def decrypt(self, message):
        return self._loadedAlgorithm.decryptString(message)