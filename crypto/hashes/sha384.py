__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA384 as libsha384


class SHA384(HashInterface):

    def hashString(self, stringMessage):
        sha384 = libsha384.new()
        sha384.update(stringMessage.encode())
        return sha384.digest()

    def getDigestSize(self):
        return libsha384.digest_size

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes

