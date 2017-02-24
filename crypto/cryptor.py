__author__ = 'bensoer'

import types
from crypto.algorithms.algorithminterface import AlgorithmInterface
import logging
logger = logging.getLogger('pychat')

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
        logger.debug("Set Algorithm. Algorithm Name: " + strAlgorithm + " Package Name: " + strAlgorithm.lower())

    '''
    testAlgorithm tests the strAlgorithm string value as to whether it will dynamicaly load a class or not. The tester
    searched in the crypto.algorithms package for the passed in algorithm as all lowercase and then will attempt to
    load the class within the .py file as the passed in algorithm name with its passed in casing. At any point of
    failure this test will fail and throw an error from the dynamic loading functions of at what point failed
    '''
    def testAlgorithm(self):
        logger.debug("Testing Of Algorithms Has Been Deprecated")
        '''
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
            if isinstance(encResponse, bytes):
                print("> Test Encryption Successful")
            else:
                print("> Test Encryption Failed. A Bytes Type Was Not Returned")
                print("> Type Is: %s" % type(encResponse))
                return False
            decResponse = algorithm.decryptString(encResponse)
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
        '''
        return True



    def loadAlgorithm(self):
        print(" -- Loading Algorithm Into System -- ")
        logger.debug("Now Attempting To Dynamically Load Algorithm")
        pkg = __import__('crypto.algorithms.' + self._strPackage, fromlist=[self._strAlgorithm])
        logger.debug("Package Import Successful. Now Attempting Class")
        mod = getattr(pkg, self._strAlgorithm)
        logger.debug("Class Import Successful. Loading Into Attributes")
        self._loadedAlgorithm = mod(self._arguments)

    def setArguments(self, arguments):
        logger.debug("Setting System Arguments As Attribute")
        self._arguments = arguments

    # -- Encryption Methods --
    # encrypt will take the message that arrives as a string and then return them as bytes
    def encrypt(self, message):
        logger.debug("Passing Message To Loaded Algorithm To Encrypt")
        return self._loadedAlgorithm.encryptString(message)

    def getInitializationMessage(self):
        logger.debug("Retrieving First Message to Send")
        return self._loadedAlgorithm.sendFirstMessage()

    # -- Decryption Methods --
    # decrypt will take a message that is in bytes and then return them as a string
    def decrypt(self, message):
        logger.debug("Passing Message To Loaded Algorithm To Decrypt")
        return self._loadedAlgorithm.decryptString(message)

    def giveFirstMessage(self, firstMessage):
        logger.debug("Passing First Received Message To The Algorithm")
        return self._loadedAlgorithm.receiveFirstMessage(firstMessage)
