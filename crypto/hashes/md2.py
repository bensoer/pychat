from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import MD2 as libmd2


class MD2(HashInterface):

    def hashString(self, stringMessage):
        md2 = libmd2.new()
        md2.update(stringMessage.encode())
        return md2.digest()

    def getDigestSize(self):
        return 16

    def isValidHash(self, stringMessage, hashBytes):
        return self.hashString(stringMessage) == hashBytes
