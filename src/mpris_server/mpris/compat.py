# Python and DBus compatibility
# See:  https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/
from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import wraps
from random import choices
from typing import Final

from emoji import demojize, emoji_count
from unidecode import unidecode

from ..base import DbusObj, NAME_PREFIX, RAND_CHARS, VALID_CHARS


DBUS_NAME_MAX: Final[int] = 255
START_WITH: Final[str] = "_"
FIRST_CHAR: Final[int] = 0

# following must be subscriptable to be used with random.choices()
VALID_CHARS_SUB: Final[Sequence[str]] = tuple(VALID_CHARS)
INTERFACE_CHARS: Final[set[str]] = {*VALID_CHARS, '-'}


type ReturnsStr[**P] = Callable[P, str]


def to_ascii(text: str) -> str:
  if emoji_count(text):
    text = demojize(text)

  return unidecode(text)


def random_name() -> str:
  chars = choices(VALID_CHARS_SUB, k=RAND_CHARS)
  name = ''.join(chars)

  return NAME_PREFIX + name


def enforce_dbus_length[**P](func: ReturnsStr) -> ReturnsStr:
  @wraps(func)
  def new_func(*args: P.args, **kwargs: P.kwargs) -> str:
    val: str = func(*args, **kwargs)
    return val[:DBUS_NAME_MAX]

  return new_func


@enforce_dbus_length
def get_dbus_name(
  name: str | None = None,
  is_interface: bool = False,
) -> str:
  if not name:
    return get_dbus_name(random_name())

  # interface names can contain hyphens
  valid_chars = INTERFACE_CHARS if is_interface else VALID_CHARS

  # convert utf8 to ascii
  new_name = to_ascii(name)

  # new name shouldn't have spaces
  new_name = new_name.replace(' ', '_')

  # new name should only contain D-Bus valid chars
  new_name = ''.join(
    char
    for char in new_name
    if char in valid_chars
  )

  # D-Bus names can't start with numbers
  if new_name and new_name[FIRST_CHAR].isnumeric():
    # just stick an underscore in front of the number
    return START_WITH + new_name

  # but they can start with letters or underscores
  elif new_name:
    return new_name

  # if there is no name left after normalizing,
  # then make a random one and validate it
  return get_dbus_name(random_name())


@enforce_dbus_length
def get_track_id(name: str) -> DbusObj:
  return f'/track/{get_dbus_name(name)}'
