from __future__ import annotations
from typing import Set, List, Tuple, NamedTuple, Any, TypeAlias, \
  Dict, TypedDict, Optional

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


METADATA_PY_TYPES: Dict[str, type] = {
  MprisMetadata.TRACKID: str,
  MprisMetadata.LENGTH: int,
  MprisMetadata.ART_URL: str,
  MprisMetadata.URL: str,
  MprisMetadata.TITLE: str,
  MprisMetadata.ARTIST: List[str],
  MprisMetadata.ALBUM: str,
  MprisMetadata.ALBUM_ARTIST: List[str],
  MprisMetadata.DISC_NUMBER: int,
  MprisMetadata.TRACK_NUMBER: int,
  MprisMetadata.COMMENT: List[str]
}

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


MetadataBase = \
  TypedDict('Metadata', METADATA_PY_TYPES, total=False)


class Metadata(MetadataBase):
  pass


class _DbusTypes(NamedTuple):
  OBJ: str = 'o'
  STRING: str = 's'
  INT32: str = 'i'
  INT64: str = 'x'
  STRING_ARRAY: str = 'as'


DbusTypes = _DbusTypes()


DBUS_PY_TYPES: Dict[str, type] = {
  DbusTypes.OBJ: str,
  DbusTypes.STRING: str,
  DbusTypes.INT32: int,
  DbusTypes.INT64: int,
  DbusTypes.STRING_ARRAY: List[str],
}


DBUS_RUNTIME_TYPES: Tuple[type] = tuple({
  val
  for val in DBUS_PY_TYPES.values()
  if isinstance(val, type)
})


class MetadataObj(NamedTuple):
  track_id: str = DEFAULT_TRACK_ID
  length: Optional[int] = None
  art_url: Optional[str] = None
  url: Optional[str] = None
  title: Optional[str] = None
  artist: Optional[List[str]] = None
  album: Optional[str] = None
  album_artist: Optional[List[str]] = None
  disc_no: Optional[int] = None
  track_no: Optional[int] = None
  comment: Optional[List[str]] = None

  def to_dict(self) -> Metadata:
    return Metadata({
      key: val
      for key, val in zip(MprisMetadata, self)
      if val is not None
    })


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
