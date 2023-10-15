from __future__ import annotations

import logging
from abc import ABC
from functools import wraps
from typing import ClassVar, Final, Self, TYPE_CHECKING

from pydbus.generic import signal

from ..base import Interfaces, NAME, P
from ..enums import Method


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
  INTERFACE: ClassVar[Interfaces] = Interfaces.Root

  PropertiesChanged: Final[signal] = signal()

  def __init__(
    self,
    name: str = NAME,
    adapter: MprisAdapter | None = None
  ):
    self.name = name
    self.adapter = adapter
