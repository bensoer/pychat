__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import HMAC as libhmac
from Crypto.Hash import SHA
from Crypto.Hash import SHA224
from Crypto.Hash import SHA256
from Crypto.Hash import SHA384
from Crypto.Hash import SHA512
from Crypto.Hash import MD5
from tools.argparcer import ArgParcer
from enum import Enum

class DIGESTMODEENUM(Enum):
    SHA1 = 1,
    SHA224 = 2,
    SHA256 = 3,
    SHA384 = 4,
    SHA512 = 5,
    MD5 = 6

class HMAC(HashInterface):

    password = ""
    digestMode = ""
    digestModeEnum = DIGESTMODEENUM.SHA1

    def __init__(self, arguments):
        self.password = ArgParcer.getValue(arguments, "-hk")
        self.digestMode = ArgParcer.getValue(arguments, "-hm")  # this parameter is optional
        if self.password == "":
            raise AttributeError("HMAC Requires a Password Parameter -hk")
        if self.digestMode != "":
            try:
                self.digestModeEnum = DIGESTMODEENUM[self.digestMode]
            except:
                raise AttributeError("The Passed In Digest Mode Is Invalid. Valid Digest Modes Are SHA1, SHA224, "
                                     "SHA256, SHA384, SHA512 and MD5. Default is SHA1 if no parameter supplied")

    def hashString(self, stringMessage):
        if self.digestModeEnum == DIGESTMODEENUM.SHA1:
            hmac = libhmac.new(self.password.encode(), digestmod=SHA)
            hmac.update(stringMessage.encode())
            return hmac.digest()
        elif self.digestModeEnum == DIGESTMODEENUM.SHA224:
            hmac = libhmac.new(self.password.encode(), digestmod=SHA224)
            hmac.update(stringMessage.encode())
            return hmac.digest()
        elif self.digestModeEnum == DIGESTMODEENUM.SHA256:
            hmac = libhmac.new(self.password.encode(), digestmod=SHA256)
            hmac.update(stringMessage.encode())
            return hmac.digest()
        elif self.digestModeEnum == DIGESTMODEENUM.SHA384:
            hmac = libhmac.new(self.password.encode(), digestmod=SHA384)
            hmac.update(stringMessage.encode())
            return hmac.digest()
        elif self.digestModeEnum == DIGESTMODEENUM.SHA512:
            hmac = libhmac.new(self.password.encode(), digestmod=SHA512)
            hmac.update(stringMessage.encode())
            return hmac.digest()
        elif self.digestModeEnum == DIGESTMODEENUM.MD5:
            hmac = libhmac.new(self.password.encode(), digestmod=MD5)
            hmac.update(stringMessage.encode())
            return hmac.digest()

    def getDigestSize(self):
        if self.digestModeEnum == DIGESTMODEENUM.SHA1:
            return SHA.digest_size
        elif self.digestModeEnum == DIGESTMODEENUM.SHA224:
            return SHA224.digest_size
        elif self.digestModeEnum == DIGESTMODEENUM.SHA256:
            return SHA256.digest_size
        elif self.digestModeEnum == DIGESTMODEENUM.SHA384:
            return SHA384.digest_size
        elif self.digestModeEnum == DIGESTMODEENUM.SHA512:
            return SHA512.digest_size
        elif self.digestModeEnum == DIGESTMODEENUM.MD5:
            return MD5.digest_size

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes
