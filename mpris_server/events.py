from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from .base import dbus_emit_changes, Microseconds, DbusObj, \
  ON_VOLUME_PROPS, ON_PLAYBACK_PROPS, ON_PLAYPAUSE_PROPS, \
  ON_TITLE_PROPS, ON_SEEK_PROPS, ON_OPTION_PROPS, ON_ENDED_PROPS, \
  ON_PLAYLIST_PROPS, ON_TRACKS_PROPS, ON_PLAYER_PROPS, \
  ON_ROOT_PROPS
from .interfaces.interface import MprisInterface
from .interfaces.playlists import Playlists
from .interfaces.tracklist import TrackList
from .interfaces.player import Player
from .interfaces.root import Root
from .mpris.metadata import Metadata


class BaseEventAdapter(ABC):
  def __init__(
    self,
    player: Player,
    root: Root,
    playlist: Optional[Playlists] = None,
    tracklist: Optional[TrackList] = None,
  ):
    self.root = root
    self.player = player
    self.playlist = playlist
    self.tracklist = tracklist

  def emit_changes(self, interface: MprisInterface, changes: list[str]):
    dbus_emit_changes(interface, changes)

  @abstractmethod
  def emit_all(self):
    pass


class RootEventAdapter(BaseEventAdapter, ABC):
  def emit_all(self):
    self.on_root_all()
    super().emit_all()

  def emit_root_changes(self, changes: list[str]):
    self.emit_changes(self.root, changes)

  def on_root_all(self):
    self.emit_root_changes(ON_ROOT_PROPS)


class PlayerEventAdapter(BaseEventAdapter, ABC):
  def emit_all(self):
    self.on_player_all()
    super().emit_all()

  def emit_player_changes(self, changes: list[str]):
    self.emit_changes(self.player, changes)

  def on_ended(self):
    self.emit_player_changes(ON_ENDED_PROPS)

  def on_volume(self):
    self.emit_player_changes(ON_VOLUME_PROPS)

  def on_playback(self):
    self.emit_player_changes(ON_PLAYBACK_PROPS)

  def on_playpause(self):
    self.emit_player_changes(ON_PLAYPAUSE_PROPS)

  def on_title(self):
    self.emit_player_changes(ON_TITLE_PROPS)

  def on_seek(self, position: Microseconds):
    self.player.Seeked(position)
    self.emit_player_changes(ON_SEEK_PROPS)

  def on_options(self):
    self.emit_player_changes(ON_OPTION_PROPS)

  def on_player_all(self):
    self.emit_player_changes(ON_PLAYER_PROPS)


class PlaylistsEventAdapter(BaseEventAdapter, ABC):
  def emit_playlist_changes(self, changes: list[str]):
    self.emit_changes(self.playlist, changes)

  def on_playlist_change(self, playlist_id: DbusObj):
    self.playlist.PlaylistChanged(playlist_id)
    self.emit_playlist_changes(ON_PLAYLIST_PROPS)


class TracklistEventAdapter(BaseEventAdapter, ABC):
  def emit_tracklist_changes(self, changes: list[str]):
    self.emit_changes(self.tracklist, changes)

  def on_list_replaced(self, tracks: list[DbusObj], current_track: DbusObj):
    self.tracklist.TrackListReplaced(tracks, current_track)
    self.emit_tracklist_changes(ON_TRACKS_PROPS)

  def on_track_added(self, metadata: Metadata, after_track: DbusObj):
    self.tracklist.TrackAdded(metadata, after_track)
    self.emit_tracklist_changes(ON_TRACKS_PROPS)

  def on_track_removed(self, track_id: DbusObj):
    self.tracklist.TrackRemoved(track_id)
    self.emit_tracklist_changes(ON_TRACKS_PROPS)

  def on_track_metadata_change(self, track_id: DbusObj, metadata: Metadata):
    self.tracklist.TrackMetadataChanged(track_id, metadata)
    self.emit_tracklist_changes(ON_TRACKS_PROPS)


class EventAdapter(
  RootEventAdapter,
  PlayerEventAdapter,
  TracklistEventAdapter,
  PlaylistsEventAdapter,
  ABC,
):
  '''
  Notify D-Bus of state-change events in the media player.

  Implement this class and integrate it in your application to emit
  D-Bus signals when there are state changes in the media player.
  '''
  pass
