__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA256 as libsha256


class SHA256(HashInterface):

    def hashString(self, stringMessage):
        sha256 = libsha256.new()
        sha256.update(stringMessage.encode())
        return sha256.digest()

    def getDigestSize(self):
        return 32

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes

