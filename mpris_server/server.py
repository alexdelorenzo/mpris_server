from __future__ import annotations

import logging
from typing import Final
from weakref import finalize

from gi.repository import GLib
from pydbus import SessionBus, SystemBus
from pydbus.bus import Bus
from pydbus.publication import Publication

from .adapters import MprisAdapter
from .base import DBUS_PATH, Interfaces, NAME
from .enums import BusType
from .interfaces.player import Player
from .interfaces.playlists import Playlists
from .interfaces.root import Root
from .interfaces.tracklist import TrackList
from .mpris.compat import get_dbus_name


__all__ = [
  'DEFAULT_BUS_TYPE',  # for backwards compatibility
  'BusType',  # for backwards compatibility
  'Server',
]

DEFAULT_BUS_TYPE: Final[BusType] = BusType.session


class Server[T: MprisAdapter]:
  name: str
  adapter: T | None

  dbus_name: str

  root: Root
  player: Player
  playlists: Playlists
  tracklist: TrackList

  _loop: GLib.MainLoop | None
  _publication_token: Publication | None

  def __init__(
    self,
    name: str = NAME,
    adapter: T | None = None
  ):
    self.name = name
    self.adapter = adapter
    self.dbus_name = get_dbus_name(self.name)

    self.root = Root(self.name, self.adapter)
    self.player = Player(self.name, self.adapter)
    self.playlists = Playlists(self.name, self.adapter)
    self.tracklist = TrackList(self.name, self.adapter)

    self._loop = None
    self._publication_token = None

    finalize(self, self.__del__)

  def __del__(self):
    self.unpublish()
    self.quit_loop()

  def publish(self, bus_type: BusType = BusType.default):
    logging.debug(f'Connecting to D-Bus {bus_type} bus...')
    bus: Bus

    match bus_type:
      case BusType.system:
        bus = SystemBus()

      case BusType.session:
        bus = SessionBus()

      case _:
        logging.warning(f'Invalid bus "{bus_type}", using {BusType.default}.')
        bus = SessionBus()

    logging.info(f'MPRIS server connected to D-Bus {bus_type} bus.')

    self._publication_token = bus.publish(
      f'{Interfaces.Root}.{self.dbus_name}',
      (DBUS_PATH, self.root),
      (DBUS_PATH, self.player),
      (DBUS_PATH, self.playlists),
      (DBUS_PATH, self.tracklist),
    )

  def unpublish(self):
    if self._publication_token:
      logging.debug('Unpublishing MPRIS interface.')

      self._publication_token.unpublish()
      self._publication_token = None

  def loop(self, bus_type: BusType = BusType.default):
    if not self._publication_token:
      self.publish(bus_type)

    self._loop = GLib.MainLoop()

    try:
      self._loop.run()

    finally:
      self.quit_loop()

  def quit_loop(self):
    if self._loop:
      logging.debug('Quitting GLib loop.')

      self._loop.quit()
      self._loop = None
