import tornado.web
import time
import pickle

from consts import *
from exceptions.threshold_reached_exception import ThresholdReachedException


class MainHandler(tornado.web.RequestHandler):
    FRAME_DURATION_IN_SEC = 5
    MAX_REQUESTS_PER_FRAME = 5

    FAILURE_STATUS_CODE = 500
    OK_STATUS_CODE = 200
    SERVER_UNAVAILABLE_STATUS_CODE = 503

    @tornado.web.asynchronous
    def get(self):
        """
        Override the get method, so each request will be handled in this way
        :return:
        """
        try:
            client_id = self.get_argument(CLIENT_PARAM_NAME)
            client_id_num = int(client_id)
            if client_id_num < 1:
                raise ValueError()
        except tornado.web.MissingArgumentError:
            self.send_error(reason="Parameter %s is required" % CLIENT_PARAM_NAME)
        except ValueError:
            self.send_error(reason="Parameter %s is an invalid positive int value" % CLIENT_PARAM_NAME)

        # Already got an error, exit..
        if self.get_status() == self.FAILURE_STATUS_CODE:
            return

        # TODO: Add a lock to prevent race conditions
        client_old_settings = self.application.db.get(client_id)
        try:
            new_settings = self.handle_request(client_old_settings)
            self.application.db.set(client_id, pickle.dumps(new_settings))
            self.write("Current frame counter: %d" % new_settings[0])
            self.set_status(self.OK_STATUS_CODE)
        except ThresholdReachedException:
            self.set_status(self.SERVER_UNAVAILABLE_STATUS_CODE)
        self.finish()

    def handle_request(self, previous_settings):
        """
        Handle a request of a client, which already had a request before
        :param previous_settings: The current saved settings of this client id.
        e.g: (NUMBER_OF_REQUESTS_IN_FRAME, FIRST_REQUEST_TIME_IN_FRAME)
        :type previous_settings: Pickle object of tuple
        :return:
        """
        current_time = time.time()
        initialed_settings = (1, current_time)

        # There is no previous data about this client id, initialize it
        if previous_settings is None:
            return initialed_settings

        requests_counter, frame_start_time = pickle.loads(previous_settings)

        # This request is out of the current frame, so start a new frame
        if (current_time - frame_start_time) > self.FRAME_DURATION_IN_SEC:
            return initialed_settings

        # Request is in the current frame, but threshold reached
        if requests_counter == self.MAX_REQUESTS_PER_FRAME:
            raise ThresholdReachedException()

        # Request is in the current frame and client hasn't reached the threshold
        return requests_counter + 1, frame_start_time
