from __future__ import annotations

from typing import ClassVar, Final

from pydbus.generic import signal

from .interface import MprisInterface, log_trace
from ..base import ActivePlaylist, DbusTypes, Interfaces, PlaylistEntry, ROOT_INTERFACE
from ..enums import Access, Arg, Direction, Method, Property, Signal


class Playlists(MprisInterface):
  INTERFACE: ClassVar[Interfaces] = Interfaces.Playlists

  __doc__ = f"""
  <node>
    <interface name="{INTERFACE}">
      <method name="{Method.ActivatePlaylist}">
        <arg name="{Arg.PlaylistId}" type="{DbusTypes.OBJ}" direction="{Direction.In}"/>
      </method>
      <method name="{Method.GetPlaylists}">
        <arg name="{Arg.Index}" type="{DbusTypes.UINT32}" direction="{Direction.In}"/>
        <arg name="{Arg.MaxCount}" type="{DbusTypes.UINT32}" direction="{Direction.In}"/>
        <arg name="{Arg.Order}" type="{DbusTypes.STRING}" direction="{Direction.In}"/>
        <arg name="{Arg.ReverseOrder}" type="{DbusTypes.BOOLEAN}" direction="{Direction.In}"/>
        <arg name="{Arg.Playlists}" type="{DbusTypes.PLAYLISTS}" direction="{Direction.out}"/>
      </method>

      <property name="{Property.ActivePlaylist}" type="{DbusTypes.MAYBE_PLAYLIST}" access="{Access.read}"/>
      <property name="{Property.Orderings}" type="{DbusTypes.STRING_ARRAY}" access="{Access.read}"/>
      <property name="{Property.PlaylistCount}" type="{DbusTypes.UINT32}" access="{Access.read}"/>

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
    # self.log_trace("Getting %s.ActivePlaylist", self.INTERFACE)
    # playlist_is_valid = False
    # playlist = ("/", "None", "")
    # return (playlist_is_valid, playlist)

  @property
  @log_trace
  def Orderings(self) -> list[str]:
    return self.adapter.get_orderings()

  @property
  @log_trace
  def PlaylistCount(self) -> int:
    return self.adapter.get_playlist_count()

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
  def GetPlaylists(self, index: int, max_count: int, order: str, reverse: bool) -> list[PlaylistEntry]:
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
