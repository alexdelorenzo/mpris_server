from typing import List, NamedTuple, Optional, Dict, Union, Tuple
from abc import ABC
from enum import Enum

from .base import URI, MIME_TYPES, PlayState, dbus_emit_changes
from .player import Player
from .root import Root


TimeInMicroseconds = int
VolumeAsDecimal = float
Metadata = Dict[str, Union[str, float, int, bool]]


class Artist(NamedTuple):
  name: str = "Default Artist"


class Album(NamedTuple):
  name: str = "Default Album"
  artists: Tuple[Artist] = tuple()
  art_url: str = None


class Track(NamedTuple):
  track_id: str = '/default/1'
  name: str = "Default Track"
  track_no: int = None
  length: TimeInMicroseconds = 0
  uri: str = None
  artists: Tuple[Artist] = tuple()
  album: Optional[Album] = None
  art_url: str = None
  disc_no: int = None
  type: Optional[Enum] = None


class EventAdapter(ABC):
  """
  Notify DBUS of state-change events in the media player.
  """

  def __init__(self, player: Player, root: Root):
    self.player = player
    self.root = root

  def emit_changes(self, changes: List[str]):
    # TODO: emit Root changes, too
    dbus_emit_changes(self.player, changes)

  def on_ended(self):
    self.emit_changes(['PlaybackStatus'])

  def on_volume(self):
    self.emit_changes(['Volume', 'Metadata'])

  def on_playback(self):
    self.emit_changes(['PlaybackStatus', 'Metadata'])

  def on_playpause(self):
    self.emit_changes(['PlaybackStatus'])

  def on_title(self):
    self.emit_changes(['Metadata'])

  def on_seek(self, position: int):
    self.player.Seeked(position)

  def on_options(self):
    self.emit_changes(['LoopStatus', 'Shuffle', 'CanGoPrevious', 'CanGoNext'])


class RootAdapter(ABC):
  def get_uri_schemes(self) -> List[str]:
    return URI

  def get_mime_types(self) -> List[str]:
    return MIME_TYPES

  def set_raise(self, val: bool):
    pass

  def quit(self):
    pass

  def get_fullscreen(self) -> bool:
    return False

  def set_fullscreen(self, val: bool):
    pass

  def get_desktop_entry(self) -> str:
    return ''


class PlayerAdapter(ABC):
  def get_current_position(self) -> TimeInMicroseconds:
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

  def seek(self, time: TimeInMicroseconds):
    pass

  def open_uri(self, uri: str):
    pass

  def is_repeating(self) -> bool:
    pass

  def is_playlist(self) -> bool:
    pass

  def set_repeating(self, val: bool):
    pass

  def set_loop_status(self, val: str):
    pass

  def get_rate(self) -> float:
    return 1.0

  def set_rate(self, val: float):
    pass

  def get_shuffle(self) -> bool:
    pass

  def set_shuffle(self, val: bool):
    pass

  def get_art_url(self, track: int) -> str:
    pass

  def get_volume(self) -> VolumeAsDecimal:
    pass

  def set_volume(self, val: VolumeAsDecimal):
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

  def get_current_track(self) -> Track:
    pass

  def get_previous_track(self) -> Track:
    pass

  def get_next_track(self) -> Track:
    pass

  def metadata(self) -> Metadata:
    pass


# TODO: implement PlaylistAdapter interface
class PlaylistAdapter(ABC):
  pass


class MprisAdapter(RootAdapter, PlayerAdapter, PlaylistAdapter):
  """
  MRPRIS interface for your application.

  The MPRIS implementation is supplied with information
  returned from this adapter.
  """

  def __init__(self, name: str = 'MprisAdapter'):
    self.name = name
