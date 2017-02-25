from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA


class SHA1(HashInterface):

    def hashString(self, stringMessage):
        sha1 = SHA.new()
        sha1.update(stringMessage)
        return sha1.hexdigest()
