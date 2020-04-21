from abc import ABC
from typing import List, NamedTuple, Optional, Dict, Union
from enum import Enum

from .base import URI, MIME_TYPES, PlayState, dbus_emit_changes
from .player import Player


TimeInMicroseconds = int
VolumeAsDecimal = float
Metadata = Dict[str, Union[str, float, int, bool]]


class Artist(NamedTuple):
  name: str = "Default Artist"


class Album(NamedTuple):
  name: str = "Default Album"
  artists: List[Artist] = []
  art_url: str = None


class Track(NamedTuple):
  track_id: str = '/default/1'
  name: str = "Default Track"
  track_no: int = None
  length: TimeInMicroseconds = 0
  uri: str = None
  artists: List[Artist] = []
  album: Optional[Album] = None
  art_url: str = None
  disc_no: int = None
  type: Optional[Enum] = None


class EventAdapter(ABC):
  """
  Implement this class to notify DBUS of state changes in
  the media player app or device.
  """

  def __init__(self, player: Player):
    self.player = player

  def on_ended(self):
    dbus_emit_changes(self.player, ['PlaybackStatus'])

  def on_volume(self):
    dbus_emit_changes(self.player, ['Volume', 'Metadata'])

  def on_playback(self):
    dbus_emit_changes(self.player, ['PlaybackStatus', 'Metadata'])

  def on_playpause(self):
    dbus_emit_changes(self.player, ['PlaybackStatus'])

  def on_title(self):
    dbus_emit_changes(self.player, ['Metadata'])

  def on_seek(self, position: int):
    self.player.Seeked(position)

  def on_options(self):
    dbus_emit_changes(self.player,
                      ['LoopStatus', 'Shuffle, CanGoPrevious', 'CanGoNext'])


class MprisAdapter(ABC):
  """
  MRPRIS interface for your application.

  The MPRIS implementation is supplied with information
  returned from this adapter.
  """

  def __init__(self, name: str = 'MprisAdapter'):
    self.name = name

  def get_uri_schemes(self) -> List[str]:
    return URI

  def get_mime_types(self) -> List[str]:
    return MIME_TYPES

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

  def metadata(self) -> Metadata:
    pass

  def get_stream_title(self) -> str:
    pass

  def get_current_track(self) -> Track:
    pass

  def get_previous_track(self) -> Track:
    pass

  def get_next_track(self) -> Track:
    pass
