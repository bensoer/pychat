__author__ = 'bensoer'
from Crypto import Random
from enum import Enum


class MODE(Enum):
    CBC = 1,
    ECB = 2


class ModeHandler:

    mode = MODE.ECB
    data = bytearray()

    def __init__(self, mode, blocksize):
        self.mode = mode

        if mode == MODE.CBC:
            self.data.append(self._generateIV(blocksize))

    def _generateIV(self, blocksize):
        return Random.new().read(blocksize)

    def addBlock(self, blockBytes):
        if self.mode == MODE.CBC:
            self.data[0] = self.data[0] ^ blockBytes
        elif self.mode == MODE.ECB:
            for byte in blockBytes:
                if byte != b'\x00':
                    self.data.append(byte)
        else:
            raise AttributeError("Unknown Mode Set. Can't Determine How To Prepare Next Block")

    def getResultForMode(self):
        return self.data

    def clearData(self):
        self.data = bytearray()
