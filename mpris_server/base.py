from enum import Enum, auto
from typing import Iterable

INTERFACE = "org.mpris.MediaPlayer2"
NAME = "mprisServer"
MIME_TYPES = ["audio/mpeg", "application/ogg", "video/mpeg"]
BUS_TYPE = "session"
URI = ["file"]


class AutoName(Enum):
  """See https://docs.python.org/3/library/enum.html#using-automatic-values"""

  def _generate_next_value_(name, *args):
    return name


class PlayState(AutoName):
  PLAYING = auto()
  PAUSED = auto()
  STOPPED = auto()


def dbus_emit_changes(interface: 'Interface',
                      changes: Iterable[str]):
  attr_vals = {attr: getattr(interface, attr)
               for attr in changes}

  interface.PropertiesChanged(interface.INTERFACE, attr_vals, [])