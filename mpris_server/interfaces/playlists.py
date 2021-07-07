from __future__ import annotations
from typing import Union
import base64
import logging

from pydbus.generic import signal

from ..base import PlaylistEntry, PlaylistValidity, ROOT_INTERFACE
from ..types import Final
from .interface import MprisInterface, log_trace


class Playlists(MprisInterface):
  """
  <node>
    <interface name="org.mpris.MediaPlayer2.Playlists">
      <method name="ActivatePlaylist">
        <arg name="PlaylistId" type="o" direction="in"/>
      </method>
      <method name="GetPlaylists">
        <arg name="Index" type="u" direction="in"/>
        <arg name="MaxCount" type="u" direction="in"/>
        <arg name="Order" type="s" direction="in"/>
        <arg name="ReverseOrder" type="b" direction="in"/>
        <arg name="Playlists" type="a(oss)" direction="out"/>
      </method>
      <signal name="PlaylistChanged">
        <arg name="Playlist" type="oss"/>
      </signal>
      <property name="PlaylistCount" type="u" access="read"/>
      <property name="Orderings" type="as" access="read"/>
      <property name="ActivePlaylist" type="(b(oss))" access="read"/>
    </interface>
  </node>
  """

  INTERFACE: Final[str] = f"{ROOT_INTERFACE}.Playlists"

  PlaylistChanged = signal()

  @log_trace
  def ActivatePlaylist(self, playlist_id: str):
    self.adapter.activate_playlist(playlist_id)
    # logging.debug(
    #     "%s.ActivatePlaylist(%r) called", self.INTERFACE, playlist_id
    # )
    # playlist_uri = get_playlist_uri(playlist_id)
    # playlist = self.core.playlists.lookup(playlist_uri).get()
    # if playlist and playlist.tracks:
    #     tl_tracks = self.core.tracklist.add(playlist.tracks).get()
    #     self.core.playback.play(tlid=tl_tracks[0].tlid).get()

  @log_trace
  def GetPlaylists(self, index: int, max_count: int, order: str, reverse: bool) -> list[tuple]:
    return self.adapter.get_playlists(index, max_count, order, reverse)
    # logging.debug(
    #     "%s.GetPlaylists(%r, %r, %r, %r) called",
    #     self.INTERFACE,
    #     index,
    #     max_count,
    #     order,
    #     reverse,
    # )
    # playlists = self.core.playlists.as_list().get()
    # if order == "Alphabetical":
    #     playlists.sort(key=lambda p: p.name, reverse=reverse)
    # elif order == "User" and reverse:
    #     playlists.reverse()
    # slice_end = index + max_count
    # playlists = playlists[index:slice_end]
    # results = [(get_playlist_id(p.uri), p.name, "") for p in playlists]
    # return results

  @property
  @log_trace
  def PlaylistCount(self) -> int:
    return self.adapter.get_playlist_count()

  @property
  @log_trace
  def Orderings(self) -> list[str]:
    return self.adapter.get_orderings()

  @property
  @log_trace
  def ActivePlaylist(self) -> tuple[PlaylistValidity, PlaylistEntry]:
    return self.adapter.get_active_playlist()
    # self.log_trace("Getting %s.ActivePlaylist", self.INTERFACE)
    # playlist_is_valid = False
    # playlist = ("/", "None", "")
    # return (playlist_is_valid, playlist)

#
# def get_playlist_id(playlist_uri: Union[str, bytes]) -> str:
#     # Only A-Za-z0-9_ is allowed, which is 63 chars, so we can't use
#     # base64. Luckily, D-Bus does not limit the length of object paths.
#     # Since base32 pads trailing bytes with "=" chars, we need to replace
#     # them with an allowed character such as "_".
#     if isinstance(playlist_uri, str):
#         playlist_uri = playlist_uri.encode()
#     encoded_uri = base64.b32encode(playlist_uri).decode().replace("=", "_")
#     return "/com/mopidy/playlist/%s" % encoded_uri
#
#
# def get_playlist_uri(playlist_id: Union[str, bytes]) -> str:
#     if isinstance(playlist_id, bytes):
#         playlist_id = playlist_id.decode()
#     encoded_uri = playlist_id.split("/")[-1].replace("_", "=").encode()
#     return base64.b32decode(encoded_uri).decode()
