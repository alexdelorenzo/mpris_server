from __future__ import annotations

import logging
from collections.abc import Collection, Iterable
from typing import Any, Final, NamedTuple, Required, Self, TypedDict, cast

from gi.repository.GLib import Variant
from strenum import StrEnum

from ..base import DEFAULT_TRACK_ID, DbusPyTypes, DbusTypes, MprisTypes, PyType
from ..types import get_type, is_type


log = logging.getLogger(__name__)

FIRST: Final[int] = 0
DEFAULT_METADATA: Final[Metadata] = {}
FIELDS_ERROR: Final[str] = "Added or missing fields."


type Name = str
type MetadataEntry = str
type NameMetadata = tuple[Name, DbusPyTypes]
type SortedMetadata = dict[Name, DbusPyTypes]


class MetadataEntries(StrEnum):
  ALBUM: MetadataEntry = "xesam:album"
  ALBUM_ARTISTS: MetadataEntry = "xesam:albumArtist"
  ART_URL: MetadataEntry = "mpris:artUrl"
  ARTISTS: MetadataEntry = "xesam:artist"
  AS_TEXT: MetadataEntry = 'xesam:asText'
  AUDIO_BPM: MetadataEntry = 'xesam:audioBPM'
  AUTO_RATING: MetadataEntry = 'xesam:autoRating'
  COMMENT: MetadataEntry = "xesam:comment"
  COMPOSER: MetadataEntry = "xesam:composer"
  CONTENT_CREATED: MetadataEntry = "xesam:contentCreated"
  DISC_NUMBER: MetadataEntry = "xesam:discNumber"
  FIRST_USED: MetadataEntry = "xesam:firstUsed"
  GENRE: MetadataEntry = "xesam:genre"
  LAST_USED: MetadataEntry = "xesam:lastUsed"
  LENGTH: MetadataEntry = "mpris:length"
  LYRICIST: MetadataEntry = "xesam:lyricist"
  TITLE: MetadataEntry = "xesam:title"
  TRACK_ID: MetadataEntry = "mpris:trackid"
  TRACK_NUMBER: MetadataEntry = "xesam:trackNumber"
  URL: MetadataEntry = "xesam:url"
  USE_COUNT: MetadataEntry = "xesam:useCount"
  USER_RATING: MetadataEntry = "xesam:userRating"

  @classmethod
  def sorted(cls: type[Self]) -> list[Self]:
    return sorted(cls, key=sort_by_enum_name)

  @classmethod
  def to_dict(cls: type[Self]) -> dict[str, Self]:
    return {
      enum.name: enum.value
      for enum in cls.sorted()
    }


# map of D-Bus metadata entries and their D-Bus types
METADATA_TYPES: Final[dict[MetadataEntries, DbusTypes]] = {
  MetadataEntries.ALBUM: DbusTypes.STRING,
  MetadataEntries.ALBUM_ARTISTS: DbusTypes.STRING_ARRAY,
  MetadataEntries.ART_URL: DbusTypes.STRING,
  MetadataEntries.ARTISTS: DbusTypes.STRING_ARRAY,
  MetadataEntries.AS_TEXT: DbusTypes.STRING_ARRAY,
  MetadataEntries.AUDIO_BPM: DbusTypes.INT32,
  MetadataEntries.AUTO_RATING: DbusTypes.DOUBLE,
  MetadataEntries.COMMENT: DbusTypes.STRING_ARRAY,
  MetadataEntries.COMPOSER: DbusTypes.STRING_ARRAY,
  MetadataEntries.CONTENT_CREATED: DbusTypes.STRING,
  MetadataEntries.DISC_NUMBER: DbusTypes.INT32,
  MetadataEntries.FIRST_USED: DbusTypes.STRING,
  MetadataEntries.GENRE: DbusTypes.STRING_ARRAY,
  MetadataEntries.LAST_USED: DbusTypes.STRING_ARRAY,
  MetadataEntries.LENGTH: DbusTypes.INT64,
  MetadataEntries.LYRICIST: DbusTypes.STRING_ARRAY,
  MetadataEntries.TITLE: DbusTypes.STRING,
  MetadataEntries.TRACK_ID: DbusTypes.STRING,
  MetadataEntries.TRACK_NUMBER: DbusTypes.INT32,
  MetadataEntries.URL: DbusTypes.STRING,
  MetadataEntries.USE_COUNT: DbusTypes.INT32,
  MetadataEntries.USER_RATING: DbusTypes.DOUBLE,
}

