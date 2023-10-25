from __future__ import annotations

import logging
from typing import Final, Iterable
from weakref import finalize
from threading import Thread

from gi.repository import GLib
from pydbus import SessionBus, SystemBus
from pydbus.bus import Bus
from pydbus.publication import Publication

from .adapters import MprisAdapter
from .base import DBUS_PATH, Interfaces, NAME
from .enums import BusType
from .interfaces.interface import MprisInterface
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
NOW: Final[int] = 0


log = logging.getLogger(__name__)


class Server[A: MprisAdapter, I: MprisInterface]:
  name: str
  adapter: A | None

  dbus_name: str

  root: Root
  player: Player
  playlists: Playlists
  tracklist: TrackList
  interfaces: tuple[I, ...]

  _loop: GLib.MainLoop | None
  _publication_token: Publication | None
  _thread: Thread | None

  def __init__(
    self,
    name: str = NAME,
    adapter: A | None = None,
    *interfaces: I,
  ):
    self.name = name
    self.adapter = adapter
    self.dbus_name = get_dbus_name(self.name)

    self.root = Root(self.name, self.adapter)
    self.player = Player(self.name, self.adapter)
    self.playlists = Playlists(self.name, self.adapter)
    self.tracklist = TrackList(self.name, self.adapter)
    self.interfaces = self.root, self.player, self.playlists, self.tracklist, *interfaces

    self._loop = None
    self._publication_token = None
    self._thread = None

    finalize(self, self.__del__)

  def __del__(self):
    self.quit()

  def _get_dbus_paths(self) -> Iterable[tuple[str, I]]:
    for interface in self.interfaces:
      yield DBUS_PATH, interface

  def _run_loop(self):
    self._loop = GLib.MainLoop()

    try:
      self._loop.run()

    finally:
      self.quit_loop()

  def publish(self, bus_type: BusType = BusType.default):
    log.debug(f'Connecting to D-Bus {bus_type} bus...')
    bus: Bus

    match bus_type:
      case BusType.default:
        bus = SessionBus()

      case BusType.session:
        bus = SessionBus()

      case BusType.system:
        bus = SystemBus()

      case _:
        log.warning(f'Invalid bus "{bus_type}", using {BusType.default}.')
        bus = SessionBus()

    log.debug(f'MPRIS server connecting to D-Bus {bus_type} bus.')
    name = f'{Interfaces.Root}.{self.dbus_name}'
    paths = self._get_dbus_paths()

    self._publication_token = bus.publish(name, *paths)
    log.info(f'Published {name} to D-Bus {bus_type} bus.')

  def unpublish(self):
    if self._publication_token:
      log.debug('Unpublishing MPRIS interface.')

      self._publication_token.unpublish()
      self._publication_token = None

  def loop(self, bus_type: BusType = BusType.default, background: bool = False):
    if not self._publication_token:
      self.publish(bus_type)

    if background:
      log.debug("Entering D-Bus loop in background thread.")
      self._thread = Thread(target=self._run_loop, name=self.name)

    else:
      log.debug("Entering D-Bus loop in foreground thread.")
      self._run_loop()

  def quit_loop(self):
    try:
      if self._loop:
        log.debug('Quitting GLib loop.')

        self._loop.quit()
        self._loop = None

    finally:
      if self._thread:
        log.debug("Joining background thread.")
        self._thread.join(timeout=NOW)

  def quit(self):
    log.debug('Unpublishing and quitting loop.')
    self.unpublish()
    self.quit_loop()
