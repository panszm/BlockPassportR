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
        self.hash = hash_sha256(self.previous_hash, get_transactions_merkle_root(self.transactions),str(self.timestamp))
        return self.hash
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        if len(self.transactions) == MAX_TRANSACTION_COUNT:
            return False
        else:
            return True