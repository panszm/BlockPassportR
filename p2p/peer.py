import threading
import socket
from p2p.connection_tools import *
from p2p.peer_connection import ServerPeerConnection, ClientPeerConnection
import logging

class PeerInfo:

    def __init__(self, host :str, port:int):
        self.host = host
        self.port = port
        self.server_alive = False

    def get_info(self):
        return (self.host,self.port)

class Peer:

    def __init__(self, peer_info: PeerInfo):
        self.peer_info = peer_info
        self.server_peer_connections = []
        self.client_peer_connections = []

    def get_info(self):
        return self.peer_info.get_info()

    def add_client_peer_connection(self, peer_connection: ClientPeerConnection):
        self.client_peer_connections.append(peer_connection)

    def make_connection(self, peer_info: PeerInfo):
        if not validate_peer(peer_info):
            logger = logging.getLogger(__name__)
            logger.setLevel(30)
            logger.log("Unathorized connection attemp to: "+peer_info)
            return
            
        for connection in self.client_peer_connections:
            if connection.get_peer_info() == peer_info:
                break
        else:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_peer_client_connection = ClientPeerConnection(peer_info,client_socket)
            self.client_peer_connections.append(new_peer_client_connection)
            new_peer_client_connection.make_connection()

    def broadcast_message(self,mssg:str):
        for peer_connection in self.client_peer_connections:
            peer_connection.send(mssg)

    def add_server_peer_connection(self, peer_connection: ServerPeerConnection):
        self.server_peer_connections.append(peer_connection)

    def start_listening(self):
        self.server_alive = True
        self.server_thread = threading.Thread(target=self.listening)
        self.server_thread.start()

    def stop_listening(self):
        self.server_alive = False
        for conn in self.server_peer_connections:
            conn.stop_message_listening()
        for conn in self.client_peer_connections:
            conn.stop_message_listening()

    def listening(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.get_info())
        self.server_socket.listen()
        while self.server_alive:
            try:
                connection, address = self.server_socket.accept()
                if validate_peer(address):
                    for peer_connection in self.server_peer_connections:
                        if address == peer_connection.get_peer_info():
                            peer_connection.stop_message_listening()
                            peer_connection.set_socket(connection)
                            peer_connection.initialize_message_listening()
                            break
                    else:
                        new_peer_connection = ServerPeerConnection(address,connection)
                        new_peer_connection.initialize_message_listening()
                        self.add_server_peer_connection(new_peer_connection)
                else:
                    logger = logging.getLogger(__name__)
                    logger.setLevel(30)
                    logger.log("Unathorized connection attemp from: "+address)
            except OSError:
                print("Forcibly shut-down: "+str(self.get_info()))

    def stop(self):
        self.server_socket.close()
        self.stop_listening()
        for conn in self.client_peer_connections:
            conn.stop_message_listening()
            conn.close()
        for conn in self.server_peer_connections:
            conn.stop_message_listening()
            conn.close()