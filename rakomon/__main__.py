import sys

from tornado.web import Application
import tornado.ioloop

from rakomon.monitor import monitor
from endpoint import RakomonHandler


def _get_app(monitor=monitor):
    return Application((
        (r'/rakomon', RakomonHandler, dict(monitor=monitor))
    ))


if __name__ == '__main__':
    if 'start' in sys.argv:
