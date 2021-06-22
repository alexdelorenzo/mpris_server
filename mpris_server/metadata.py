from __future__ import annotations
from typing import List, Tuple, NamedTuple, Any, \
  Dict, Optional, Union

from gi.repository.GLib import Variant

from .base import DbusTypes, DbusMetadata, DEFAULT_TRACK_ID, \
  DbusTypes, MprisTypes, DbusType, Types
from .types import get_origin, TypeAlias, \
  GenericAlias, _GenericAlias, TypedDict


DEFAULT_METADATA: Metadata = {}


MetadataEntry = str


class _MetadataEntries(NamedTuple):
  TRACKID: MetadataEntry = "mpris:trackid"
  LENGTH: MetadataEntry = "mpris:length"
  ART_URL: MetadataEntry = "mpris:artUrl"
  URL: MetadataEntry = "xesam:url"
  TITLE: MetadataEntry = "xesam:title"
  ARTIST: MetadataEntry = "xesam:artist"
  ALBUM: MetadataEntry = "xesam:album"
  ALBUM_ARTIST: MetadataEntry = "xesam:albumArtist"
  DISC_NUMBER: MetadataEntry = "xesam:discNumber"
  TRACK_NUMBER: MetadataEntry = "xesam:trackNumber"
  COMMENT: MetadataEntry = "xesam:comment"


MetadataEntries = _MetadataEntries()


# map of D-Bus metadata entries and their D-Bus types
METADATA_TYPES: Dict[MetadataEntry, DbusType] = {
  MetadataEntries.TRACKID: DbusTypes.OBJ,
  MetadataEntries.LENGTH: DbusTypes.INT64,
  MetadataEntries.ART_URL: DbusTypes.STRING,
  MetadataEntries.URL: DbusTypes.STRING,
  MetadataEntries.TITLE: DbusTypes.STRING,
  MetadataEntries.ARTIST: DbusTypes.STRING_ARRAY,
  MetadataEntries.ALBUM: DbusTypes.STRING,
  MetadataEntries.ALBUM_ARTIST: DbusTypes.STRING_ARRAY,
  MetadataEntries.DISC_NUMBER: DbusTypes.INT32,
  MetadataEntries.TRACK_NUMBER: DbusTypes.INT32,
  MetadataEntries.COMMENT: DbusTypes.STRING_ARRAY,
}

DBUS_PY_TYPES: Dict[DbusType, Types] = {
  DbusTypes.OBJ: MprisTypes.OBJ,
  DbusTypes.STRING: MprisTypes.STRING,
  DbusTypes.INT32: MprisTypes.INT32,
  DbusTypes.INT64: MprisTypes.INT64,
  DbusTypes.UINT32: MprisTypes.UINT32,
  DbusTypes.UINT64: MprisTypes.UINT64,
  DbusTypes.DOUBLE: MprisTypes.DOUBLE,
  DbusTypes.BOOLEAN: MprisTypes.BOOLEAN,
  DbusTypes.OBJ_ARRAY: MprisTypes.OBJ_ARRAY,
  DbusTypes.STRING_ARRAY: MprisTypes.STRING_ARRAY,
}

METADATA_PY_TYPES: Dict[MetadataEntry, Types] = {
  MetadataEntries.TRACKID: DBUS_PY_TYPES[DbusTypes.OBJ],
  MetadataEntries.LENGTH: DBUS_PY_TYPES[DbusTypes.INT64],
  MetadataEntries.ART_URL: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.URL: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.TITLE: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.ARTIST: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.ALBUM: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.ALBUM_ARTIST: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.DISC_NUMBER: DBUS_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.TRACK_NUMBER: DBUS_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.COMMENT: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY]
}


class _MetadataTypes(NamedTuple):
  TRACKID: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.TRACKID]
  LENGTH: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.LENGTH]
  ART_URL: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.ART_URL]
  URL: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.URL]
  TITLE: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.TITLE]
  ARTIST: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.ARTIST]
  ALBUM: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.ALBUM]
  ALBUM_ARTIST: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.ALBUM_ARTIST]
  DISC_NUMBER: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.DISC_NUMBER]
  TRACK_NUMBER: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.TRACK_NUMBER]
  COMMENT: MetadataEntry = METADATA_PY_TYPES[MetadataEntries.COMMENT]


MetadataTypes = _MetadataTypes()


class MetadataObj(NamedTuple):
  track_id: MetadataTypes.TRACKID = DEFAULT_TRACK_ID
  length: Optional[MetadataTypes.LENGTH] = None
  art_url: Optional[MetadataTypes.STRING] = None
  url: Optional[MetadataTypes.STRING] = None
  title: Optional[MetadataTypes.STRING] = None
  artists: Optional[MetadataTypes.STRING_ARRAY] = None
  album: Optional[MetadataTypes.STRING] = None
  album_artists: Optional[MetadataTypes.STRING_ARRAY] = None
  disc_no: Optional[MetadataTypes.INT32] = None
  track_no: Optional[MetadataTypes.INT32] = None
  comment: Optional[MetadataTypes.COMMENT] = None

  def to_dict(self) -> Metadata:
    return Metadata({
      key: val
      for key, val in zip(MetadataEntries, self)
      if val is not None
    })


Metadata = \
  TypedDict('Metadata', METADATA_PY_TYPES, total=False)


ValidMetadata = Union[Metadata, MetadataObj]


def get_runtime_types() -> Tuple[type]:
  types = {
    val
    for val in DBUS_PY_TYPES.values()
    if isinstance(val, type)
  }

  generics = {
    get_origin(val)
    for val in DBUS_PY_TYPES.values()
    if get_origin(val)
  }

  return tuple({*types, *generics})


DBUS_RUNTIME_TYPES: Tuple[type] = get_runtime_types()


def is_null_list(obj: Any) -> bool:
  if isinstance(obj, list):
    return all(item is None for item in obj)

  return False


def is_dbus_type(obj: Any) -> bool:
  return isinstance(obj, DBUS_RUNTIME_TYPES)


def is_valid_metadata(key: str, obj: Any) -> bool:
  if obj is None or key not in METADATA_TYPES:
    return False

  return is_dbus_type(obj) and not is_null_list(obj)


def get_dbus_metadata(metadata: ValidMetadata) -> DbusMetadata:
  if isinstance(metadata, MetadataObj):
    metadata: Metadata = metadata.to_dict()

  return {
    key: Variant(METADATA_TYPES[key], val)
    for key, val in metadata.items()
    if is_valid_metadata(key, val)
  }
