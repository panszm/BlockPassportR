import pickle

def serialize_str(arg:str):
    return arg.encode()

def encode_str(arg:str):
    serialized = serialize_str(arg)
    msg_len = int(len(serialized))
    msg_len = msg_len.to_bytes(6,byteorder='big')
    return (msg_len,serialized)

def deserialize_str(arg:bytearray):
    return arg.decode()

def validate_peer(peer_address) -> bool:
    return True

def serialize_obj(obj):
    return pickle.dumps(obj)

def deserialize_obj(serialized_obj):
    return pickle.loads(serialized_obj)

def encode_command(command_code, obj):
    serialized_obj = serialize_obj(obj)
    data_size = int(serialized_obj.__sizeof__())
    data_size = data_size.to_bytes(4,byteorder='big')
    command_code = command_code.to_bytes(2,byteorder='big')
    return (data_size, command_code, serialized_obj)
    