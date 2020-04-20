from dataclasses import dataclass
from abc import ABC
import abc
from typing import List, NamedTuple, Optional
from enum import Enum, auto

from .constants import URI, MIME_TYPES
# from .interface import Interface


# from https://docs.python.org/3/library/enum.html#using-automatic-values
class AutoName(Enum):
  def _generate_next_value_(name, start, count, last_values):
    return name


class PlayState(AutoName):
  PLAYING = auto()
  PAUSED = auto()
  STOPPED = auto()


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
  length: int = 0
  uri: str = None
  artists: List[Artist] = []
  album: Optional[Album] = None
  art_url: str = None
  disc_no: int = None
  type: Optional[Enum] = None


class Adapter(ABC):
  def __init__(self, name: str = 'mprisAdapter'):
    self.name = name

  ## root.py
  def get_uri_schemes(self) -> List[str]:
    return URI

  def get_mime_types(self) -> List[str]:
    return MIME_TYPES

  ## player.py
  def get_current_postion(self) -> int:
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

  def seek(self, time: int):
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

  def get_volume(self) -> int:
    pass

  def set_volume(self, val: int):
    pass

  def is_mute(self) -> bool:
    pass

  def set_mute(self, val: bool):
    pass

  def get_position(self) -> int:
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

  def metadata(self):
    pass

  def get_stream_title(self) -> str:
    pass

  def get_current_track(self) -> Track:
    pass

  def get_previous_track(self) -> Track:
    pass

  def get_next_track(self) -> Track:
    pass
