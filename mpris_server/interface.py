import logging

from pydbus.generic import signal
from .constants import NAME, INTERFACE as _INTERFACE
from .adapter import Adapter

logger = logging.getLogger(__name__)

# This should be kept in sync with mopidy.internal.log.TRACE_LOG_LEVEL
TRACE_LOG_LEVEL = 5


class Interface:
    INTERFACE = _INTERFACE

    def __init__(self, name: str = NAME, adapter: Adapter = None):
        self.name = name
        self.adapter = adapter

    PropertiesChanged = signal()

    def log_trace(self, *args, **kwargs):
        logger.log(TRACE_LOG_LEVEL, *args, **kwargs)
