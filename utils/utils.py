import sys
import numpy as np
from cycler import cycler
import logging
from functools import update_wrapper

default_cycler = cycler(color=["r", "g", "b", "y"]) + cycler(
    linestyle=["-", "--", ":", "-."]
)

custom_cycler = cycler(color=["c", "m", "y", "k"]) + cycler(lw=[1, 2, 3, 4])

color_cycler = cycler(color=["r", "g", "b", "y", "c", "m", "y", "k"])
linestyle_cycler = cycler(linestyle=["-", "--", ":", "-."])
linewidth_cycler = cycler(lw=[1, 2, 3, 4])

colors = ["r", "g", "b", "y", "c", "m", "y", "k"]


def create_logger(debug=True, stream=True, disable=None):
    if disable is None:
        disable = []

    for module in disable:
        logging.getLogger(module).disabled = True

    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logger = logging.getLogger()

    # Stream
    level = logging.INFO
    if debug:
        level = logging.DEBUG

    logger.setLevel(level)
    logger.handlers = []

    # Stream errors always
    err_stream_handler = logging.StreamHandler(stream=sys.stderr)
    err_stream_handler.setLevel(logging.ERROR)
    logger.addHandler(err_stream_handler)

    # Stream other info only if required
    if stream:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        logger.addHandler(stream_handler)


def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


def spline_data(x, y, new_length=1000, k=3):
    from scipy.interpolate import UnivariateSpline

    # Combine lists into list of tuples
    points = zip(x, y, strict=False)

    # Sort list of tuples by x-value
    points = sorted(points, key=lambda point: point[0])

    # Split list of tuples into two list of x values any y values
    x1, y1 = zip(*points, strict=False)
    new_x = np.linspace(min(x1), max(x1), new_length)
    new_y = UnivariateSpline(x1, y1, k=k)(new_x)
    return new_x, new_y


class LazyProperty(property):
    """Lazy Property class from https://github.com/jackmaney/lazy-property"""

    def __init__(self, method, fget=None, fset=None, fdel=None, doc=None):

        self.method = method
        self.cache_name = "_{}".format(self.method.__name__)

        doc = doc or method.__doc__
        super(LazyProperty, self).__init__(fget=fget, fset=fset, fdel=fdel, doc=doc)

        update_wrapper(self, method)

    def __get__(self, instance, owner):

        if instance is None:
            return self

        if hasattr(instance, self.cache_name):
            result = getattr(instance, self.cache_name)
        else:
            if self.fget is not None:
                result = self.fget(instance)
            else:
                result = self.method(instance)

            setattr(instance, self.cache_name, result)

        return result
