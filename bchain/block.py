from datetime import datetime
import pytz
from bchain.bchain_tools import *

BASE_TIMEZONE = pytz.timezone('Etc/Greenwich')
MAX_TRANSACTION_COUNT = 5

class Block:

    def __init__(self, previous_hash:str):
        self.transactions = []
        self.previous_hash = previous_hash
        self.timestamp = datetime.now(BASE_TIMEZONE).time()

    def get_hash(self):
        self.hash = hash_sha256([self.previous_hash, get_transactions_hashable(self.transactions),str(self.timestamp)]) 
        return self.hash
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.get_hash()
        if len(self.transactions) >= MAX_TRANSACTION_COUNT:
            return False
        else:
            return True

    def to_string(self,index):
        output = "\tBlock nr"+str(index)
        for transaction in self.transactions:
            output+='\n\t\t'+transaction.to_string()
        return output

    def to_string_of_hashes(self, index):
        return '\tBlock nr'+str(index)+': '+self.previous_hash + '\n\t\t' + self.hash

    def is_in_block(self, transaction):
        for t in self.transactions:
            if transaction.compare(t):
                return True
        return False

    def is_full(self):
        return len(self.transactions)>=MAX_TRANSACTION_COUNT
