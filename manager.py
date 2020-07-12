import redis
import signal
from multiprocessing import Process

from server.server import Server
from client.clients_manager import ClientsManager
from consts import *


class Manager(object):
    """
    Represents the manager of the entire program
    """
    server_process = None
    client_manager_process = None

    def __init__(self, num_of_clients, server_port, server_address=SERVER_NAME):
        """
        :param num_of_clients: Number of clients to create
        :param server_port: The port that this server should be listened to
        :param server_address: Address may be either an IP address or hostname. If it's a hostname,
        the server will listen on all IP addresses associated with the name.
        """
        self.db = redis.Redis()
        self.build_server(server_address, server_port)
        self.build_client_manager(num_of_clients, server_address, server_port)

    def build_server(self, server_address, server_port):
        """
        Initial a new server object
        """
        server = Server(server_address, server_port)
        p = Process(target=server.start, daemon=True)
        self.server_process = p

    def build_client_manager(self, num_of_clients, server_address, server_port):
        """
        Initial a new client manager object
        """
        client_manager = ClientsManager(num_of_clients, server_port, server_address)
        p = Process(target=client_manager.simulate, daemon=True)
        self.client_manager_process = p

    def start(self):
        """
        Start server and client activity
        """
        # Initial exit signal to a default value, this will be changed later in case of an exit
        self.db.set(SERVER_SIGNAL_KEY_NAME, 0)
        # Start server and client manager
        self.server_process.start()
        self.client_manager_process.start()

    def stop(self):
        """
        Stops gracefully server and client
        """
        self.db.set(SERVER_SIGNAL_KEY_NAME, signal.SIGINT.value)
        # Wait for exit
        self.server_process.join()
        self.client_manager_process.join()
