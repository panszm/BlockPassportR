import hashlib
import copy

def hash_sha256(args):
    hash_function = hashlib.sha256()
    for arg in args:
        hash_function.update(arg)
    return hash_function.digest()

def get_transactions_merkle_root(transactions):
    result = copy.deepcopy(transactions)
    
    while len(result>1):
        for index in range(0,len(result)-len(result)%2,2):
            result[index] = hash_sha256([result[index].to_string(), result[index+1].to_string()])
        for index in range(len(result)-1-len(result)%2,-1,-2):
            del result[index]

    return result[0]