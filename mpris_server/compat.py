# See:  https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/
import logging
from random import choices

from gi.repository.GLib import Variant

from .base import VALID_CHARS, DEFAULT_NAME_LEN, Metadata, DbusMetadata

# Python and DBus metadata compatibility

logger = logging.getLogger(__name__)

METADATA_TYPES = {
    "mpris:trackid": "o",
    "mpris:length": "x",
    "mpris:artUrl": "s",
    "xesam:url": "s",
    "xesam:title": "s",
    "xesam:artist": "as",
    "xesam:album": "s",
    "xesam:albumArtist": "as",
    "xesam:discNumber": 'i',
    "xesam:trackNumber": 'i',
    "xesam:comment": "as",
}


def random_name() -> str:
    return ''.join(choices(VALID_CHARS, k=DEFAULT_NAME_LEN))


def get_dbus_name(name: str = None) -> str:
    if not name:
        return random_name()

    new_name = name.replace(' ', '_')
    new_name = ''.join(char for char in new_name
                       if char in VALID_CHARS)

    if new_name:
        return new_name

    return random_name()


def is_null_list(obj: object) -> bool:
    if isinstance(obj, (list, tuple, set)):
        return all(item is None for item in obj)
    return False


def is_valid_metadata(obj: object) -> bool:
    return obj is not None and not is_null_list(obj)


def get_dbus_metadata(metadata: Metadata) -> DbusMetadata:
    return {key: Variant(METADATA_TYPES[key], val)
            for key, val in metadata.items()
            if is_valid_metadata(val)}
