from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA512


class SHA512(HashInterface):

    def hashString(self, stringMessage):
        sha512 = SHA512.new()
        sha512.update(stringMessage)
        return sha512.hexdigest()
