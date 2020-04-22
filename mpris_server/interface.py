import logging
from abc import ABC

from pydbus.generic import signal
from .base import NAME, INTERFACE as _INTERFACE

logger = logging.getLogger(__name__)

TRACE_LOG_LEVEL = 5


class MprisInterface(ABC):
    INTERFACE = _INTERFACE

    def __init__(self,
                 name: str = NAME,
                 adapter: 'MprisAdapter' = None):
        self.name = name
        self.adapter = adapter

    PropertiesChanged = signal()

    def log_trace(self, *args, **kwargs):
        logger.log(TRACE_LOG_LEVEL, *args, **kwargs)


