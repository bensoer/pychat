__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import MD5 as libmd5


class MD5(HashInterface):

    def hashString(self, stringMessage):
        md5 = libmd5.new()
        md5.update(stringMessage.encode())
        return md5.digest()

    def getDigestSize(self):
        return 16

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes
