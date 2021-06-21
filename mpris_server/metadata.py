from __future__ import annotations
from typing import Set, List, Tuple, NamedTuple, Any, TypeAlias, \
  Dict, TypedDict, Optional, _GenericAlias

from gi.repository.GLib import Variant

from .base import DbusTypes, DbusMetadata, DEFAULT_TRACK_ID


DEFAULT_METADATA: Metadata = {}


class _MprisMetadata(NamedTuple):
  TRACKID: str = "mpris:trackid"
  LENGTH: str = "mpris:length"
  ART_URL: str = "mpris:artUrl"
  URL: str = "xesam:url"
  TITLE: str = "xesam:title"
  ARTIST: str = "xesam:artist"
  ALBUM: str = "xesam:album"
  ALBUM_ARTIST: str = "xesam:albumArtist"
  DISC_NUMBER: str = "xesam:discNumber"
  TRACK_NUMBER: str = "xesam:trackNumber"
  COMMENT: str = "xesam:comment"


MprisMetadata = _MprisMetadata()


class _DbusTypes(NamedTuple):
  OBJ: str = 'o'
  STRING: str = 's'
  INT32: str = 'i'
  INT64: str = 'x'
  UINT32: str = 'u'
  UINT64: str = 't'
  DOUBLE: str = 'd'
  BOOLEAN: str = 'b'
  OBJ_ARRAY: str = 'ao'
  STRING_ARRAY: str = 'as'


DbusTypes = _DbusTypes()


# map of D-Bus metadata entries and their D-Bus types
METADATA_TYPES: Dict[str, str] = {
  MprisMetadata.TRACKID: DbusTypes.OBJ,
  MprisMetadata.LENGTH: DbusTypes.INT64,
  MprisMetadata.ART_URL: DbusTypes.STRING,
  MprisMetadata.URL: DbusTypes.STRING,
  MprisMetadata.TITLE: DbusTypes.STRING,
  MprisMetadata.ARTIST: DbusTypes.STRING_ARRAY,
  MprisMetadata.ALBUM: DbusTypes.STRING,
  MprisMetadata.ALBUM_ARTIST: DbusTypes.STRING_ARRAY,
  MprisMetadata.DISC_NUMBER: DbusTypes.INT32,
  MprisMetadata.TRACK_NUMBER: DbusTypes.INT32,
  MprisMetadata.COMMENT: DbusTypes.STRING_ARRAY,
}


DBUS_PY_TYPES: Dict[str, type] = {
  DbusTypes.OBJ: str,
  DbusTypes.STRING: str,
  DbusTypes.INT32: int,
  DbusTypes.INT64: int,
  DbusTypes.UINT32: int,
  DbusTypes.UINT64: int,
  DbusTypes.DOUBLE: float,
  DbusTypes.BOOLEAN: bool,
  DbusTypes.OBJ_ARRAY: List[str],
  DbusTypes.STRING_ARRAY: List[str],
}


METADATA_PY_TYPES: Dict[str, type] = {
  MprisMetadata.TRACKID: DBUS_PY_TYPES[DbusTypes.OBJ],
  MprisMetadata.LENGTH: DBUS_PY_TYPES[DbusTypes.INT64],
  MprisMetadata.ART_URL: DBUS_PY_TYPES[DbusTypes.STRING],
  MprisMetadata.URL: DBUS_PY_TYPES[DbusTypes.STRING],
  MprisMetadata.TITLE: DBUS_PY_TYPES[DbusTypes.STRING],
  MprisMetadata.ARTIST: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MprisMetadata.ALBUM: DBUS_PY_TYPES[DbusTypes.STRING],
  MprisMetadata.ALBUM_ARTIST: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MprisMetadata.DISC_NUMBER: DBUS_PY_TYPES[DbusTypes.INT32],
  MprisMetadata.TRACK_NUMBER: DBUS_PY_TYPES[DbusTypes.INT32],
  MprisMetadata.COMMENT: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY]
}


class _MetadataTypes(NamedTuple):
  TRACKID: str = METADATA_PY_TYPES[MprisMetadata.TRACKID]
  LENGTH: str = METADATA_PY_TYPES[MprisMetadata.LENGTH]
  ART_URL: str = METADATA_PY_TYPES[MprisMetadata.ART_URL]
  URL: str = METADATA_PY_TYPES[MprisMetadata.URL]
  TITLE: str = METADATA_PY_TYPES[MprisMetadata.TITLE]
  ARTIST: str = METADATA_PY_TYPES[MprisMetadata.ARTIST]
  ALBUM: str = METADATA_PY_TYPES[MprisMetadata.ALBUM]
  ALBUM_ARTIST: str = METADATA_PY_TYPES[MprisMetadata.ALBUM_ARTIST]
  DISC_NUMBER: str = METADATA_PY_TYPES[MprisMetadata.DISC_NO]
  TRACK_NUMBER: str = METADATA_PY_TYPES[MprisMetadata.TRACK_NUMBER]
  COMMENT: str = METADATA_PY_TYPES[MprisMetadata.COMMENT]


MetadataTypes = _MetadataTypes()


class MetadataObj(NamedTuple):
  track_id: MetadataTypes.TRACKID = DEFAULT_TRACK_ID
  length: Optional[MetadataTypes.LENGTH] = None
  art_url: Optional[MetadataTypes.STRING] = None
  url: Optional[MetadataTypes.STRING] = None
  title: Optional[MetadataTypes.STRING] = None
  artist: Optional[MetadataTypes.STRING_ARRAY] = None
  album: Optional[MetadataTypes.STRING] = None
  album_artist: Optional[MetadataTypes.STRING_ARRAY] = None
  disc_no: Optional[MetadataTypes.INT32] = None
  track_no: Optional[MetadataTypes.INT32] = None
  comment: Optional[MetadataTypes.COMMENT] = None

  def to_dict(self) -> Metadata:
    return Metadata({
      key: val
      for key, val in zip(MprisMetadata, self)
      if val is not None
    })


Metadata = \
  TypedDict('Metadata', METADATA_PY_TYPES, total=False)


def get_runtime_types() -> Tuple[type]:
  types = {
    val
    for val in DBUS_PY_TYPES.values()
    if isinstance(val, type)
  }

  generics = {
    val.__origin__
    for val in DBUS_PY_TYPES.values()
    if isinstance(val, _GenericAlias)
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


def get_dbus_metadata(metadata: Metadata) -> DbusMetadata:
  return {
    key: Variant(METADATA_TYPES[key], val)
    for key, val in metadata.items()
    if is_valid_metadata(key, val)
  }
