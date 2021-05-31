from bchain.block import Block
from datetime import datetime
import pytz

BASE_TIMEZONE = pytz.timezone('Etc/Greenwich')

class Chain:

    def __init__(self):
        self.blocks = []

    def add_block(self, block:Block):
        if block.previous_hash == self.blocks[-1].hash and datetime.now(BASE_TIMEZONE).time() > block.timestamp > self.blocks[-1].timestamp:
            self.blocks.append(block)

    def verify_chain(self):
        for index in range(1,len(self.blocks)):
            if not verify_block(index):
                return False
        return True

    def verify_block(self, index):
        if index==0:
            return True
        else:
            if self.blocks[index-1].get_hash() == self.blocks[index].previous_hash and datetime.now(BASE_TIMEZONE).time() > self.blocks[index].timestamp > self.blocks[index-1]:
                return True
        return False
