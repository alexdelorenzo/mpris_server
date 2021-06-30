from __future__ import annotations
from typing import Optional
from weakref import finalize
import logging

from gi.repository import GLib
import pydbus

from .adapters import MprisAdapter
from .base import NAME, BUS_TYPE
from .interfaces.player import Player
from .interfaces.playlists import Playlists
from .interfaces.root import Root
from .interfaces.interface import MprisInterface
from .interfaces.tracklist import TrackList
from .mpris.compat import get_dbus_name


class Server:
  def __init__(
    self,
    name: str = NAME,
    adapter: Optional[MprisAdapter] = None
  ):
    self.name = name
    self.adapter = adapter
    self.dbus_name: str = get_dbus_name(self.name)
    self.root = Root(name, self.adapter)
    self.player = Player(name, self.adapter)
    self.playlists = Playlists(name, self.adapter)
    self.tracklist = TrackList(name, self.adapter)

    self._loop: Optional[GLib.MainLoop] = None
    self._publication_token: Optional[str] = None

    finalize(self, self.__del__)

  def __del__(self):
    self.unpublish()
    self.quit_loop()

  def publish(self):
    bus_type: str = BUS_TYPE
    logging.debug(f'Connecting to D-Bus {bus_type} bus...')

    if bus_type == 'system':
      bus = pydbus.SystemBus()

    else:
      bus = pydbus.SessionBus()

    logging.info(f'MPRIS server connected to D-Bus {bus_type} bus')

    self._publication_token = bus.publish(
      f'org.mpris.MediaPlayer2.{self.dbus_name}',
      ('/org/mpris/MediaPlayer2', self.root),
      ('/org/mpris/MediaPlayer2', self.player),
      ('/org/mpris/MediaPlayer2', self.playlists),
      ('/org/mpris/MediaPlayer2', self.tracklist)
    )

  def unpublish(self):
    if self._publication_token:
      logging.debug('Unpublishing MPRIS interface.')

      self._publication_token.unpublish()
      self._publication_token = None

  def quit_loop(self):
    if self._loop:
      logging.debug('Quitting GLib loop.')

      self._loop.quit()
      self._loop = None

  def loop(self):
    if not self._publication_token:
      self.publish()

    self._loop = GLib.MainLoop()

    try:
      self._loop.run()

    finally:
      self.quit_loop()
