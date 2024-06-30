from __future__ import annotations

import logging
from collections.abc import Iterable
from threading import Thread
from typing import Final
from weakref import finalize

from gi.repository import GLib
from pydbus import SessionBus, SystemBus
from pydbus.bus import Bus
from pydbus.publication import Publication

from .adapters import MprisAdapter
from .base import DBUS_PATH, Interface, NAME
from .enums import BusType
from .events import EventAdapter
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

log = logging.getLogger(__name__)

DEFAULT_BUS_TYPE: Final[BusType] = BusType.SESSION
NOW: Final[int] = 0


class Server[A: MprisAdapter, E: EventAdapter, I: MprisInterface]:
  name: str
  adapter: A | None
  events: E | None

  root: Root
  player: Player
  playlists: Playlists
  tracklist: TrackList
  interfaces: tuple[I, ...]

  dbus_name: str

  _loop: GLib.MainLoop | None
  _publication_token: Publication | None
  _thread: Thread | None

  def __init__(
    self,
    name: str = NAME,
    adapter: A | None = None,
    events: E | None = None,
    *interfaces: I,
  ):
    self.name = name
    self.adapter = adapter

    self.root = Root(self.name, self.adapter)
    self.player = Player(self.name, self.adapter)
    self.playlists = Playlists(self.name, self.adapter)
    self.tracklist = TrackList(self.name, self.adapter)
    self.interfaces = self.root, self.player, self.playlists, self.tracklist, *interfaces

    self.dbus_name = get_dbus_name(self.name)

    self._loop = None
    self._publication_token = None
    self._thread = None

    self.set_event_adapter(events)

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

  def set_event_adapter(self, events: E):
    self.events = events

  def publish(self, bus_type: BusType = BusType.DEFAULT):
    log.debug(f'Connecting to D-Bus {bus_type} bus...')
    bus: Bus

    match bus_type:
      case BusType.DEFAULT:
        bus = SessionBus()

      case BusType.SESSION:
        bus = SessionBus()

      case BusType.SYSTEM:
        bus = SystemBus()

      case _:
        log.warning(f'Invalid bus "{bus_type}", using {BusType.DEFAULT}.')
        bus = SessionBus()

    log.debug(f'MPRIS server connecting to D-Bus {bus_type} bus.')
    name = f'{Interface.Root}.{self.dbus_name}'
    paths = self._get_dbus_paths()

    self._publication_token = bus.publish(name, *paths)
    log.info(f'Published {name} to D-Bus {bus_type} bus.')

  def unpublish(self):
    if self._publication_token:
      log.debug('Unpublishing MPRIS interface.')

      self._publication_token.unpublish()
      self._publication_token = None

  def loop(self, bus_type: BusType = BusType.DEFAULT, background: bool = False):
    if not self._publication_token:
      self.publish(bus_type)

    if background:
      log.debug("Entering D-Bus loop in background thread.")
      self._thread = Thread(target=self._run_loop, name=self.name, daemon=True)
      self._thread.start()

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
        self._thread = None

  def quit(self):
    log.debug('Unpublishing and quitting loop.')
    self.unpublish()
    self.quit_loop()