DBUS_TYPES_TO_PY_TYPES: Final[dict[DbusTypes, PyType]] = {
  DbusTypes.BOOLEAN: MprisTypes.BOOLEAN,
  DbusTypes.DATETIME: MprisTypes.DATETIME,
  DbusTypes.DOUBLE: MprisTypes.DOUBLE,
  DbusTypes.INT32: MprisTypes.INT32,
  DbusTypes.INT64: MprisTypes.INT64,
  DbusTypes.OBJ: MprisTypes.OBJ,
  DbusTypes.OBJ_ARRAY: MprisTypes.OBJ_ARRAY,
  DbusTypes.STRING: MprisTypes.STRING,
  DbusTypes.STRING_ARRAY: MprisTypes.STRING_ARRAY,
  DbusTypes.UINT32: MprisTypes.UINT32,
  DbusTypes.UINT64: MprisTypes.UINT64,
}

METADATA_TO_PY_TYPES: Final[dict[MetadataEntries, PyType]] = {
  MetadataEntries.ALBUM: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.ALBUM_ARTISTS: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.ART_URL: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.ARTISTS: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.AS_TEXT: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.AUDIO_BPM: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.AUTO_RATING: DBUS_TYPES_TO_PY_TYPES[DbusTypes.DOUBLE],
  MetadataEntries.COMMENT: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.COMPOSER: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.CONTENT_CREATED: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.DISC_NUMBER: DBUS_TYPES_TO_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.FIRST_USED: DBUS_TYPES_TO_PY_TYPES[DbusTypes.DATETIME],
  MetadataEntries.GENRE: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.LAST_USED: DBUS_TYPES_TO_PY_TYPES[DbusTypes.DATETIME],
  MetadataEntries.LENGTH: DBUS_TYPES_TO_PY_TYPES[DbusTypes.INT64],
  MetadataEntries.LYRICIST: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.TITLE: Required[DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING]],
  MetadataEntries.TRACK_ID: DBUS_TYPES_TO_PY_TYPES[DbusTypes.OBJ],
  MetadataEntries.TRACK_NUMBER: DBUS_TYPES_TO_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.URL: DBUS_TYPES_TO_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.USE_COUNT: DBUS_TYPES_TO_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.USER_RATING: DBUS_TYPES_TO_PY_TYPES[DbusTypes.DOUBLE],
}


assert len(MetadataEntries) == len(METADATA_TYPES) == len(METADATA_TO_PY_TYPES), FIELDS_ERROR


class _MetadataTypes(NamedTuple):
  ALBUM: PyType = METADATA_TO_PY_TYPES[MetadataEntries.ALBUM]
  ALBUM_ARTISTS: PyType = METADATA_TO_PY_TYPES[MetadataEntries.ALBUM_ARTISTS]
  ART_URL: PyType = METADATA_TO_PY_TYPES[MetadataEntries.ART_URL]
  ARTISTS: PyType = METADATA_TO_PY_TYPES[MetadataEntries.ARTISTS]
  AS_TEXT: PyType = METADATA_TO_PY_TYPES[MetadataEntries.AS_TEXT]
  AUDIO_BPM: PyType = METADATA_TO_PY_TYPES[MetadataEntries.AUDIO_BPM]
  AUTO_RATING: PyType = METADATA_TO_PY_TYPES[MetadataEntries.AUTO_RATING]
  COMMENT: PyType = METADATA_TO_PY_TYPES[MetadataEntries.COMMENT]
  COMPOSER: PyType = METADATA_TO_PY_TYPES[MetadataEntries.COMPOSER]
  CONTENT_CREATED: PyType = METADATA_TO_PY_TYPES[MetadataEntries.CONTENT_CREATED]
  DISC_NUMBER: PyType = METADATA_TO_PY_TYPES[MetadataEntries.DISC_NUMBER]
  FIRST_USED: PyType = METADATA_TO_PY_TYPES[MetadataEntries.FIRST_USED]
  GENRE: PyType = METADATA_TO_PY_TYPES[MetadataEntries.GENRE]
  LAST_USED: PyType = METADATA_TO_PY_TYPES[MetadataEntries.FIRST_USED]
  LENGTH: PyType = METADATA_TO_PY_TYPES[MetadataEntries.LENGTH]
  LYRICIST: PyType = METADATA_TO_PY_TYPES[MetadataEntries.LYRICIST]
  TITLE: PyType = METADATA_TO_PY_TYPES[MetadataEntries.TITLE]
  TRACK_ID: PyType = METADATA_TO_PY_TYPES[MetadataEntries.TRACK_ID]
  TRACK_NUMBER: PyType = METADATA_TO_PY_TYPES[MetadataEntries.TRACK_NUMBER]
  URL: PyType = METADATA_TO_PY_TYPES[MetadataEntries.URL]
  USE_COUNT: PyType = METADATA_TO_PY_TYPES[MetadataEntries.USE_COUNT]
  USER_RATING: PyType = METADATA_TO_PY_TYPES[MetadataEntries.USER_RATING]


