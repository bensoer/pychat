__author__='bensoer'
from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA512 as libsha512


class SHA512(HashInterface):

    def hashString(self, stringMessage):
        sha512 = libsha512.new()
        sha512.update(stringMessage.encode())
        return sha512.digest()


    def getDigestSize(self):
        return libsha512.digest_size

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes

