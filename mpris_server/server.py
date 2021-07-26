from __future__ import annotations
from typing import Optional
from weakref import finalize
from enum import auto
import logging

from strenum import StrEnum
from gi.repository import GLib
import pydbus

from .types import Final
from .adapters import MprisAdapter
from .base import NAME, BUS_TYPE, DBUS_PATH, \
  ROOT_INTERFACE
from .interfaces.player import Player
from .interfaces.playlists import Playlists
from .interfaces.root import Root
from .interfaces.interface import MprisInterface
from .interfaces.tracklist import TrackList
from .mpris.compat import get_dbus_name


class BusType(StrEnum):
  session: str = auto()
  system: str = auto()


DEFAULT_BUS_TYPE: Final[BusType] = BusType.session


class Server:
  def __init__(
    self,
    name: str = NAME,
    adapter: Optional[MprisAdapter] = None
  ):
    self.name = name
    self.adapter = adapter
    self.dbus_name: str = get_dbus_name(self.name)

    self.root = Root(self.name, self.adapter)
    self.player = Player(self.name, self.adapter)
    self.playlists = Playlists(self.name, self.adapter)
    self.tracklist = TrackList(self.name, self.adapter)

    self._loop: Optional[GLib.MainLoop] = None
    self._publication_token: Optional[str] = None

    finalize(self, self.__del__)

  def __del__(self):
    self.unpublish()
    self.quit_loop()

  def publish(self, bus_type: BusType = DEFAULT_BUS_TYPE):
    logging.debug(f'Connecting to D-Bus {bus_type} bus...')

    if bus_type == BusType.system:
      bus = pydbus.SystemBus()

    else:
      bus = pydbus.SessionBus()

    logging.info(f'MPRIS server connected to D-Bus {bus_type} bus')

    self._publication_token = bus.publish(
      f'{ROOT_INTERFACE}.{self.dbus_name}',
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

  def loop(self, bus_type: BusType = DEFAULT_BUS_TYPE):
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

