from __future__ import annotations

import logging
from abc import ABC
from functools import wraps
from typing import ClassVar, Final, Self, TYPE_CHECKING

from pydbus.generic import signal

from ..base import Interface, Method, NAME


if TYPE_CHECKING:
  from ..adapters import MprisAdapter


log = logging.getLogger(__name__)


def log_trace[S: Self, **P, T](method: Method) -> Method:
  @wraps(method)
  def new_method(self: S, *args: P.args, **kwargs: P.kwargs) -> T:
    name = method.__name__
    func = f'{self.INTERFACE}.{name}()'

    log.debug(f'{func} called.')

    if (result := method(self, *args, **kwargs)) is not None:
      log.debug(f'{func} result: {result}')

    return result

  return new_method


class MprisInterface[A: MprisAdapter](ABC):
  INTERFACE: ClassVar[Interface] = Interface.Root

  name: str
  adapter: A | None

  PropertiesChanged: Final[signal] = signal()

  def __init__(self, name: str = NAME, adapter: A | None = None):
    self.name = name
    self.adapter = adapter
