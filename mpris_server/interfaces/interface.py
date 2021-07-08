from __future__ import annotations
from typing import Optional, Callable, Any
from functools import wraps
from abc import ABC
import logging

from pydbus.generic import signal

from ..base import NAME, INTERFACE as MPRIS_INTERFACE
from ..types import Final


TRACE_LOG_LEVEL: Final[int] = logging.DEBUG


Method = Callable[[Any, ...], Optional[Any]]


def log_trace(method: Method) -> Method:
  @wraps(method)
  def new_method(self, *args, **kwargs):
    name = method.__name__
    logging.debug(f'{self.INTERFACE}.{name}() called.')

    return method(self, *args, **kwargs)
  return new_method


class MprisInterface(ABC):
  INTERFACE: Final[str] = MPRIS_INTERFACE

  PropertiesChanged: Final[signal] = signal()

  def __init__(
    self,
    name: str = NAME,
    adapter: Optional['MprisAdapter'] = None
  ):
    self.name = name
    self.adapter = adapter

  def log_trace(self, *args, **kwargs):
    logging.log(TRACE_LOG_LEVEL, *args, **kwargs)
