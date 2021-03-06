![PyPI version](https://img.shields.io/pypi/v/rakomon.svg)

rakomon is designed for simplest, most stupid monitoring tasks when logging, caching and other features of advanced monitoring solutions are not required.
It encapsulates some of tornado and apscheduler functionality to run simple tasks periodically, store results in memory and serve them in application/json.
You can use both monitor and endpoint modules to serve your metrics automagically, or instantiate the `monitor.Monitor` class on your own to use it however you see fit. 

### Disclaimer: though I use this code in my projects, it's rather raw. I set up this repository mainly to learn how to maintain an open-source project. It's up to you to evaluate if rakomon is production ready. 

# Dependencies
rakomon is Python 3 only. It also requires tornado and apscheduler.

# Installation
Use pip:
```sh
$ pip install rakomon
```
Or clone repository to your machine and use easy_install:
```sh
$ easy_install setup.py
```

# Basic usage
rakomon is ready out of the box. All you need is get default `Monitor` instance, then define your metrics as functions and decorate them with the `Monitor.metric` decorator.
A metric function should return either a number or a string. Iterables support is planned for future. 
After you define your metrics, call `endpoint.run()` to launch a simple tornado server to serve them. It will bind to port 80 on localhost by default.
```python
import psutil

from rakomon import monitor, endpoint

m = monitor.default()

@m.metric
def cpu():
    return psutil.cpu_percent(interval=1)

@m.metric
def ram():
    return psutil.virtual_memory().percent

endpoint.run()
```
```sh
$ curl http://127.0.0.1/rakomon
{"cpu": 2.3, "ram": 33.1}
```

# Configuration
Both `monitor.Monitor` and `endpoint.run` are configurable. You can pass configuration as keyword arguments. If kwargs are not provided, rakomon uses default values.

## monitor.Monitor
* `scheduler` - a class that inherits from `apscheduler.schedulers.base.BaseScheduler`. Useful when you want to utilize Monitor on its own, without the included endpoint. See [apscheduler docs](http://apscheduler.readthedocs.io) for more info on schedulers. Defaults to `TornadoScheduler`. 
* `metric_interval` - number of idle seconds between metric runs. Defaults to `5`.
* `round_ndigits` - number of digits when rounding metric values. Naturally, applies to number values only. Defaults to `2`.

## endpoint.run
* `monitor` - an instance of `monitor.Monitor`. Defaults to `monitor.default()`.
* `address` - address to bind the tornado endpoint to. Defaults to `'127.0.0.1'`.
* `port` - port to bind the tornado endpoint to. Defaults to `80`.
* `url_path` - defaults to `r'/rakomon'`.
