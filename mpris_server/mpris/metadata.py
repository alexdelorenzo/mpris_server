from __future__ import annotations

import logging
from typing import NamedTuple, Any, Optional, Union, \
  cast

from gi.repository.GLib import Variant
from strenum import StrEnum
from rich import print

from ..base import DbusObj, DbusTypes, DbusMetadata, DEFAULT_TRACK_ID, \
  DbusTypes, MprisTypes, DbusType, PyType
from ..types import Final, TypedDict, is_type, get_type


DEFAULT_METADATA: Final[Metadata] = {}


MetadataEntry = str


class MetadataEntries(StrEnum):
  ALBUM: MetadataEntry = "xesam:album"
  ALBUM_ARTIST: MetadataEntry = "xesam:albumArtist"
  ART_URL: MetadataEntry = "mpris:artUrl"
  ARTIST: MetadataEntry = "xesam:artist"
  COMMENT: MetadataEntry = "xesam:comment"
  DISC_NUMBER: MetadataEntry = "xesam:discNumber"
  LENGTH: MetadataEntry = "mpris:length"
  TITLE: MetadataEntry = "xesam:title"
  TRACK_ID: MetadataEntry = "mpris:trackid"
  TRACK_NUMBER: MetadataEntry = "xesam:trackNumber"
  URL: MetadataEntry = "xesam:url"


# MetadataEntries: Final = _MetadataEntries()


# map of D-Bus metadata entries and their D-Bus types
METADATA_TYPES: Final[dict[MetadataEntry, DbusType]] = {
  MetadataEntries.ALBUM: DbusTypes.STRING,
  MetadataEntries.ALBUM_ARTIST: DbusTypes.STRING_ARRAY,
  MetadataEntries.ART_URL: DbusTypes.STRING,
  MetadataEntries.ARTIST: DbusTypes.STRING_ARRAY,
  MetadataEntries.COMMENT: DbusTypes.STRING_ARRAY,
  MetadataEntries.DISC_NUMBER: DbusTypes.INT32,
  MetadataEntries.LENGTH: DbusTypes.INT64,
  MetadataEntries.TITLE: DbusTypes.STRING,
  MetadataEntries.TRACK_ID: DbusTypes.STRING,
  MetadataEntries.TRACK_NUMBER: DbusTypes.INT32,
  MetadataEntries.URL: DbusTypes.STRING,
}

DBUS_PY_TYPES: Final[dict[DbusType, PyType]] = {
  DbusTypes.BOOLEAN: MprisTypes.BOOLEAN,
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

METADATA_PY_TYPES: Final[dict[MetadataEntry, PyType]] = {
  MetadataEntries.ALBUM: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.ALBUM_ARTIST: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.ART_URL: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.ARTIST: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.COMMENT: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.DISC_NUMBER: DBUS_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.LENGTH: DBUS_PY_TYPES[DbusTypes.INT64],
  MetadataEntries.TITLE: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.TRACK_ID: DBUS_PY_TYPES[DbusTypes.OBJ],
  MetadataEntries.TRACK_NUMBER: DBUS_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.URL: DBUS_PY_TYPES[DbusTypes.STRING],
}


class _MetadataTypes(NamedTuple):
  ALBUM: PyType = METADATA_PY_TYPES[MetadataEntries.ALBUM]
  ALBUM_ARTIST: PyType = METADATA_PY_TYPES[MetadataEntries.ALBUM_ARTIST]
  ART_URL: PyType = METADATA_PY_TYPES[MetadataEntries.ART_URL]
  ARTIST: PyType = METADATA_PY_TYPES[MetadataEntries.ARTIST]
  COMMENT: PyType = METADATA_PY_TYPES[MetadataEntries.COMMENT]
  DISC_NUMBER: PyType = METADATA_PY_TYPES[MetadataEntries.DISC_NUMBER]
  LENGTH: PyType = METADATA_PY_TYPES[MetadataEntries.LENGTH]
  TITLE: PyType = METADATA_PY_TYPES[MetadataEntries.TITLE]
  TRACK_NUMBER: PyType = METADATA_PY_TYPES[MetadataEntries.TRACK_NUMBER]
  TRACKID: PyType = METADATA_PY_TYPES[MetadataEntries.TRACK_ID]
  URL: PyType = METADATA_PY_TYPES[MetadataEntries.URL]


MetadataTypes: Final = _MetadataTypes()


class MetadataObj(NamedTuple):
  album: Optional[MprisTypes.STRING] = None
  album_artists: Optional[MprisTypes.STRING_ARRAY] = None
  art_url: Optional[MprisTypes.STRING] = None
  artists: Optional[MprisTypes.STRING_ARRAY] = None
  comments: Optional[MprisTypes.STRING_ARRAY] = None
  disc_no: Optional[MprisTypes.INT32] = None
  length: Optional[MprisTypes.LENGTH] = None
  title: Optional[MprisTypes.STRING] = None
  track_id: MprisTypes.OBJ = DEFAULT_TRACK_ID
  track_no: Optional[MprisTypes.INT32] = None
  url: Optional[MprisTypes.STRING] = None

  def to_dict(self) -> Metadata:
    return {
      key: val
      for key, val in zip(MetadataEntries, self)
      if val is not None
    }


Metadata = \
  TypedDict('Metadata', METADATA_PY_TYPES, total=False)

ValidMetadata = Union[Metadata, MetadataObj]


def get_runtime_types() -> tuple[type, ...]:
  types = {
    get_type(val)
    for val in DBUS_PY_TYPES.values()
    if is_type(val)
  }

  return tuple(types)


DBUS_RUNTIME_TYPES: Final[tuple[type, ...]] = \
  get_runtime_types()


def is_null_list(obj: Any) -> bool:
  if isinstance(obj, list):
    return all(item is None for item in obj)

  return False


def is_dbus_type(obj: Any) -> bool:
  return isinstance(obj, DBUS_RUNTIME_TYPES)


def is_valid_metadata(entry: str, obj: Any) -> bool:
  if obj is None or entry not in METADATA_TYPES:
    return False

  return is_dbus_type(obj) and not is_null_list(obj)


def get_dbus_var(entry: MetadataEntry, obj: DbusObj) -> Variant:
  metadata_type = METADATA_TYPES[entry]
  logging.debug(f"{entry=}, {obj=}, {metadata_type=}")
  return Variant(metadata_type, obj)


def get_dbus_metadata(metadata: ValidMetadata) -> DbusMetadata:
  if isinstance(metadata, MetadataObj):
    metadata: Metadata = metadata.to_dict()

  metadata = cast(Metadata, metadata)

  return {
    entry: get_dbus_var(entry, val)
    for entry, val in metadata.items()
    if is_valid_metadata(entry, val)
  }
