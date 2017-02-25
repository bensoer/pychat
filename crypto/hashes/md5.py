from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import MD5


class MD5(HashInterface):

    def hashString(self, stringMessage):
        md5 = MD5.new()
        md5.update(stringMessage)
        return md5.hexdigest()
