__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA224 as libsha224


class SHA224(HashInterface):

    def hashString(self, stringMessage):
        sha224 = libsha224.new()
        sha224.update(stringMessage.encode())
        return sha224.digest()

    def getDigestSize(self):
        return 28

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes
