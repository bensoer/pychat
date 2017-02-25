from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA256


class SHA256(HashInterface):

    def hashString(self, stringMessage):
        sha256 = SHA256.new()
        sha256.update(stringMessage)
        return sha256.hexdigest()
