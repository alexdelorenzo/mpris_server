from __future__ import annotations

import logging
from enum import StrEnum
from typing import ClassVar, Optional

from gi.repository.GLib import Variant
from pydbus.generic import signal

from .interface import MprisInterface, log_trace
from ..base import BEGINNING, DbusTypes, MAX_RATE, MAX_VOL, MIN_RATE, MUTE_VOL, PAUSE_RATE, \
  PlayState, Position, ROOT_INTERFACE, Rate, Track, Volume
from ..enums import Access, Arg, Direction, Method, Property, Signal
from ..mpris.metadata import DEFAULT_METADATA, DbusMetadata, Metadata, get_dbus_metadata
from ..types import Final


class LoopStatus(StrEnum):
  NONE: str = 'None'
  TRACK: str = 'Track'
  PLAYLIST: str = 'Playlist'


class Player(MprisInterface):
  INTERFACE: ClassVar[str] = f"{ROOT_INTERFACE}.Player"

  __doc__ = f"""
  <node>
    <interface name="{INTERFACE}">
      <method name="{Method.Next}"/>
      <method name="{Method.Pause}"/>
      <method name="{Method.PlayPause}"/>
      <method name="{Method.Play}"/>
      <method name="{Method.Previous}"/>
      <method name="{Method.Stop}"/>
      <method name="{Method.OpenUri}">
        <arg name="{Arg.Uri}" type="{DbusTypes.STRING}" direction="{Direction.In}"/>
      </method>
        <method name="{Method.Seek}">
        <arg name="{Arg.Offset}" type="{DbusTypes.INT64}" direction="{Direction.In}"/>
      </method>
      <method name="{Method.SetPosition}">
        <arg name="{Arg.TrackId}" type="{DbusTypes.OBJ}" direction="{Direction.In}"/>
        <arg name="{Arg.Position}" type="{DbusTypes.INT64}" direction="{Direction.In}"/>
      </method>

      <property name="{Property.CanControl}" type="{DbusTypes.BOOLEAN}" access="{Access.read}"/>
      <property name="{Property.CanGoNext}" type="{DbusTypes.BOOLEAN}" access="{Access.read}"/>
      <property name="{Property.CanGoPrevious}" type="{DbusTypes.BOOLEAN}" access="{Access.read}"/>
      <property name="{Property.CanPause}" type="{DbusTypes.BOOLEAN}" access="{Access.read}"/>
      <property name="{Property.CanPlay}" type="{DbusTypes.BOOLEAN}" access="{Access.read}"/>
      <property name="{Property.CanSeek}" type="{DbusTypes.BOOLEAN}" access="{Access.read}"/>
      <property name="{Property.LoopStatus}" type="{DbusTypes.STRING}" access="{Access.readwrite}"/>
      <property name="{Property.MaximumRate}" type="{DbusTypes.DOUBLE}" access="{Access.read}"/>
      <property name="{Property.Metadata}" type="{DbusTypes.METADATA}" access="{Access.read}"/>
      <property name="{Property.MinimumRate}" type="{DbusTypes.DOUBLE}" access="{Access.read}"/>
      <property name="{Property.PlaybackStatus}" type="{DbusTypes.STRING}" access="{Access.read}"/>
      <property name="{Property.Position}" type="{DbusTypes.INT64}" access="{Access.read}"/>
      <property name="{Property.Rate}" type="{DbusTypes.DOUBLE}" access="{Access.readwrite}"/>
      <property name="{Property.Shuffle}" type="{DbusTypes.BOOLEAN}" access="{Access.readwrite}"/>
      <property name="{Property.Volume}" type="{DbusTypes.DOUBLE}" access="{Access.readwrite}"/>

      <signal name="{Signal.Seeked}">
        <arg name="{Arg.Position}" type="{DbusTypes.INT64}"/>
      </signal>
    </interface>
  </node>
  """

  Seeked: Final[signal] = signal()

  def _dbus_metadata(self) -> Optional[DbusMetadata]:
    if metadata := self.adapter.metadata():
      return get_dbus_metadata(metadata)

    return None

  def _get_art_url(self, track: 'Track') -> str:
    return self.adapter.get_art_url(track)

  @log_trace
  def Next(self):
    if not self.CanGoNext:
      logging.debug(f"{self.INTERFACE}.Next not allowed")
      return

    self.adapter.next()

  @log_trace
  def Previous(self):
    if not self.CanGoPrevious:
      logging.debug(f"{self.INTERFACE}.Previous not allowed")
      return

    self.adapter.previous()

  @log_trace
  def Pause(self):
    if not self.CanPause:
      logging.debug(f"{self.INTERFACE}.Pause not allowed")
      return

    self.adapter.pause()

  @log_trace
  def PlayPause(self):
    if not self.CanPause:
      logging.debug(f"{self.INTERFACE}.PlayPause not allowed")
      return

    state = self.adapter.get_playstate()

    if state is PlayState.PLAYING:
      self.adapter.pause()

    elif state is PlayState.PAUSED:
      self.adapter.resume()

    elif state is PlayState.STOPPED:
      self.adapter.play()

  @log_trace
  def Stop(self):
    if not self.CanControl:
      logging.debug(f"{self.INTERFACE}.Stop not allowed")
      return

    self.adapter.stop()

  @log_trace
  def Play(self):
    if not self.CanPlay:
      logging.debug(f"{self.INTERFACE}.Play not allowed")
      return

    state = self.adapter.get_playstate()

    if state is PlayState.PAUSED:
      self.adapter.resume()

    else:
      self.adapter.play()

  @log_trace
  def Seek(self, offset: Position):
    if not self.CanSeek:
      logging.debug(f"{self.INTERFACE}.Seek not allowed")
      return

    current_position = self.adapter.get_current_position()
    new_position = current_position + offset

    if new_position < BEGINNING:
      new_position = BEGINNING

    self.adapter.seek(new_position)

  @log_trace
  def SetPosition(self, track_id: str, position: Position):
    if not self.CanSeek:
      logging.debug(f"{self.INTERFACE}.SetPosition not allowed")
      return

    self.adapter.seek(position, track_id=track_id)

    # metadata = self.adapter.metadata()
    # current_track: Optional[Track] = None

    ##use metadata from adapter if available
    # if metadata \
    # and 'mpris:trackid' in metadata \
    # and 'mpris:length' in metadata:
    # current_track = Track(
    # track_id=metadata['mpris:trackid'],
    # length=metadata['mpris:length']
    # )

    ##if no metadata, build metadata from Track interface
    # else:
    # current_track = self.adapter.get_current_track()

    # if current_track is None:
    # return

    # if track_id != current_track.track_id:
    # return

    # if position < BEGINNING:
    # return

    # if current_track.length < position:
    # return

    # self.adapter.seek(position, track_id=track_id)

  @log_trace
  def OpenUri(self, uri: str):
    if not self.CanControl:
      logging.debug(f"{self.INTERFACE}.OpenUri not allowed")
      return

    # NOTE Check if URI has MIME type known to the backend, if MIME support
    # is added to the backend.
    self.adapter.open_uri(uri)

  @property
  @log_trace
  def PlaybackStatus(self) -> str:
    state = self.adapter.get_playstate()
    return state.value.title()

  @property
  @log_trace
  def LoopStatus(self) -> str:
    if not self.adapter.is_repeating():
      return LoopStatus.NONE

    elif not self.adapter.is_playlist():
      return LoopStatus.TRACK

    else:
      return LoopStatus.PLAYLIST

  @LoopStatus.setter
  @log_trace
  def LoopStatus(self, value: str):
    if not self.CanControl:
      logging.debug(f"Setting {self.INTERFACE}.LoopStatus not allowed")
      return

    logging.debug(f"Setting {self.INTERFACE}.LoopStatus to {value}")

    self.adapter.set_loop_status(value)
    # if value == "None":
    # self.core.tracklist.set_repeat(False)
    # self.core.tracklist.set_single(False)
    # elif value == "Track":
    # self.core.tracklist.set_repeat(True)
    # self.core.tracklist.set_single(True)
    # elif value == "Playlist":
    # self.core.tracklist.set_repeat(True)
    # self.core.tracklist.set_single(False)

  @property
  @log_trace
  def Rate(self) -> Rate:
    return self.adapter.get_rate()

  @Rate.setter
  @log_trace
  def Rate(self, value: Rate):
    if not self.CanControl:
      logging.debug(f"Setting {self.INTERFACE}.Rate not allowed")
      return

    self.adapter.set_rate(value)

    if value == PAUSE_RATE:
      self.Pause()

  @property
  @log_trace
  def Shuffle(self) -> bool:
    return self.adapter.get_shuffle()

  @Shuffle.setter
  @log_trace
  def Shuffle(self, value: bool):
    if not self.CanControl:
      logging.debug(f"Setting {self.INTERFACE}.Shuffle not allowed")
      return

    logging.debug(f"Setting {self.INTERFACE}.Shuffle to {value}")
    self.adapter.set_shuffle(value)

  @property
  @log_trace
  def Metadata(self) -> Metadata:
    # prefer adapter's metadata to building our own
    metadata: DbusMetadata = self._dbus_metadata()

    if metadata:
      return metadata

    # build metadata if no metadata supplied by adapter
    logging.debug(f"Building {self.INTERFACE}.Metadata")

    track = self.adapter.get_current_track()
    stream_title = self.adapter.get_stream_title()

    if track is None:
      return DEFAULT_METADATA

    track_id = track.track_id
    metadata = {"mpris:trackid": Variant("o", track_id)}

    if track.length:
      metadata["mpris:length"] = Variant("x", track.length)

    if track.uri:
      metadata["xesam:url"] = Variant("s", track.uri)

    if stream_title or track.name:
      metadata["xesam:title"] = Variant("s", stream_title or track.name)

    if track.artists:
      artists = list(track.artists)
      artists.sort(key=lambda a: a.name or "")
      metadata["xesam:artist"] = Variant("as", [a.name for a in artists if a.name])

    if track.album and track.album.name:
      metadata["xesam:album"] = Variant("s", track.album.name)

    if track.album and track.album.artists:
      artists = list(track.album.artists)
      artists.sort(key=lambda a: a.name or "")
      metadata["xesam:albumArtist"] = Variant(
        "as", [a.name for a in artists if a.name]
      )

    art_url = self._get_art_url(track)

    if art_url:
      metadata["mpris:artUrl"] = Variant("s", art_url)

    if track.disc_no:
      metadata["xesam:discNumber"] = Variant("i", track.disc_no)

    if track.track_no:
      metadata["xesam:trackNumber"] = Variant("i", track.track_no)

    return metadata

  @property
  @log_trace
  def Volume(self) -> Volume:
    mute = self.adapter.is_mute()
    volume = self.adapter.get_volume()

    if volume is None or mute is True:
      return MUTE_VOL

    return volume

  @Volume.setter
  @log_trace
  def Volume(self, value: Volume):
    if not self.CanControl:
      logging.debug(f"Setting {self.INTERFACE}.Volume not allowed")
      return

    if value is None:
      return

    if value < MUTE_VOL:
      value = MUTE_VOL

    elif value > MAX_VOL:
      value = MAX_VOL

    self.adapter.set_volume(value)

    if value > MUTE_VOL:
      self.adapter.set_mute(False)

    elif value == MUTE_VOL:
      self.adapter.set_mute(True)

  @property
  @log_trace
  def Position(self) -> Position:
    return self.adapter.get_current_position()

  @property
  @log_trace
  def MinimumRate(self) -> Rate:
    rate = self.adapter.get_minimum_rate()

    if rate is None:
      return MIN_RATE

    return rate

  @property
  @log_trace
  def MaximumRate(self) -> Rate:
    rate = self.adapter.get_minimum_rate()

    if rate is None:
      return MAX_RATE

    return rate

  @property
  @log_trace
  def CanGoNext(self) -> bool:
    # if not self.CanControl:
    # return False

    return self.adapter.can_go_next()

  @property
  @log_trace
  def CanGoPrevious(self) -> bool:
    # if not self.CanControl:
    # return False

    return self.adapter.can_go_previous()

  @property
  @log_trace
  def CanPlay(self) -> bool:
    # if not self.CanControl:
    # return False

    return self.adapter.can_play()

  @property
  @log_trace
  def CanPause(self) -> bool:
    return self.adapter.can_pause()
    # if not self.CanControl:
    # return False

    # return True

  @property
  @log_trace
  def CanSeek(self) -> bool:
    return self.adapter.can_seek()
    # if not self.CanControl:
    # return False

    # return True

  @property
  @log_trace
  def CanControl(self) -> bool:
    return self.adapter.can_control()
