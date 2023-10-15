from __future__ import annotations

from abc import ABC
from typing import Optional

from .base import ActivePlaylist, DEFAULT_DESKTOP, DEFAULT_ORDERINGS, DEFAULT_PLAYLIST_COUNT, \
  DEFAULT_RATE, DbusObj, MIME_TYPES, Paths, PlayState, PlaylistEntry, Position, Rate, Track, URI, \
  Volume, NoTrack, Ordering
from .enums import LoopStatus
from .mpris.metadata import Metadata, ValidMetadata


__all__ = [
  'MprisAdapter',
  'NoTrack',
  'PlayerAdapter',
  'PlaylistAdapter',
  'RootAdapter',
  'TrackListAdapter',
]


class RootAdapter(ABC):
  def can_quit(self) -> bool:
    pass

  def can_raise(self) -> bool:
    pass

  def can_fullscreen(self) -> bool:
    pass

  def has_tracklist(self) -> bool:
    pass

  def get_uri_schemes(self) -> list[str]:
    return URI

  def get_mime_types(self) -> list[str]:
    return MIME_TYPES

  def set_raise(self, val: bool):
    pass

  def quit(self):
    pass

  def get_fullscreen(self) -> bool:
    return False

  def set_fullscreen(self, val: bool):
    pass

  def get_desktop_entry(self) -> Paths:
    return DEFAULT_DESKTOP


class PlayerAdapter(ABC):
  def metadata(self) -> ValidMetadata:
    """
    Implement this function to supply your own MPRIS Metadata.

    If this function is implemented, metadata won't be built from get_current_track().

    See: https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/
    """
    pass

  def get_current_track(self) -> Track:
    """
    This function is an artifact of forking the base MPRIS library to a generic interface.
    The base library expected Track-like objects to build metadata.

    If metadata() is implemented, this function won't be used to build MPRIS metadata.
    """
    pass

  def get_current_position(self) -> Position:
    pass

  def next(self):
    pass

  def previous(self):
    pass

  def pause(self):
    pass

  def resume(self):
    pass

  def stop(self):
    pass

  def play(self):
    pass

  def get_playstate(self) -> PlayState:
    pass

  def seek(
    self,
    time: Position,
    track_id: Optional[DbusObj] = None
  ):
    pass

  def open_uri(self, uri: str):
    pass

  def is_repeating(self) -> bool:
    pass

  def is_playlist(self) -> bool:
    pass

  def set_repeating(self, val: bool):
    pass

  def set_loop_status(self, val: LoopStatus):
    match val:
      case LoopStatus.NONE:
        self.set_repeating(False)

      case LoopStatus.TRACK | LoopStatus.PLAYLIST:
        self.set_repeating(True)

  def get_rate(self) -> Rate:
    return DEFAULT_RATE

  def set_rate(self, val: Rate):
    pass

  def set_minimum_rate(self, val: Rate):
    pass

  def set_maximum_rate(self, val: Rate):
    pass

  def get_minimum_rate(self) -> Rate:
    pass

  def get_maximum_rate(self) -> Rate:
    pass

  def set_rate(self, val: Rate):
    pass

  def get_shuffle(self) -> bool:
    pass

  def set_shuffle(self, val: bool):
    pass

  def get_art_url(self, track: int) -> str:
    pass

  def get_volume(self) -> Volume:
    pass

  def set_volume(self, val: Volume):
    pass

  def is_mute(self) -> bool:
    pass

  def set_mute(self, val: bool):
    pass

  def can_go_next(self) -> bool:
    pass

  def can_go_previous(self) -> bool:
    pass

  def can_play(self) -> bool:
    pass

  def can_pause(self) -> bool:
    pass

  def can_seek(self) -> bool:
    pass

  def can_control(self) -> bool:
    pass

  def get_stream_title(self) -> str:
    pass

  def get_previous_track(self) -> Track:
    pass

  def get_next_track(self) -> Track:
    pass


class PlaylistAdapter(ABC):
  def activate_playlist(self, id: DbusObj):
    pass

  def get_playlists(self, index: int, max_count: int, order: str, reverse: bool) -> list[PlaylistEntry]:
    pass

  def get_playlist_count(self) -> int:
    return DEFAULT_PLAYLIST_COUNT

  def get_orderings(self) -> list[Ordering]:
    return DEFAULT_ORDERINGS

  def get_active_playlist(self) -> ActivePlaylist:
    pass


class TrackListAdapter(ABC):
  def get_tracks_metadata(self, track_ids: list[DbusObj]) -> list[Metadata]:
    pass

  def add_track(self, uri: str, after_track: DbusObj, set_as_current: bool):
    pass

  def remove_track(self, track_id: DbusObj):
    pass

  def go_to(self, track_id: DbusObj):
    pass

  def get_tracks(self) -> list[DbusObj]:
    pass

  def can_edit_tracks(self) -> bool:
    pass


class MprisAdapter(
  RootAdapter,
  PlayerAdapter,
  PlaylistAdapter,
  TrackListAdapter,
  ABC
):
  """
  MRPRIS interface for your application.

  The MPRIS implementation is supplied with information
  returned from this adapter.
  """

  def __init__(self, name: str = 'MprisAdapter'):
    self.name = name
