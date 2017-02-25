from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import SHA384


class SHA384(HashInterface):

    def hashString(self, stringMessage):
        sha384 = SHA384.new()
        sha384.update(stringMessage)
        return sha384.hexdigest()
