from __future__ import annotations

import logging
from abc import ABC
from functools import wraps
from typing import ClassVar, Final, TYPE_CHECKING

from pydbus.generic import signal

from ..base import Interfaces, Method, NAME


if TYPE_CHECKING:
  from ..adapters import MprisAdapter


log = logging.getLogger(__name__)


def log_trace[S, **P, T](method: Method) -> Method:
  @wraps(method)
  def new_method(self: S, *args: P.args, **kwargs: P.kwargs) -> T:
    name = method.__name__
    log.debug(f'{self.INTERFACE}.{name}() called.')

    return method(self, *args, **kwargs)

  return new_method


class MprisInterface[T: MprisAdapter](ABC):
  name: str
  adapter: T | None

  INTERFACE: ClassVar[Interfaces] = Interfaces.Root

  PropertiesChanged: Final[signal] = signal()

  def __init__(
    self,
    name: str = NAME,
    adapter: T | None = None
  ):
    self.name = name
    self.adapter = adapter
