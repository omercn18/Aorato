import logging
import redis
import signal

import tornado.ioloop
import tornado.web
import tornado.httpserver

from server.urls import ROUTES
from server.server_app import ServerApp
from consts import *


class Server(object):
    def __init__(self, address, port, num_processes=1):
        """
        :param address: An address to bind to
        :param port: The server port
        :param num_processes: Number of child processes that the server should be deployed to.
        If num_processes is ``None`` or <= 0, we detect the number of cores
        available on this machine and fork that number of child processes.
        num_processes uses process.fork and therefore works in unix environment only,
        # TODO: Use a different load balancer that would work in any operation system.
        """
        self.app = ServerApp(ROUTES)
        self.address = address
        self.port = port
        self.num_processes = num_processes

    def start(self):
        """
        Start the server binding
        """
        logging.info("Starting the server")
        # Initial server
        server = tornado.httpserver.HTTPServer(self.app)
        server.bind(self.port, address=self.address)
        server.start(self.num_processes)
        # Add signal checker
        tornado.ioloop.PeriodicCallback(self.try_exit, 1000).start()
        # Start event loop
        tornado.ioloop.IOLoop.current().start()

    def try_exit(self):
        signal_value = int(self.app.db.get(SERVER_SIGNAL_KEY_NAME))
        if signal_value == signal.SIGINT.value:
            tornado.ioloop.IOLoop.current().stop()
