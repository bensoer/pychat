from crypto.hashes.hashinterface import HashInterface
from Crypto.Hash import MD2


class MD2(HashInterface):

    def hashString(self, stringMessage):
        md2 = MD2.new()
        md2.update(stringMessage)
        return md2.hexdigest()
