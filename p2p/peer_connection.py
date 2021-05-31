import socket
from p2p.connection_tools import serialize_str, deserialize_str, encode_str
import logging
import threading

SIZE_BUFFER_SIZE = 4

class PeerConnection:

    def __init__(self, peer_info, socket):
        self.peer_info = peer_info
        self.socket = socket

    def close(self):
        try:
            self.socket.close()
        except:
            pass

    def get_peer_info(self):
        return self.peer_info

    def set_socket(self, socket):
        self.socket = socket

    def send(self, arg:str):
        try:
            size, data = encode_str(arg)
            self.socket.send(size)
            self.socket.send(data)
        except: 
            logger = logging.getLogger(__name__)
            logger.setLevel(20)
            logger.log("Couldn't connect to: "+self.get_peer_info())

    def receive(self):
        try:
            data_size = self.socket.recv(SIZE_BUFFER_SIZE)
            data_size = int.from_bytes(data_size, byteorder='big')
            #print("data_size: "+str(data_size))
            data = self.socket.recv(data_size)
            print(str(self.get_peer_info()[0]) +":"+str(self.get_peer_info()[1]) + " - data: "+str(deserialize_str(data)))
            if not data:
                return None
            return deserialize_str(data)
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass
        except OSError:
            pass
                                
    def stop_message_listening(self):
        self.listening = False

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

class ClientPeerConnection(PeerConnection):

    def make_connection(self):
        self.socket.connect(self.get_peer_info())
        self.initialize_message_listening()

    def initialize_message_listening(self):
        self.listening = True
        listening_thread = threading.Thread(target=self.listen_to_messages)
        listening_thread.start()
    
    def listen_to_messages(self):
        try:
            while self.listening:
                data = self.receive()
                if data is None:
                    break
        except (ConnectionAbortedError, ConnectionResetError):
            pass
        