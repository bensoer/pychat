__author__ = 'bensoer'

class Cryptor:

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setAlgorithm(self, strAlgorithm):
        self.strAlgorithm = strAlgorithm
        self.strPackage = strAlgorithm.lower()

    def testAlgorithm(self):
        print(" -- Testing Algorithm Parameter -- ")
        try:
            pkg = __import__('crypto.algorithms.' + self.strPackage, fromlist=[self.strAlgorithm])
            mod = getattr(pkg, self.strAlgorithm)
            algorithm = mod()
            algorithm.encryptString("Here is a message")
        except (Exception, AttributeError) as error:
            print("Import Of Algorithm Failed. Perhaps you used the wrong name ? The passed in algorithm was: " +
                  self.strAlgorithm)
            print("Note you must pass in the name of the class and casing matters. PyChat will handle resolving " +
                  "the package")
            print("Test Failed In The : " + self.getName())
            raise error
        finally:
            print(" -- Testing Algorithm Parameter Complete -- ")