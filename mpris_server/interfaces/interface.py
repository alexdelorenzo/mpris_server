from __future__ import annotations

from abc import ABC
from functools import wraps
from typing import ClassVar, Optional, Self, TYPE_CHECKING
import logging

from pydbus.generic import signal

from ..base import Method, NAME, P, ROOT_INTERFACE
from ..types import Final

if TYPE_CHECKING:
  from ..adapters import MprisAdapter


def log_trace(method: Method) -> Method:
  @wraps(method)
  def new_method(self: Self, *args: P.args, **kwargs: P.kwargs):
    name = method.__name__
    logging.debug(f'{self.INTERFACE}.{name}() called.')

    return method(self, *args, **kwargs)

  return new_method


class MprisInterface(ABC):
  INTERFACE: ClassVar[str] = ROOT_INTERFACE

  PropertiesChanged: Final[signal] = signal()

  def __init__(
    self,
    name: str = NAME,
    adapter: Optional[MprisAdapter] = None
  ):
    self.name = name
    self.adapter = adapter
