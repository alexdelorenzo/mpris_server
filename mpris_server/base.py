from enum import Enum, auto
from random import choices
from string import ascii_letters, digits
from typing import Iterable, Union, Dict, Tuple


INTERFACE = "org.mpris.MediaPlayer2"
NAME = "mprisServer"
MIME_TYPES = ["audio/mpeg", "application/ogg", "video/mpeg"]
BUS_TYPE = "session"
URI = ["file"]
DEFAULT_DESKTOP = ''

# typically, these are the props that dbus needs to be notified about
# upon specific state-change events.
ON_ENDED_PROPS = ['PlaybackStatus']
ON_VOLUME_PROPS = ['Volume', 'Metadata']
ON_PLAYBACK_PROPS = ['PlaybackStatus', 'Metadata']
ON_PLAYPAUSE_PROPS = ['PlaybackStatus']
ON_TITLE_PROPS = ['Metadata']
ON_OPTION_PROPS = ['LoopStatus', 'Shuffle', 'CanGoPrevious', 'CanGoNext']
ON_SEEK_PROPS = ['Position']

ON_TRACKS_PROPS = ['Tracks']
ON_PLAYLIST_PROPS = ['PlaylistCount', 'Orderings', 'ActivePlaylist']

DEFAULT_RATE = 1.0
PAUSE_RATE = 0
MIN_RATE = 1.0
MAX_RATE = 1.0

MUTE_VOL = 0
MAX_VOL = 1
BEGINNING = 0

DEFAULT_PLAYLIST_COUNT = 1
DEFAULT_ORDERINGS = ["Alphabetical", "User"]

VALID_CHARS = set(digits + ascii_letters + '_')
DEFAULT_NAME_LEN = 10


# type aliases
TimeInMicroseconds = int
VolumeAsDecimal = float
RateAsDecimal = float
DbusTypes = Union[str, float, int, bool]
Metadata = Dict[str, DbusTypes]
DbusObj = str
PlaylistEntry = Tuple[str, str, str]
PlaylistValidity = bool


#  See https://docs.python.org/3/library/enum.html#using-automatic-values
class AutoName(Enum):
  def _generate_next_value_(name: str, *args, **kwargs) -> str:
    return name


class PlayState(AutoName):
  PLAYING = auto()
  PAUSED = auto()
  STOPPED = auto()


def dbus_emit_changes(interface: 'MprisInterface',
                      changes: Iterable[str]):
  attr_vals = {attr: getattr(interface, attr)
               for attr in changes}

  interface.PropertiesChanged(interface.INTERFACE, attr_vals, [])


def random_name() -> str:
  return ''.join(choices(VALID_CHARS, k=DEFAULT_NAME_LEN))


def get_dbus_name(name: str = None) -> str:
  if not name:
    return random_name()

  new_name = name.replace(' ', '_')
  new_name = ''.join(char for char in new_name
                     if char in VALID_CHARS)

  if new_name:
    return new_name

  return random_name()
