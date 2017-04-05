import tornado.ioloop
import tornado.web

from . import settings, monitor


class MonitorHandler(tornado.web.RequestHandler):
    def initialize(self, mon):
        self.monitor = mon

    def get(self):
        self.write(self.monitor.values)


def run(handler=MonitorHandler, mon=monitor.default(), config=settings.ENDPOINT_CONFIG.copy(), **kwargs):
    config.update(kwargs)

    app = tornado.web.Application((
        (config['url_path'], handler, dict(monitor=mon)),
    ))
    app.listen(config['port'], address=config['address'])

    tornado.ioloop.current().start()
