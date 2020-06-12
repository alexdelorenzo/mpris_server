# See:  https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/
import logging
from random import choices

from gi.repository.GLib import Variant

from .base import VALID_CHARS, Metadata, DbusMetadata, DbusTypes, \
    RAND_CHARS, NAME_PREFIX

# Python and DBus compatibility

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

START_WITH = "_"
FIRST_CHAR = 0


def random_name() -> str:
    return NAME_PREFIX + ''.join(choices(VALID_CHARS, k=RAND_CHARS))


def get_dbus_name(name: str = None) -> str:
    if not name:
        return random_name()

    new_name = name.replace(' ', '_')
    new_name = ''.join(char for char in new_name
                       if char in VALID_CHARS)

    if new_name and new_name[FIRST_CHAR].isnumeric():
        return START_WITH + new_name

    elif new_name:
        return new_name

    return get_dbus_name(random_name())


def is_null_list(obj: object) -> bool:
    if isinstance(obj, list):
        return all(item is None for item in obj)

    return False


def is_dbus_type(obj: object) -> bool:
    return isinstance(obj, DbusTypes.__args__)


def is_valid_metadata(obj: object) -> bool:
    return is_dbus_type(obj) and not is_null_list(obj)


def get_dbus_metadata(metadata: Metadata) -> DbusMetadata:
    return {key: Variant(METADATA_TYPES[key], val)
            for key, val in metadata.items()
            if is_valid_metadata(val)}
