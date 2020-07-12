from threading import Thread

from .client import Client


class ClientsManager(object):
    """
    Simulates different http get requests to a given server.
    """
    def __init__(self, number_of_clients, server_port, server_address='localhost'):
        self.request_url = f'http://{server_address}:{server_port}/'
        self.number_of_clients = number_of_clients
        self.clients_pool = []

    def simulate(self):
        for _ in range(self.number_of_clients):
            client = Client(self.number_of_clients, self.request_url)
            t = Thread(target=client.start_loop)
            t.start()
            self.clients_pool.append(t)

        # Wait for all the threads
        for t in self.clients_pool:
            t.join()
