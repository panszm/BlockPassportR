from bchain.block import Block
from datetime import datetime
import pytz
from bchain.transactions import Transaction
from ecdsa import SigningKey
import ast

BASE_TIMEZONE = pytz.timezone('Etc/Greenwich')
GENESIS_BLOCK = Block("0")

class Chain:

    def __init__(self):
        self.blocks = [GENESIS_BLOCK]
        self.sk = SigningKey.generate()
        self.vk = self.sk.get_verifying_key()

    def add_block(self, block:Block):
        if (block.previous_hash == self.blocks[-1].hash or len(self.blocks)<2) and datetime.now(BASE_TIMEZONE).time() >= block.timestamp >= self.blocks[-1].timestamp:
            print("EQUAL \n\t"+self.blocks[-1].hash+"\n\t"+block.previous_hash)
            print(self.blocks[-1].to_string(-1))
            print(block.to_string(0))
            self.blocks.append(block)
            return True
        else:
            print("UNEQUAL \n\t"+self.blocks[-1].hash+"\n\t"+block.previous_hash)
            print(self.blocks[-1].to_string(-1))
            print(block.to_string(0))
            return False
        # elif self.blocks[-1].is_full():
        #     self.add_new_block()

    def add_new_block(self):
        block = Block(self.blocks[-1].hash)
        self.add_block(block)
        return block

    def remove_last_block(self):
        self.blocks.pop()

    def verify_chain(self):
        for index in range(1,len(self.blocks)):
            if not verify_block(index):
                return False
        return True

    def verify_block(self, index):
        if index==0 or len(self.blocks)==1:
            return True
        else:
            if self.blocks[index-1].get_hash() == self.blocks[index].previous_hash and datetime.now(BASE_TIMEZONE).time() > self.blocks[index].timestamp > self.blocks[index-1]:
                return True
        return False

    def verify_last_block(self):
        return self.verify_block(-1)

    def register_transaction(self, transaction):
        return self.blocks[-1].add_transaction(transaction)

    def to_string(self):
        output = "Chain: "
        for index, block in enumerate(self.blocks):
            output+='\n'+block.to_string(index)
        return output

    def is_in_chain(self,transaction):
        for b in self.blocks:
            if b.is_in_block(transaction):
                return True
        return False