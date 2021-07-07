from __future__ import annotations
from typing import Iterable, Union, Tuple, \
  Optional, NamedTuple
from enum import Enum, auto
from string import ascii_letters, digits
from os import PathLike

from gi.repository.GLib import Variant

from .types import TypedDict, TypeAlias, \
  GenericAlias, _GenericAlias, Final


Prop = str
Props = list[Prop]


INTERFACE: Final[str] = "org.mpris.MediaPlayer2"
ROOT_INTERFACE: Final[str] = INTERFACE
NAME: Final[str] = "mprisServer"
MIME_TYPES: Final[list[str]] = ["audio/mpeg", "application/ogg", "video/mpeg"]
BUS_TYPE: Final[str] = "session"
URI: Final[Props] = ["file"]
DEFAULT_DESKTOP: Final[str] = ''

# typically, these are the props that D-Bus needs to be notified about
# upon specific state-change events.
ON_ENDED_PROPS: Final[Props] = ['PlaybackStatus']
ON_VOLUME_PROPS: Final[Props] = ['Volume', 'Metadata']
ON_PLAYBACK_PROPS: Final[Props] = [
  'PlaybackStatus', 'Metadata', 'CanControl', 'Rate',
  'MinimumRate', 'MaximumRate',
]
ON_PLAYPAUSE_PROPS: Final[Props] = ['PlaybackStatus']
ON_TITLE_PROPS: Final[Props] = ['Metadata']
ON_OPTION_PROPS: Final[Props] = [
  'LoopStatus', 'Shuffle', 'CanGoPrevious', 'CanGoNext',
  'CanPlay', 'CanPause',
]
ON_SEEK_PROPS: Final[Props] = ['Position', 'CanSeek']

# all props for each interface
ON_PLAYER_PROPS: Final[Props] = list({
  *ON_ENDED_PROPS, *ON_VOLUME_PROPS, *ON_PLAYPAUSE_PROPS,
  *ON_TITLE_PROPS, *ON_OPTION_PROPS, *ON_SEEK_PROPS,
})
ON_TRACKS_PROPS: Final[Props] = ['Tracks']
ON_PLAYLIST_PROPS: Final[Props] = ['PlaylistCount', 'Orderings', 'ActivePlaylist']
ON_ROOT_PROPS: Final[Props] = [
  'CanQuit', 'Fullscreen', 'CanSetFullscreen', 'CanRaise',
  'HasTrackList', 'Identity', 'DesktopEntry', 'SupportedUriSchemes',
  'SupportedMimeTypes'
]

DEFAULT_RATE: Final[float] = 1.0
PAUSE_RATE: Final[float] = 0.0
MIN_RATE: Final[float] = 1.0
MAX_RATE: Final[float] = 1.0

MUTE_VOL: Final[int] = 0
MAX_VOL: Final[int] = 1
BEGINNING: Final[int] = 0

DEFAULT_TRACK_ID: Final[str] = '/default/1'
DEFAULT_PLAYLIST_COUNT: Final[int] = 1
DEFAULT_ORDERINGS: Final[Props] = ["Alphabetical", "User"]

# valid characters for a DBus name
VALID_PUNC: Final[str] = '_'
VALID_CHARS: Final[set[str]] = {*ascii_letters, *digits, *VALID_PUNC}

NAME_PREFIX: Final[str] = "Mpris_Server_"
RAND_CHARS: Final[int] = 5


# type aliases
Paths = Union[PathLike, str]

# units and convenience aliases
Microseconds = int
VolumeDecimal = float
RateDecimal = float
PlaylistEntry = tuple[str, str, str]
PlaylistValidity = bool

# python, d-bus and mpris types
PyType = Union[type, GenericAlias, _GenericAlias]
DbusPyTypes = Union[str, float, int, bool, list]
AttrVals = dict[str, DbusPyTypes]
DbusMetadata = dict[str, Variant]
DbusType = str
DbusObj = str


# See https://docs.python.org/3/library/enum.html#using-automatic-values
class AutoName(Enum):
  def _generate_next_value_(name: str, *args, **kwargs) -> str:
    return name


class PlayState(AutoName):
  PLAYING = auto()
  PAUSED = auto()
  STOPPED = auto()


class _DbusTypes(NamedTuple):
  OBJ: DbusType = 'o'
  STRING: DbusType = 's'
  INT32: DbusType = 'i'
  INT64: DbusType = 'x'
  UINT32: DbusType = 'u'
  UINT64: DbusType = 't'
  DOUBLE: DbusType = 'd'
  BOOLEAN: DbusType = 'b'
  OBJ_ARRAY: DbusType = 'ao'
  STRING_ARRAY: DbusType = 'as'


DbusTypes: Final = _DbusTypes()


class _MprisTypes(NamedTuple):
  OBJ: PyType = str
  STRING: PyType = str
  INT32: PyType = int
  INT64: PyType = int
  UINT32: PyType = int
  UINT64: PyType = int
  DOUBLE: PyType = float
  BOOLEAN: PyType = bool
  OBJ_ARRAY: PyType = list[str]
  STRING_ARRAY: PyType = list[str]


MprisTypes: Final = _MprisTypes()


class Artist(NamedTuple):
  name: str = "Default Artist"


class Album(NamedTuple):
  name: str = "Default Album"
  artists: tuple[Artist] = tuple()
  art_url: Optional[str] = None


class Track(NamedTuple):
  track_id: DbusObj = DEFAULT_TRACK_ID
  name: str = "Default Track"
  track_no: Optional[int] = None
  length: Microseconds = 0
  uri: Optional[str] = None
  artists: tuple[Artist] = tuple()
  album: Optional[Album] = None
  art_url: Optional[str] = None
  disc_no: Optional[int] = None
  type: Optional[Enum] = None


def dbus_emit_changes(
  interface: 'MprisInterface',
  changes: Iterable[str]
):
  attr_vals: AttrVals = {
    attr: getattr(interface, attr)
    for attr in changes
  }

  interface.PropertiesChanged(
    interface.INTERFACE,
    attr_vals,
    []
  )
