from bchain.block import Block
from datetime import datetime
import pytz
from bchain.transactions import Transaction

BASE_TIMEZONE = pytz.timezone('Etc/Greenwich')
GENESIS_BLOCK = Block("0")

class Chain:

    def __init__(self):
        self.blocks = [GENESIS_BLOCK]

    def add_block(self, block:Block):
        if block.previous_hash == self.blocks[-1].hash and datetime.now(BASE_TIMEZONE).time() > block.timestamp > self.blocks[-1].timestamp:
            self.blocks.append(block)

    def remove_last_block(self):
        del self.blocks[-1]

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

    def verify_last_block(self):
        return verify_block(-1)

    def register_transaction(self, transaction):
        return self.blocks[-1].add_transaction(transaction)