MetadataTypes: Final[_MetadataTypes] = _MetadataTypes()


assert len(MetadataEntries) == len(MetadataTypes), FIELDS_ERROR


class MetadataObj(NamedTuple):
  album: MetadataTypes.ALBUM | None = None
  album_artists: MetadataTypes.ALBUM_ARTISTS | None = None
  art_url: MetadataTypes.ART_URL | None = None
  artists: MetadataTypes.ARTISTS | None = None
  as_text: MetadataTypes.AS_TEXT | None = None
  audio_bpm: MetadataTypes.AUDIO_BPM | None = None
  auto_rating: MetadataTypes.AUTO_RATING | None = None
  comments: MetadataTypes.COMMENT | None = None
  composer: MetadataTypes.COMPOSER | None = None
  content_created: MetadataTypes.CONTENT_CREATED | None = None
  disc_number: MetadataTypes.DISC_NUMBER | None = None
  first_used: MetadataTypes.FIRST_USED | None = None
  genre: MetadataTypes.GENRE | None = None
  last_used: MetadataTypes.LAST_USED | None = None
  length: MetadataTypes.LENGTH | None = None
  lyricist: MetadataTypes.LYRICIST | None = None
  title: MetadataTypes.TITLE | None = None
  track_id: MetadataTypes.TRACK_ID = DEFAULT_TRACK_ID
  track_number: MetadataTypes.TRACK_NUMBER | None = None
  url: MetadataTypes.URL | None = None
  use_count: MetadataTypes.USE_COUNT | None = None
  user_rating: MetadataTypes.USER_RATING | None = None

  def sorted(self) -> SortedMetadata:
    items: Iterable[NameMetadata] = self._asdict().items()
    items = sorted(items, key=sort_by_name)

    return dict(items)

  def to_dict(self) -> Metadata:
    entries = MetadataEntries.sorted()
    vals = self.sorted().values()
    pairs = zip(entries, vals)
    # return dict(filter(None, pairs))

    return {
      entry: metadata
      for entry, metadata in pairs
      if metadata is not None
    }


assert len(MetadataEntries) == len(MetadataObj._fields), FIELDS_ERROR


Metadata = TypedDict('Metadata', METADATA_TO_PY_TYPES, total=False)

type ValidMetadata = Metadata | MetadataObj
type RuntimeTypes = tuple[type, ...]


def get_runtime_types() -> RuntimeTypes:
  types: set[type] = {
    get_type(val)
    for val in DBUS_TYPES_TO_PY_TYPES.values()
    if is_type(val)
  }

  return tuple(types)


DBUS_RUNTIME_TYPES: Final[RuntimeTypes] = get_runtime_types()


def is_null_collection(obj: Any) -> bool:
  if isinstance(obj, Collection):
    return all(item is None for item in obj)

  return False


def is_dbus_type(obj: Any) -> bool:
  return isinstance(obj, DBUS_RUNTIME_TYPES)


def is_valid_metadata(entry: str, obj: Any) -> bool:
  if obj is None or entry not in METADATA_TYPES:
    log.debug(f"({entry=}, {obj=}) isn't valid metadata, skipping.")
    return False

  return is_dbus_type(obj) and not is_null_collection(obj)


def get_dbus_var(entry: MetadataEntry, obj: Any) -> Variant:
  metadata_type: DbusTypes = METADATA_TYPES[entry]
  log.debug(f"Translating {entry=}, {obj=} to {metadata_type=}")

  return Variant(metadata_type, obj)


def get_dbus_metadata(metadata: ValidMetadata) -> Metadata:
  if isinstance(metadata, MetadataObj):
    metadata: Metadata = metadata.to_dict()

  metadata = cast(Metadata, metadata)

  return {
    entry: get_dbus_var(entry, value)
    for entry, value in metadata.items()
    if is_valid_metadata(entry, value)
  }


def sort_by_name(name_metadata: NameMetadata) -> Name:
  name, _ = name_metadata

  return name.casefold()


def sort_by_enum_name(enum: StrEnum) -> str:
  return enum.name.casefold()
