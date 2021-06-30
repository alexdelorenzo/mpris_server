from __future__ import annotations

# Python 3.10+
try:
  from typing import \
    Protocol, runtime_checkable, Final, TypedDict, TypeAlias, \
    get_origin, GenericAlias, _GenericAlias

# Python 3.7 - 3.9
except ImportError:
  from typing_extensions import \
    Protocol, runtime_checkable, Final, TypedDict, TypeAlias, \
    get_origin, GenericAlias, _GenericAlias

from typing import Union, Optional


ORIGIN: Final[str] = '__origin__'


GenericAliases = Union[GenericAlias, _GenericAlias]


def is_type(obj: type) -> bool:
  return isinstance(obj, type) or get_origin(obj)


def is_generic(obj: type) -> bool:
  return hasattr(obj, ORIGIN) or get_origin(obj)


def get_type(obj: type) -> Optional[type]:
  if hasattr(obj, ORIGIN):
    return getattr(obj, ORIGIN)

  origin = get_origin(obj)

  if origin:
    return origin

  if isinstance(obj, type):
    return obj

  return None
