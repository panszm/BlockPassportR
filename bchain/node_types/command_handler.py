from bchain.node import Node

class CommandHandler:

    def __init__(self, node: Node):
        self.node = node

    def handle_command(self, command_code:int, obj):
        print("DOIN' MY BEST 'KAY??")