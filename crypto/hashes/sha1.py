__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA


class SHA1(HashInterface):

    def hashString(self, stringMessage):
        sha1 = SHA.new()
        sha1.update(stringMessage.encode())
        return sha1.digest()

    def getDigestSize(self):
        return 20

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes

