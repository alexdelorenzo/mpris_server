from typing import List, NamedTuple, Optional, Tuple
from abc import ABC
from enum import Enum

from .base import URI, MIME_TYPES, PlayState, dbus_emit_changes, ON_ENDED_PROPS, ON_VOLUME_PROPS, \
  ON_PLAYBACK_PROPS, ON_PLAYPAUSE_PROPS, ON_TITLE_PROPS, ON_OPTION_PROPS, DEFAULT_RATE, TimeInMicroseconds, \
  VolumeAsDecimal, RateAsDecimal, Metadata
from .player import Player
from .root import Root


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

  Implement this class and integrate it in your application to emit
  DBUS signals when there are state changes in the media player.
  """

  def __init__(self, player: Player, root: Root):
    self.player = player
    self.root = root

  def emit_changes(self, changes: List[str]):
    # TODO: emit Root changes, too
    dbus_emit_changes(self.player, changes)

  def on_ended(self):
    self.emit_changes(ON_ENDED_PROPS)

  def on_volume(self):
    self.emit_changes(ON_VOLUME_PROPS)

  def on_playback(self):
    self.emit_changes(ON_PLAYBACK_PROPS)

  def on_playpause(self):
    self.emit_changes(ON_PLAYPAUSE_PROPS)

  def on_title(self):
    self.emit_changes(ON_TITLE_PROPS)

  def on_seek(self, position: TimeInMicroseconds):
    self.player.Seeked(position)

  def on_options(self):
    self.emit_changes(ON_OPTION_PROPS
                      )


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
  def metadata(self) -> Metadata:
    """
    Implement this function to supply your own MPRIS Metadata.

    If this function is implemented, there is no need to implement get_current_track().

    See: https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/
    :return:
    """
    pass

  def get_current_track(self) -> Track:
    """
    This will be ignored by the Player interface if metadata() is implemented.

    This function is an artifact of forking the base MPRIS library to a generic interface.
    The base library expected Track-like objects to build metadata. If you'd like to supply
    your own, and not implement this more complicated interface, then override metadata().

    :return:
    """
    pass

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

  def get_rate(self) -> RateAsDecimal:
    return DEFAULT_RATE

  def set_rate(self, val: RateAsDecimal):
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

  def get_previous_track(self) -> Track:
    pass

  def get_next_track(self) -> Track:
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
