import hashlib
import copy
import pickle

def hash_sha256(args):
    args = str(args).encode()
    hash_function = hashlib.sha256()
    hash_function.update(args)
    # for arg in args:
    #     hash_function.update(arg)
    return str(hash_function.hexdigest())

def get_transactions_merkle_root(transactions):
    result = copy.deepcopy(transactions)
    
    while len(result)>1:
        for index in range(0,len(result)-len(result)%2,2):
            result[index] = hash_sha256([str(result[index]), str(result[index+1])])
        for index in range(len(result)-1-len(result)%2,-1,-2):
            del result[index]

    return result[0]

def serialize_obj(obj):
    return pickle.dumps(obj)

def deserialize_obj(serialized_obj):
    return pickle.loads(serialized_obj)