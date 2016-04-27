__author__ = 'bensoer'

import types
from crypto.algorithms.algorithminterface import AlgorithmInterface

'''
Cryptor is a Base class defining functionality for a Cryptographic class. This includes functionality for setting and
testing the algorithm aswell as setting the name for the cryptographic class. It is recommended the child class call
and set the name at initialization
'''
class Cryptor:

    __name = ""
    _strPackage = ""
    _strAlgorithm = ""
    _loadedAlgorithm = None


    '''
    setName sets the name attribute for the Cryptor class. This attribute is referred to in debugging and presenting
    errors so that the viewer can determine what child class, inheriting Cryptor is causing the error
    '''
    def setName(self, name):
        self.__name = name

    '''
    getName gets the name of the attribute set for the Cryptor class
    :return name String - the name attribute set
    '''
    def getName(self):
        return self.__name

    '''
    setAlgorithm sets the algorithm to be dynamicaly loaded and used by the inheriting child class. This value is
    used to test dynamic loading in the testAlgorithm function
    :param strAlgorithm String - the algorithm to be dynamicaly loaded as a string
    '''
    def setAlgorithm(self, strAlgorithm):
        self._strAlgorithm = strAlgorithm
        self._strPackage = strAlgorithm.lower()

    '''
    testAlgorithm tests the strAlgorithm string value as to whether it will dynamicaly load a class or not. The tester
    searched in the crypto.algorithms package for the passed in algorithm as all lowercase and then will attempt to
    load the class within the .py file as the passed in algorithm name with its passed in casing. At any point of
    failure this test will fail and throw an error from the dynamic loading functions of at what point failed
    '''
    def testAlgorithm(self):
        print(" -- Testing Algorithm Parameter -- ")
        try:
            pkg = __import__('crypto.algorithms.' + self._strPackage, fromlist=[self._strAlgorithm])
            print("> Dynamic Package Load Successful")
            mod = getattr(pkg, self._strAlgorithm)
            print("> Dynamic Class Load Successful")
            algorithm = mod(self._arguments)
            #algorithm = mod()
            print("> Instantiation Successful")
            if isinstance(algorithm, AlgorithmInterface):
                print("> Instantiated Class Is Inheriting AlgorithmInterface")
            else:
                print("> Instantiated Class Does Not Inherit AlgorithmInterface. Test Failure")
                return False
            encResponse = algorithm.encryptString("Here is a message")
            if isinstance(encResponse, str):
                print("> Test Encryption Successful")
            else:
                print("> Test Encryption Failed. A String Type Was Not Returned")
                print("> Type Is: " + type(encResponse))
                return False
            decResponse = algorithm.decryptString("Here is a message")
            if isinstance(decResponse, str):
                 print("> Test Decryption Successful")
            else:
                print(">Test Decryption Failed. A String Type Was Not Returned")
                print("> Type Is: " + type(decResponse))
                return False
            return True
        except (Exception, AttributeError) as error:
            print("Import Of Algorithm Failed. Perhaps you used the wrong name ? The passed in algorithm was: " +
                  self._strAlgorithm)
            print("Note you must pass in the name of the class and casing matters. PyChat will handle resolving " +
                  "the package")
            #print("Test Failed In The : " + self.getName())
            raise error
        finally:
            print(" -- Testing Algorithm Parameter Complete -- ")



    def loadAlgorithm(self):
        print(" -- Loading Algorithm Into System -- ")
        pkg = __import__('crypto.algorithms.' + self._strPackage, fromlist=[self._strAlgorithm])
        mod = getattr(pkg, self._strAlgorithm)
        self._loadedAlgorithm = mod(self._arguments)

    def setArguments(self, arguments):
        self._arguments = arguments

    # -- Encryption Methods --
    def encrypt(self, message):
        return self._loadedAlgorithm.encryptString(message)

    def getInitializationMessage(self):
        return self._loadedAlgorithm.sendFirstMessage()

    # -- Decryption Methods --
    def decrypt(self, message):
        return self._loadedAlgorithm.decryptString(message)

    def giveFirstMessage(self, firstMessage):
        return self._loadedAlgorithm.receiveFirstMessage(firstMessage)