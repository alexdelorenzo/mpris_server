from __future__ import annotations

from decimal import Decimal
from enum import Enum, auto
from os import PathLike
from string import ascii_letters, digits
from typing import Callable, Concatenate, Final, Iterable, NamedTuple, Optional, \
  ParamSpec, Self, TYPE_CHECKING, TypeVar, Union, GenericAlias, _GenericAlias

from gi.repository.GLib import Variant
from strenum import StrEnum

from .enums import Property

if TYPE_CHECKING:
  from .interfaces.interface import MprisInterface

NoTrack: Final[str] = '/org/mpris/MediaPlayer2/TrackList/NoTrack'

Properties = list[Property]

INTERFACE: Final[str] = "org.mpris.MediaPlayer2"
ROOT_INTERFACE: Final[str] = INTERFACE
DBUS_PATH: Final[str] = '/org/mpris/MediaPlayer2'
NAME: Final[str] = "mprisServer"

MIME_TYPES: Final[list[str]] = [
  "audio/mpeg",
  "application/ogg",
  "video/mpeg",
]
BUS_TYPE: Final[str] = "session"
URI: Final[list[str]] = [
  "file",
]
DEFAULT_DESKTOP: Final[str] = ''

# typically, these are the props that D-Bus needs to be notified about
# upon specific state-change events.
ON_ENDED_PROPS: Final[Properties] = [
  Property.PlaybackStatus,
]
ON_VOLUME_PROPS: Final[Properties] = [
  Property.Metadata,
  Property.Volume,
]
ON_PLAYBACK_PROPS: Final[Properties] = [
  Property.CanControl,
  Property.MaximumRate,
  Property.Metadata,
  Property.MinimumRate,
  Property.PlaybackStatus,
  Property.Rate,
]
ON_PLAYPAUSE_PROPS: Final[Properties] = [
  Property.PlaybackStatus,
]
ON_TITLE_PROPS: Final[Properties] = [
  Property.Metadata,
]
ON_OPTION_PROPS: Final[Properties] = [
  Property.CanGoNext,
  Property.CanGoPrevious,
  Property.CanPause,
  Property.CanPlay,
  Property.LoopStatus,
  Property.Shuffle,
]
ON_SEEK_PROPS: Final[Properties] = [
  Property.CanSeek,
  Property.Position,
]

# all props for each interface
ON_PLAYER_PROPS: Final[Properties] = sorted({
  *ON_ENDED_PROPS,
  *ON_OPTION_PROPS,
  *ON_PLAYBACK_PROPS,
  *ON_PLAYPAUSE_PROPS,
  *ON_SEEK_PROPS,
  *ON_TITLE_PROPS,
  *ON_VOLUME_PROPS,
})
ON_TRACKS_PROPS: Final[Properties] = [
  Property.CanEditTracks,
  Property.Tracks,
]
ON_PLAYLIST_PROPS: Final[Properties] = [
  Property.ActivePlaylist,
  Property.CanEditTracks,
  Property.Orderings,
  Property.PlaylistCount,
]
ON_ROOT_PROPS: Final[Properties] = [
  Property.CanQuit,
  Property.CanRaise,
  Property.CanSetFullscreen,
  Property.DesktopEntry,
  Property.Fullscreen,
  Property.HasTrackList,
  Property.Identity,
  Property.SupportedMimeTypes,
  Property.SupportedUriSchemes,
]


class Ordering(StrEnum):
  Alphabetical: Self = auto()
  User: Self = auto()


DEFAULT_TRACK_ID: Final[str] = '/default/1'
DEFAULT_PLAYLIST_COUNT: Final[int] = 1
DEFAULT_ORDERINGS: Final[list[Ordering]] = [
  Ordering.Alphabetical,
  Ordering.User,
]

BEGINNING: Final[int] = 0

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
DbusPyTypes = Union[str, float, int, bool, list, Decimal]
PropVals = dict[Property, DbusPyTypes]
DbusMetadata = dict[Property, Variant]
DbusType = str
DbusObj = str

T = TypeVar('T')
P = ParamSpec('P')

Method = Callable[Concatenate[Self, P], T]

DEFAULT_RATE: Final[Rate] = Rate(1.0)
PAUSE_RATE: Final[Rate] = Rate(0.0)
MIN_RATE: Final[Rate] = Rate(1.0)
MAX_RATE: Final[Rate] = Rate(1.0)

MUTE_VOL: Final[Rate] = Rate(0.0)
MAX_VOL: Final[Rate] = Rate(1.0)


class Interfaces(StrEnum):
  Root: Self = INTERFACE
  Player: Self = f'{INTERFACE}.Player'
  TrackList: Self = f'{INTERFACE}.TrackList'
  Playlists: Self = f'{INTERFACE}.Playlists'


class PlayState(StrEnum):
  PAUSED = auto()
  PLAYING = auto()
  STOPPED = auto()


class DbusTypes(StrEnum):
  BOOLEAN: DbusType = 'b'
  STRING: DbusType = 's'
  DATETIME: DbusType = STRING
  DOUBLE: DbusType = 'd'
  INT32: DbusType = 'i'
  INT64: DbusType = 'x'
  OBJ: DbusType = 'o'
  UINT32: DbusType = 'u'
  UINT64: DbusType = 't'
  VARIANT: DbusType = 'v'

  ARRAY: DbusType = 'a'
  MAP: DbusType = f'{ARRAY}{{}}'
  OBJ_ARRAY: DbusType = f'{ARRAY}{OBJ}'
  STRING_ARRAY: DbusType = f'{ARRAY}{STRING}'

  METADATA_ENTRY: DbusType = f'{{{STRING}{VARIANT}}}'
  METADATA: DbusType = f'{ARRAY}{METADATA_ENTRY}'
  METADATA_ARRAY: DbusType = f'{ARRAY}{METADATA}'
  PLAYLIST: DbusType = f'({OBJ}{STRING}{STRING})'
  MAYBE_PLAYLIST: DbusType = f'({BOOLEAN}{PLAYLIST})'
  PLAYLISTS: DbusType = f'{ARRAY}{PLAYLIST}'


class _MprisTypes(NamedTuple):
  ARRAY: PyType = list
  BOOLEAN: PyType = bool
  DATETIME: PyType = str
  DOUBLE: PyType = float
  INT32: PyType = int
  INT64: PyType = int
  MAP: PyType = dict
  OBJ: PyType = str
  OBJ_ARRAY: PyType = list[str]
  STRING: PyType = str
  STRING_ARRAY: PyType = list[str]
  UINT32: PyType = int
  UINT64: PyType = int
  VARIANT: PyType = object

  MAYBE_PLAYLIST: PyType = PlaylistEntry | None
  METADATA: PyType = DbusMetadata
  METADATA_ARRAY: PyType = list[DbusMetadata]
  PLAYLIST: PyType = PlaylistEntry
  PLAYLISTS: PyType = list[PlaylistEntry]


MprisTypes: Final = _MprisTypes()


class Artist(NamedTuple):
  name: str = "Default Artist"


class Album(NamedTuple):
  art_url: Optional[str] = None
  artists: tuple[Artist] = tuple()
  name: str = "Default Album"


class Track(NamedTuple):
  album: Optional[Album] = None
  art_url: Optional[str] = None
  artists: tuple[Artist] = tuple()
  disc_no: Optional[int] = None
  length: Duration = 0
  name: str = "Default Track"
  track_id: DbusObj = DEFAULT_TRACK_ID
  track_no: Optional[int] = None
  type: Optional[Enum] = None
  uri: Optional[str] = None


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
