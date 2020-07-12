import redis
import tornado.web


class ServerApp(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(ServerApp, self).__init__(*args, **kwargs)
        self._db = None

    @property
    def db(self):
        if self._db is None:
            self._db = redis.Redis()
        return self._db
