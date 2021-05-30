import pickle

def serialize_str(arg:str):
    return pickle.dumps(arg)

def deserialize_str(arg:str):
    return pickle.loads(arg)

def validate_peer(peer_address) -> bool:
    return True