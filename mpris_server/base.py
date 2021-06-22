from typing import Iterable, Union, Dict, Tuple, \
  Optional, NamedTuple, List, Set
from enum import Enum, auto
from string import ascii_letters, digits

from gi.repository.GLib import Variant

from .types import \
  TypedDict, TypeAlias, GenericAlias, _GenericAlias


Props = List[str]


INTERFACE: str = "org.mpris.MediaPlayer2"
NAME: str = "mprisServer"
MIME_TYPES: Props = ["audio/mpeg", "application/ogg", "video/mpeg"]
BUS_TYPE: str = "session"
URI: Props = ["file"]
DEFAULT_DESKTOP: str = ''

# typically, these are the props that dbus needs to be notified about
# upon specific state-change events.
ON_ENDED_PROPS: Props = ['PlaybackStatus']
ON_VOLUME_PROPS: Props = ['Volume', 'Metadata']
ON_PLAYBACK_PROPS: Props = ['PlaybackStatus', 'Metadata']
ON_PLAYPAUSE_PROPS: Props = ['PlaybackStatus']
ON_TITLE_PROPS: Props = ['Metadata']
ON_OPTION_PROPS: Props = ['LoopStatus', 'Shuffle', 'CanGoPrevious', 'CanGoNext']
ON_SEEK_PROPS: Props = ['Position']

ON_TRACKS_PROPS: Props = ['Tracks']
ON_PLAYLIST_PROPS: Props = ['PlaylistCount', 'Orderings', 'ActivePlaylist']

DEFAULT_RATE: float = 1.0
PAUSE_RATE: int = 0
MIN_RATE: float = 1.0
MAX_RATE: float = 1.0

MUTE_VOL: int = 0
MAX_VOL: int = 1
BEGINNING: int = 0

DEFAULT_TRACK_ID: str = '/default/1'
DEFAULT_PLAYLIST_COUNT: int = 1
DEFAULT_ORDERINGS: Props = ["Alphabetical", "User"]

# valid characters for a DBus name 
VALID_PUNC: str = '_'
VALID_CHARS: Set[str] = \
  set(digits + ascii_letters + VALID_PUNC)
NAME_PREFIX: str = "Mpris_Server_"
RAND_CHARS: int = 5


# type aliases
Microseconds = int
VolumeDecimal = float
RateDecimal = float
PlaylistEntry = Tuple[str, str, str]
PlaylistValidity = bool
DbusType = str
_DbusTypes = Union[str, float, int, bool, list]
AttrVals = Dict[str, _DbusTypes]
DbusMetadata = Dict[str, Variant]
DbusObj = str
Types = Union[type, GenericAlias, _GenericAlias]


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


DbusTypes = _DbusTypes()


class _MprisTypes(NamedTuple):
  OBJ: Types = str
  STRING: Types = str
  INT32: Types = int
  INT64: Types = int
  UINT32: Types = int
  UINT64: Types = int
  DOUBLE: Types = float
  BOOLEAN: Types = bool
  OBJ_ARRAY: Types = List[str]
  STRING_ARRAY: Types = List[str]


MprisTypes = _MprisTypes()


class Artist(NamedTuple):
  name: str = "Default Artist"


class Album(NamedTuple):
  name: str = "Default Album"
  artists: Tuple[Artist] = tuple()
  art_url: Optional[str] = None


class Track(NamedTuple):
  track_id: DbusObj = DEFAULT_TRACK_ID
  name: str = "Default Track"
  track_no: Optional[int] = None
  length: Microseconds = 0
  uri: Optional[str] = None
  artists: Tuple[Artist] = tuple()
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
