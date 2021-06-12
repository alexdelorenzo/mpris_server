# Python and DBus compatibility
# See:  https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/
from random import choices
from typing import Dict, Tuple, Any, Callable, \
  Optional, Set
from functools import wraps
import logging

from unidecode import unidecode
from emoji import emoji_count, demojize

from .base import VALID_CHARS, RAND_CHARS, NAME_PREFIX
from .metadata import Metadata, DbusMetadata, DbusTypes, \
  MprisMetadata, DbusTypes, METADATA_TYPES


logger = logging.getLogger(__name__)

DBUS_NAME_MAX = 255
START_WITH = "_"
FIRST_CHAR = 0

# following must be subscriptable to be used with choices()
VALID_CHARS_SUB: Tuple[str] = tuple(VALID_CHARS)
INTERFACE_CHARS: Set[str] = {*VALID_CHARS, '-'}


ReturnsStr = Callable[..., str]


def to_ascii(text: str) -> str:
  if emoji_count(text):
    text = demojize(text)

  return unidecode(text)


def random_name() -> str:
  chars = choices(VALID_CHARS_SUB, k=RAND_CHARS)
  rand = ''.join(chars)

  return NAME_PREFIX + rand


def enforce_dbus_length(func: ReturnsStr) -> ReturnsStr:
  @wraps(func)
  def new_func(*args, **kwargs) -> str:
    val: str = func(*args, **kwargs)
    return val[:DBUS_NAME_MAX]

  return new_func


@enforce_dbus_length
def get_dbus_name(
  name: Optional[str] = None,
  is_interface: bool = False
) -> str:
  if not name:
    return get_dbus_name(random_name())

  # interface names can contain hyphens
  if is_interface:
    valid_chars = {*VALID_CHARS, '-'}

  else:
    valid_chars = VALID_CHARS

  # convert utf8 to ascii
  new_name = to_ascii(name)

  # new name shouldn't have spaces
  new_name = new_name.replace(' ', '_')

  # new name should only contain DBus valid chars
  new_name = ''.join(
    char
    for char in new_name
    if char in valid_chars
  )

  # DBus names can't start with numbers
  if new_name and new_name[FIRST_CHAR].isnumeric():
    # just stick an underscore in front of the number
    return START_WITH + new_name

  # but they can start with letters or underscore
  elif new_name:
    return new_name

  # if there is no name left after normalizing,
  # then make a random one and validate it
  return get_dbus_name(random_name())
