import random
import time
import redis
import signal
import requests

from consts import *


class Client(object):
    FIRST_CLIENT_IDENTIFIER = 1
    MIN_SLEEP_BETWEEN_REQUESTS = 1
    MAX_SLEEP_BETWEEN_REQUESTS = 3

    def __init__(self, max_client_id, request_url):
        self.client_id = random.randint(self.FIRST_CLIENT_IDENTIFIER, max_client_id)
        self.request_url = request_url
        self.db = redis.Redis()

    def start_loop(self):
        """
        Send requests as long as signal is not received
        """
        signal_value = None
        while signal_value != signal.SIGINT.value:
            requests.get(self.request_url, params={CLIENT_PARAM_NAME: self.client_id})
            time_to_sleep = random.randint(self.MIN_SLEEP_BETWEEN_REQUESTS, self.MAX_SLEEP_BETWEEN_REQUESTS)
            time.sleep(time_to_sleep)

            # Set current signal value
            signal_value = int(self.db.get(SERVER_SIGNAL_KEY_NAME))
