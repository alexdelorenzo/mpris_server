from __future__ import annotations

from typing import Final

from . import adapters, base, types, server, mpris, interfaces

from .adapters import *
from .base import *
from .enums import *
from .events import *
from .interfaces import *
from .mpris import *
from .server import *


# modules
from . import adapters, base, interfaces, mpris, server, types
from .interfaces import interface, player, playlists, root, tracklist

# constants and aliases
from .base import (
  BEGINNING, DEFAULT_RATE, MIME_TYPES, URI, DbusObj, Microseconds, Paths, PlayState,
  Rate, Track, Volume,
)

# classes
from .adapters import (
  MprisAdapter, PlayerAdapter, PlaylistAdapter, RootAdapter, TrackListAdapter,
)
from .events import EventAdapter
from .server import Server

# mpris spec
from .mpris.compat import enforce_dbus_length, get_dbus_name, get_track_id
from .mpris.metadata import Metadata, MetadataObj, ValidMetadata


__version__: Final[str] = '0.8.0'
