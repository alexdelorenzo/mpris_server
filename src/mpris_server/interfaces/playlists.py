from __future__ import annotations

import logging
from typing import ClassVar, Final

from pydbus.generic import signal

from .interface import MprisInterface, log_trace
from ..base import ActivePlaylist, DbusTypes, Interface, Ordering, PlaylistEntry, PlaylistId
from ..enums import Access, Arg, Direction, Method, Property, Signal


log = logging.getLogger(__name__)


class Playlists(MprisInterface):
  INTERFACE: ClassVar[Interface] = Interface.Playlists

  __doc__: Final[str] = f"""
  <node>
    <interface name="{INTERFACE}">
      <method name="{Method.ActivatePlaylist}">
        <arg name="{Arg.PlaylistId}" type="{DbusTypes.OBJ}" direction="{Direction.IN}"/>
      </method>
      <method name="{Method.GetPlaylists}">
        <arg name="{Arg.Index}" type="{DbusTypes.UINT32}" direction="{Direction.IN}"/>
        <arg name="{Arg.MaxCount}" type="{DbusTypes.UINT32}" direction="{Direction.IN}"/>
        <arg name="{Arg.Order}" type="{DbusTypes.STRING}" direction="{Direction.IN}"/>
        <arg name="{Arg.ReverseOrder}" type="{DbusTypes.BOOLEAN}" direction="{Direction.IN}"/>
        <arg name="{Arg.Playlists}" type="{DbusTypes.PLAYLISTS}" direction="{Direction.OUT}"/>
      </method>

      <property name="{Property.ActivePlaylist}" type="{DbusTypes.MAYBE_PLAYLIST}" access="{Access.READ}"/>
      <property name="{Property.Orderings}" type="{DbusTypes.STRING_ARRAY}" access="{Access.READ}"/>
      <property name="{Property.PlaylistCount}" type="{DbusTypes.UINT32}" access="{Access.READ}"/>

      <signal name="{Signal.PlaylistChanged}">
        <arg name="{Arg.Playlist}" type="{DbusTypes.PLAYLIST}"/>
      </signal>
    </interface>
  </node>
  """

  PlaylistChanged: Final[signal] = signal()

  @property
  @log_trace
  def ActivePlaylist(self) -> ActivePlaylist:
    return self.adapter.get_active_playlist()

  @property
  @log_trace
  def Orderings(self) -> list[Ordering]:
    return self.adapter.get_orderings()

  @property
  @log_trace
  def PlaylistCount(self) -> int:
    return self.adapter.get_playlist_count()

  @log_trace
  def ActivatePlaylist(self, playlist_id: PlaylistId):
    self.adapter.activate_playlist(playlist_id)

  @log_trace
  def GetPlaylists(self, index: int, max_count: int, order: str, reverse: bool) -> list[PlaylistEntry]:
    return self.adapter.get_playlists(index, max_count, order, reverse)
