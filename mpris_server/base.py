from __future__ import annotations

from decimal import Decimal
from enum import Enum, auto
from os import PathLike
from string import ascii_letters, digits
from typing import Iterable, NamedTuple, Optional, Self, TYPE_CHECKING, Union

from gi.repository.GLib import Variant
from strenum import StrEnum

from .types import Final, GenericAlias, _GenericAlias


if TYPE_CHECKING:
  from .interfaces.interface import MprisInterface


class Property(StrEnum):
  ActivePlaylist: Self = auto()
  CanControl: Self = auto()
  CanGoNext: Self = auto()
  CanGoPrevious: Self = auto()
  CanPause: Self = auto()
  CanPlay: Self = auto()
  CanQuit: Self = auto()
  CanRaise: Self = auto()
  CanSeek: Self = auto()
  CanSetFullscreen: Self = auto()
  DesktopEntry: Self = auto()
  Fullscreen: Self = auto()
  HasTrackList: Self = auto()
  Identity: Self = auto()
  LoopStatus: Self = auto()
  MaximumRate: Self = auto()
  Metadata: Self = auto()
  MinimumRate: Self = auto()
  Orderings: Self = auto()
  PlaybackStatus: Self = auto()
  PlaylistCount: Self = auto()
  Position: Self = auto()
  Rate: Self = auto()
  Shuffle: Self = auto()
  SupportedMimeTypes: Self = auto()
  SupportedUriSchemes: Self = auto()
  Tracks: Self = auto()
  Volume: Self = auto()


Properties = list[Property]

INTERFACE: Final[str] = "org.mpris.MediaPlayer2"
ROOT_INTERFACE: Final[str] = INTERFACE
DBUS_PATH: Final[str] = '/org/mpris/MediaPlayer2'
NAME: Final[str] = "mprisServer"

MIME_TYPES: Final[list[str]] = ["audio/mpeg", "application/ogg", "video/mpeg"]
BUS_TYPE: Final[str] = "session"
URI: Final[list[str]] = ["file"]
DEFAULT_DESKTOP: Final[str] = ''

# typically, these are the props that D-Bus needs to be notified about
# upon specific state-change events.
ON_ENDED_PROPS: Final[Properties] = [
  Property.PlaybackStatus,
]
ON_VOLUME_PROPS: Final[Properties] = [
  Property.Volume,
  Property.Metadata,
]
ON_PLAYBACK_PROPS: Final[Properties] = [
  Property.PlaybackStatus,
  Property.Metadata,
  Property.CanControl,
  Property.Rate,
  Property.MinimumRate,
  Property.MaximumRate,
]
ON_PLAYPAUSE_PROPS: Final[Properties] = [
  Property.PlaybackStatus,
]
ON_TITLE_PROPS: Final[Properties] = [
  Property.Metadata,
]
ON_OPTION_PROPS: Final[Properties] = [
  Property.LoopStatus,
  Property.Shuffle,
  Property.CanGoPrevious,
  Property.CanGoNext,
  Property.CanPlay,
  Property.CanPause,
]
ON_SEEK_PROPS: Final[Properties] = [
  Property.Position,
  Property.CanSeek
]

# all props for each interface
ON_PLAYER_PROPS: Final[Properties] = list({
  *ON_ENDED_PROPS,
  *ON_VOLUME_PROPS,
  *ON_PLAYPAUSE_PROPS,
  *ON_TITLE_PROPS,
  *ON_OPTION_PROPS,
  *ON_SEEK_PROPS,
  *ON_PLAYBACK_PROPS,
})
ON_TRACKS_PROPS: Final[Properties] = [
  Property.Tracks
]
ON_PLAYLIST_PROPS: Final[Properties] = [
  Property.PlaylistCount,
  Property.Orderings,
  Property.ActivePlaylist
]
ON_ROOT_PROPS: Final[Properties] = [
  Property.CanQuit,
  Property.Fullscreen,
  Property.CanSetFullscreen,
  Property.CanRaise,
  Property.HasTrackList,
  Property.Identity,
  Property.DesktopEntry,
  Property.SupportedUriSchemes,
  Property.SupportedMimeTypes,
]

BEGINNING: Final[int] = 0

DEFAULT_TRACK_ID: Final[str] = '/default/1'
DEFAULT_PLAYLIST_COUNT: Final[int] = 1
DEFAULT_ORDERINGS: Final[list[str]] = ["Alphabetical", "User"]

# valid characters for a DBus name
VALID_PUNC: Final[str] = '_'
VALID_CHARS: Final[set[str]] = {*ascii_letters, *digits, *VALID_PUNC}

NAME_PREFIX: Final[str] = "Mpris_Server_"
RAND_CHARS: Final[int] = 5

# type aliases
Paths = Union[PathLike, str]

# units and convenience aliases
Microseconds = int
Position = Microseconds
Duration = Microseconds
UnitInterval = Decimal
Volume = UnitInterval
Rate = UnitInterval

PlaylistId = str
PlaylistName = str
PlaylistIcon = str
PlaylistEntry = tuple[PlaylistId, PlaylistName, PlaylistIcon]
PlaylistValidity = bool
ActivePlaylist = tuple[PlaylistValidity, PlaylistEntry]

# python, d-bus and mpris types
PyType = Union[type, GenericAlias, _GenericAlias]
DbusPyTypes = Union[str, float, int, bool, list]
PropVals = dict[Property, DbusPyTypes]
DbusMetadata = dict[Property, Variant]
DbusType = str
DbusObj = str

DEFAULT_RATE: Final[Rate] = Rate(1.0)
PAUSE_RATE: Final[Rate] = Rate(0.0)
MIN_RATE: Final[Rate] = Rate(1.0)
MAX_RATE: Final[Rate] = Rate(1.0)

MUTE_VOL: Final[Rate] = Rate(0)
MAX_VOL: Final[Rate] = Rate(1)


class PlayState(StrEnum):
  PLAYING = auto()
  PAUSED = auto()
  STOPPED = auto()


class DbusTypes(StrEnum):
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
  length: Duration = 0
  uri: Optional[str] = None
  artists: tuple[Artist] = tuple()
  album: Optional[Album] = None
  art_url: Optional[str] = None
  disc_no: Optional[int] = None
  type: Optional[Enum] = None


def dbus_emit_changes(
  interface: MprisInterface,
  changes: Iterable[Property]
):
  prop_vals: PropVals = {
    prop: getattr(interface, prop)
    for prop in changes
  }

  interface.PropertiesChanged(
    interface.INTERFACE,
    prop_vals,
    []
  )
