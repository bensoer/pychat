__author__ = 'bensoer'

from crypto.cryptor import Cryptor

class Encryptor(Cryptor):

    def __init__(self):
        Cryptor.__init__(self)
        self.setName("Encryptor")

    def encrypt(self, message):
        try:
            pkg = __import__('crypto.algorithms.' + self.strPackage, fromlist=[self.strAlgorithm])
            mod = getattr(pkg, self.strAlgorithm)
            algorithm = mod()
            return algorithm.encryptString(message)
        except (Exception, AttributeError) as error:
            print("Import Of Algorithm Failed. Perhaps you used the wrong name ? The passed in algorithm was: " +
                  self.strAlgorithm)
            print("Note you must pass in the name of the class and casing matters. PyChat will handle resolving " +
                  "the package")
            raise error