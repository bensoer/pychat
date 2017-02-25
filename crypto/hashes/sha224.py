from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA224


class SHA224(HashInterface):

    def hashString(self, stringMessage):
        sha224 = SHA224.new()
        sha224.update(stringMessage)
        return sha224.hexdigest()
