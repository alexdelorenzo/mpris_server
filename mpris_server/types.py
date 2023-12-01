from __future__ import annotations

from typing import Final, GenericAlias, _GenericAlias, get_origin


ORIGIN: Final[str] = '__origin__'


type GenericAliases = GenericAlias | _GenericAlias


def is_type(obj: type) -> bool:
  return isinstance(obj, type) or bool(get_origin(obj))


def is_generic(obj: type) -> bool:
  return hasattr(obj, ORIGIN) or bool(get_origin(obj))


def get_type(obj: type) -> type | None:
  if hasattr(obj, ORIGIN):
    return getattr(obj, ORIGIN)

  if origin := get_origin(obj):
    return origin

  if isinstance(obj, type):
    return obj

  return None
