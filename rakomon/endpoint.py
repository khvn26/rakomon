import tornado.ioloop
import tornado.web

from . import settings, monitor


class MonitorHandler(tornado.web.RequestHandler):
    def initialize(self, monitor):
        self.monitor = monitor.default()

    def get(self):
        self.write(self.monitor.values)


def run(handler=MonitorHandler, monitor=monitor, config=settings.ENDPOINT_CONFIG.copy(), **kwargs):
    config.update(kwargs)

    app = tornado.web.Application((
        (config['url_path'], handler, dict(monitor=monitor))
    ))
    app.listen(config['port'], address=config['address']')

    torando.ioloop.current().start()
