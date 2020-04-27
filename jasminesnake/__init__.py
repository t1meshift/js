"""Pylint tells me this module should have a docstring.
So here it is.
"""
import logging

__version__ = "0.0.7"
__snake__ = r"""
   _________         _________
  /         \       /         \
 /  /~~~~~\  \     /  /~~~~~\  \
 |  |     |  |     |  |     |  |
 |  |     |  |     |  |     |  |
 |  |     |  |     |  |     |  |         /
 |  |     |  |     |  |     |  |       //
(o  o)    \  \_____/  /     \  \_____/ /
 \__/      \         /       \        /
  |         ~~~~~~~~~         ~~~~~~~~
  ^
"""

LOG_LEVELS = {
    0: {"level": logging.CRITICAL, "format": u"[%(asctime)s] %(message)s"},
    1: {
        "level": logging.ERROR,
        "format": u"[%(asctime)s] [%(levelname)s] %(message)s",
    },
    2: {"level": logging.WARN, "format": u"[%(asctime)s] [%(levelname)s] %(message)s"},
    3: {"level": logging.INFO, "format": u"[%(asctime)s] [%(levelname)s] %(message)s"},
    4: {
        "level": logging.DEBUG,
        "format": u"[%(asctime)s] [%(levelname)s] %(filename)s:%(lineno)d: %(message)s",
    },
}

# TODO: make it usable as a module too
