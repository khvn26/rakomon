import numbers
import warnings

from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from . import settings


__INSTANCE = None

class Monitor(object):
    ERROR_VALUE = '?'

    def __init__(self, scheduler=TornadoScheduler, config=settings.MONITOR_CONFIG.copy(), **kwargs):
        config.update(kwargs)
        self._config = config
        if not issubclass(scheduler, BaseScheduler):
            raise ValueError('Scheduler should be a subclass of BaseScheduler, not %s', repr(scheduler.__name__))
        self._values_store = dict()
        self._scheduler = scheduler()
        self._scheduler.add_listener(self._listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._scheduler.start()

    def _listener(self, event):
        if event.exception:
            self._values_store[event.job_id] = self.ERROR_VALUE
        elif isinstance(event.retval, numbers.Number):
            self._values_store[event.job_id] = round(event.retval, self._config['round_ndigits'])
        elif isinstance(event.retval, str):
            self._values_store[event.job_id] = event.retval

    @property
    def values(self):
        return self._values_store

    def metric(self, func):
        '''
        Use as a decorator, e.g.:
        >>> m = Monitor()
        >>> @m.metric
        >>> def rannum():
        ...    return random.getrandbits(10)
        '''
        self._scheduler.add_job(
            func,
            id=func.__name__,
            trigger='interval',
            seconds=self._config['metric_interval']
        )
        return func


def default(**kwargs):
    global __INSTANCE
    if not __INSTANCE:
        __INSTANCE = Monitor(**kwargs)
    elif kwargs:
        warnings.warn('default() called with kwargs with instance already created; it won\'t be reconfigured', warnings.RuntimeWarning)
    return __INSTANCE
