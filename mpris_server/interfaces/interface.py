from __future__ import annotations
from typing import Optional
from abc import ABC
import logging

from pydbus.generic import signal

from ..base import NAME, INTERFACE as MPRIS_INTERFACE
from ..types import Final


TRACE_LOG_LEVEL: Final[int] = logging.DEBUG


class MprisInterface(ABC):
    INTERFACE: Final[str] = MPRIS_INTERFACE

    PropertiesChanged = signal()

    def __init__(
      self,
      name: str = NAME,
      adapter: Optional['MprisAdapter'] = None
    ):
        self.name = name
        self.adapter = adapter

    def log_trace(self, *args, **kwargs):
        logging.log(TRACE_LOG_LEVEL, *args, **kwargs)
