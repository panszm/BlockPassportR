from bchain.node import Node

class CommandHandler:

    def __init__(self, node: Node):
        self.node = node

    def handle_command(self, command_code:int, obj, peer_info):
        command_function = self.switch_command(command_code)
        if command_function is not None:
            command_function(obj,peer_info)

    def switch_command(self, command_code:int):
        switch = {
            11:self.c_chain_length,
            12:self.c_chain_request,
            13:self.c_chain_pass,

            21:self.c_block_create,

            31:self.c_passport_create,
            32:self.c_passport_edit,

            41:self.c_border_crossing,

            51:self.c_visa_create
        }
        return switch.get(command_code, None)

    def c_chain_length(self, obj,peer_info):
        pass
    
    def c_chain_request(self, obj,peer_info):
        pass
    
    def c_chain_pass(self, obj,peer_info):
        pass
    
    def c_block_create(self, obj,peer_info):
        pass
    
    def c_passport_create(self, obj,peer_info):
        pass
    
    def c_passport_edit(self, obj,peer_info):
        pass
    
    def c_border_crossing(self, obj,peer_info):
        pass
    
    def c_visa_create(self, obj,peer_info):
        pass