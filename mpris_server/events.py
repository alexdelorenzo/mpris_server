from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override

from .base import Changes, DbusObj, ON_ENDED_PROPS, ON_OPTION_PROPS, ON_PLAYBACK_PROPS, ON_PLAYER_PROPS, \
  ON_PLAYLIST_PROPS, ON_PLAYPAUSE_PROPS, ON_ROOT_PROPS, ON_SEEK_PROPS, ON_TITLE_PROPS, ON_TRACKS_PROPS, ON_VOLUME_PROPS, \
  Position, dbus_emit_changes
from .interfaces.interface import MprisInterface
from .interfaces.player import Player
from .interfaces.playlists import Playlists
from .interfaces.root import Root
from .interfaces.tracklist import TrackList
from .mpris.metadata import Metadata


__all__ = [
  'BaseEventAdapter',
  'Changes',
  'EventAdapter',
  'PlayerEventAdapter',
  'PlaylistsEventAdapter',
  'RootEventAdapter',
  'TracklistEventAdapter',
]


class BaseEventAdapter(ABC):
  root: Root
  player: Player | None
  playlist: Playlists | None
  tracklist: TrackList | None

  def __init__(
    self,
    root: Root,
    player: Player | None = None,
    playlists: Playlists | None = None,
    tracklist: TrackList | None = None,
  ):
    self.root = root
    self.player = player
    self.playlist = playlists
    self.tracklist = tracklist

  @staticmethod
  def emit_changes[I: MprisInterface](interface: I, changes: Changes):
    dbus_emit_changes(interface, changes)

  @abstractmethod
  def emit_all(self):
    """Emit all changes for all adapters in hierarchy"""
    pass


class RootEventAdapter(BaseEventAdapter, ABC):
  @override
  def emit_all(self):
    self.on_root_all()
    super().emit_all()

  def emit_root_changes(self, changes: Changes):
    self.emit_changes(self.root, changes)

  def on_root_all(self):
    self.emit_root_changes(ON_ROOT_PROPS)


class PlayerEventAdapter(BaseEventAdapter, ABC):
  @override
  def emit_all(self):
    self.on_player_all()
    super().emit_all()

  def on_player_all(self):
    self.emit_player_changes(ON_PLAYER_PROPS)

  def emit_player_changes(self, changes: Changes):
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

  def on_seek(self, position: Position):
    self.player.Seeked(position)
    self.emit_player_changes(ON_SEEK_PROPS)

  def on_options(self):
    self.emit_player_changes(ON_OPTION_PROPS)


class PlaylistsEventAdapter(BaseEventAdapter, ABC):
  @override
  def emit_all(self):
    self.on_playlists_all()
    super().emit_all()

  def emit_playlist_changes(self, changes: Changes):
    self.emit_changes(self.playlist, changes)

  def on_playlists_all(self):
    self.emit_playlist_changes(ON_PLAYLIST_PROPS)

  def on_playlist_change(self, playlist_id: DbusObj):
    self.playlist.PlaylistChanged(playlist_id)
    self.emit_playlist_changes(ON_PLAYLIST_PROPS)


class TracklistEventAdapter(BaseEventAdapter, ABC):
  @override
  def emit_all(self):
    self.on_tracklist_all()
    super().emit_all()

  def emit_tracklist_changes(self, changes: Changes):
    self.emit_changes(self.tracklist, changes)

  def on_tracklist_all(self):
    self.emit_tracklist_changes(ON_TRACKS_PROPS)

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
