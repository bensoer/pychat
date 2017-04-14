__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import MD4 as libmd4


class MD4(HashInterface):

    def hashString(self, stringMessage):
        md4 = libmd4.new()
        md4.update(stringMessage.encode())
        return md4.digest()

    def getDigestSize(self):
        return libmd4.digest_size

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes