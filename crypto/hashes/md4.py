from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import MD4


class MD4(HashInterface):

    def hashString(self, stringMessage):
        md4 = MD4.new()
        md4.update(stringMessage)
        return md4.hexdigest()
