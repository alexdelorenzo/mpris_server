from .player import Player
from .playlists import Playlists
from .root import Root
from .base import NAME, BUS_TYPE
from .adapters import MprisAdapter
import logging

import pydbus

logger = logging.getLogger(__name__)
logger.debug("test")


class Server:
    def __init__(self,
                 name: str = NAME,
                 adapter: MprisAdapter = None):
        self.name = name
        self.root = Root(name, adapter)
        self.player = Player(name, adapter)
        self.playlists = Playlists(name, adapter)

        self._publication_token = None

    def __del__(self):
        self.unpublish()

    def publish(self):
        bus_type = BUS_TYPE
        logger.debug("Connecting to D-Bus %s bus...", bus_type)

        if bus_type == "system":
            bus = pydbus.SystemBus()
        else:
            bus = pydbus.SessionBus()

        logger.info("MPRIS server connected to D-Bus %s bus", bus_type)

        self._publication_token = bus.publish(
            f"org.mpris.MediaPlayer2.{self.name}",
            ("/org/mpris/MediaPlayer2", self.root),
            ("/org/mpris/MediaPlayer2", self.player),
            # ("/org/mpris/MediaPlayer2", self.playlists),
        )

    def unpublish(self):
        if self._publication_token:
            self._publication_token.unpublish()
            self._publication_token = None
