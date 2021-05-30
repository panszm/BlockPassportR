import socket
from p2p.connection_tools import serialize_str, deserialize_str
import logging
import threading

class PeerConnection:

    def __init__(self, peer_info, socket):
        self.peer_info = peer_info
        self.socket = socket

    def get_peer_info(self):
        return self.peer_info

    def set_socket(self, socket):
        self.socket = socket

    def send(self, arg:str):
        try:
            self.socket.sendall(serialize_str(arg))
        except: 
            logger = logging.getLogger(__name__)
            logger.setLevel(20)
            logger.log("Couldn't connect to: "+self.peer_info.get_info())

    def receive(self):
        data = self.socket.recv(4096)
        if not data:
            return None
        return deserialize_str(data)
                                
class ServerPeerConnection(PeerConnection):

    def initialize_message_listening(self):
        self.listening = True
        listening_thread = threading.Thread(target=self.listen_to_messages)
        listening_thread.start()

    def listen_to_messages(self):
        while self.listening:
            data = self.receive()
            if data is None:
                break
            self.socket.sendall(serialize_str(data))
    
    def stop_message_listening(self):
        self.listening = False

class ClientPeerConnection(PeerConnection):

    def make_connection(self):
        self.socket.connect(self.peer_info)
        self.initialize_message_listening()

    def initialize_message_listening(self):
        self.listening = True
        listening_thread = threading.Thread(target=self.listen_to_messages)
        listening_thread.start()
    
    def listen_to_messages(self):
        while self.listening:
            data = self.receive()
            if data is None:
                break
            self.socket.sendall(serialize_str(data))