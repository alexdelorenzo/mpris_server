from __future__ import annotations

from collections.abc import Callable, Collection, Iterable, Mapping, Sequence
from decimal import Decimal
from enum import Enum, auto
from os import PathLike
from string import ascii_letters, digits
from typing import Concatenate, Final, NamedTuple, Self, TYPE_CHECKING, Union

from strenum import StrEnum

from .enums import Property
from .types import GenericAliases


if TYPE_CHECKING:
  from .interfaces.interface import MprisInterface


INTERFACE: Final[str] = "org.mpris.MediaPlayer2"
DBUS_PATH: Final[str] = f"/{INTERFACE.replace('.', '/')}"
NAME: Final[str] = "mprisServer"

NoTrack: Final[DbusObj] = f'{DBUS_PATH}/TrackList/NoTrack'

type Properties = Collection[Property]


MIME_TYPES: Final[list[str]] = [
  "audio/mpeg",
  "application/ogg",
  "video/mpeg",
]
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
INVALIDATED_PROPERTIES: Final[Properties] = ()


class Ordering(StrEnum):
  Alphabetical = auto()
  User = auto()


DEFAULT_TRACK_ID: Final[str] = '/default/1'
DEFAULT_TRACK_NAME: Final[str] = "Default Track"
DEFAULT_TRACK_LENGTH: Final[int] = 0
DEFAULT_PLAYLIST_COUNT: Final[int] = 1
DEFAULT_ORDERINGS: Final[list[Ordering]] = [
  Ordering.Alphabetical,
  Ordering.User,
]
DEFAULT_ALBUM_NAME: Final[str] = "Default Album"
DEFAULT_ARTIST_NAME: Final[str] = "Default Artist"
NO_ARTISTS: Final[tuple[Artist, ...]] = tuple()
NO_ARTIST_NAME: Final[str] = ''

BEGINNING: Final[int] = 0

# valid characters for a DBus name
VALID_PUNC: Final[str] = '_'
VALID_CHARS: Final[set[str]] = {*ascii_letters, *digits, *VALID_PUNC}

NAME_PREFIX: Final[str] = "MprisServer_"
RAND_CHARS: Final[int] = 5

# type aliases
type Paths = PathLike | str
type Changes = Iterable[Property | str]

# units and convenience aliases
Microseconds = int
Position = Microseconds
Duration = Microseconds
UnitInterval = Decimal
Volume = UnitInterval
Rate = UnitInterval

type PlaylistId = str
type PlaylistName = str
type PlaylistIcon = str
type PlaylistEntry = tuple[PlaylistId, PlaylistName, PlaylistIcon]
type PlaylistValidity = bool
type ActivePlaylist = tuple[PlaylistValidity, PlaylistEntry]

# python, d-bus and mpris types
type PyType = type | GenericAliases
type DbusPyTypes = str | float | int | bool | list | Decimal
type PropertyValues = dict[Property, DbusPyTypes]
type DbusMetadata = dict[Property, 'Variant']
type DbusType = str
type DbusObj = str

type Method[S: Self, **P, T] = Callable[Concatenate[S, P], T]


DEFAULT_RATE: Final[Rate] = Rate(1.0)
PAUSE_RATE: Final[Rate] = Rate(0.0)
MIN_RATE: Final[Rate] = Rate(1.0)
MAX_RATE: Final[Rate] = Rate(1.0)

MUTE_VOLUME: Final[Volume] = Volume(0.0)
MAX_VOLUME: Final[Volume] = Volume(1.0)


class Interface(StrEnum):
  Root = INTERFACE
  Player = f'{Root}.Player'
  TrackList = f'{Root}.TrackList'
  Playlists = f'{Root}.Playlists'


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
  ARRAY: PyType = Sequence
  BOOLEAN: PyType = bool
  DATETIME: PyType = str
  DOUBLE: PyType = float
  INT32: PyType = int
  INT64: PyType = int
  MAP: PyType = Mapping
  OBJ: PyType = str
  OBJ_ARRAY: PyType = Sequence[str]
  STRING: PyType = str
  STRING_ARRAY: PyType = Sequence[str]
  UINT32: PyType = int
  UINT64: PyType = int
  VARIANT: PyType = object

  MAYBE_PLAYLIST: PyType = PlaylistEntry | None
  METADATA: PyType = DbusMetadata
  METADATA_ARRAY: PyType = Sequence[DbusMetadata]
  PLAYLIST: PyType = PlaylistEntry
  PLAYLISTS: PyType = Sequence[PlaylistEntry]


MprisTypes: Final = _MprisTypes()
type Compatible = Union[*MprisTypes]


class Artist(NamedTuple):
  name: str = DEFAULT_ARTIST_NAME


class Album(NamedTuple):
  art_url: str | None = None
  artists: Sequence[Artist] = NO_ARTISTS
  name: str = DEFAULT_ALBUM_NAME


class Track(NamedTuple):
  album: Album | None = None
  art_url: str | None = None
  artists: Sequence[Artist] = NO_ARTISTS
  comments: list[str] | None = None
  disc_number: int | None = None
  length: Duration = DEFAULT_TRACK_LENGTH
  name: str = DEFAULT_TRACK_NAME
  track_id: DbusObj = DEFAULT_TRACK_ID
  track_number: int | None = None
  type: Enum | None = None
  uri: str | None = None


def emit_properties_changed[I: MprisInterface](
  interface: I,
  changed_properties: PropertyValues,
  invalidated_properties: Properties = INVALIDATED_PROPERTIES,
):
  interface.PropertiesChanged(
    interface.INTERFACE,
    changed_properties,
    invalidated_properties,
  )


def get_changed_properties[I: MprisInterface](interface: I, changes: Changes) -> PropertyValues:
  return {
    prop: getattr(interface, prop)
    for prop in changes
  }


def dbus_emit_changes[I: MprisInterface](interface: I, changes: Changes):
  if not all(change in Property for change in changes):
    raise ValueError(f"Invalid property in {changes=}")

  changed_properties = get_changed_properties(interface, changes)
  emit_properties_changed(interface, changed_properties)
