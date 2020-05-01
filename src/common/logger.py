"""Logging
This module contains logging methods common for different packages.
"""

import coloredlogs, logging


def configure_logging(
    level=logging.DEBUG,
    format_str='@%(name)s.%(funcName)s [%(levelname)s]: %(message)s',
    colored=True
):
    """Loggging
    This method configures the log with some useful default values.
    """
    if colored:
        coloredlogs.install(fmt=format_str, level=level)
    else:
        logging.basicConfig(format=format_str, level=level)


class LoggingClass(object):
    """Logger
    This class implements a logging system in order to provide a base clase
    from which others can inherit. This way, they can forget about configuring
    and creating the associated logging objects.
    """

    def __init__(self):
        """Main Constructor"""
        configure_logging()
        self._l = logging.getLogger(self.__class__.__name__)
