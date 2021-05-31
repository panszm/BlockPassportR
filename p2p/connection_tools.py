
def serialize_str(arg:str):
    return arg.encode()#bytearray(arg, encoding='utf-8')

def encode_str(arg:str):
    serialized = serialize_str(arg)
    msg_len = int(len(serialized))#.__sizeof__())
    msg_len = msg_len.to_bytes(4,byteorder='big')
    # print(msg_len,serialized)
    return (msg_len,serialized)

def deserialize_str(arg:bytearray):
    return arg.decode()

def validate_peer(peer_address) -> bool:
    return True