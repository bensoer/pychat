__author__ = 'bensoer'

from crypto.cryptor import Cryptor

'''
Decryptor is an implementation of the Cryptor class and extends the functionality to allow decryption of encrypted
messages. The Decryptor takes the loaded algorithm from the Cryptor class and calls the decryptString methods on it
'''
class Decryptor(Cryptor):

    def __init__(self):
        Cryptor.__init__(self)
        self.setName("Decryptor")

    def decrypt(self, message):
        return self._loadedAlgorithm.decryptString(message)