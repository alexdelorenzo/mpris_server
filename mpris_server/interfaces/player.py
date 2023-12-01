from __future__ import annotations

import logging
from fractions import Fraction
from typing import ClassVar, Final

from pydbus.generic import signal

from .interface import MprisInterface, log_trace
from ..base import BEGINNING, DbusObj, DbusTypes, Interface, MAX_RATE, MAX_VOLUME, MIN_RATE, MUTE_VOLUME, \
  PAUSE_RATE, PlayState, Position, Rate, Track, Volume
from ..enums import Access, Arg, Direction, LoopStatus, Method, Property, Signal
from ..mpris.metadata import Metadata, MetadataEntries, create_metadata_from_track, get_dbus_metadata, update_metadata


log = logging.getLogger(__name__)

ERR_NOT_ENOUGH_METADATA: Final[str] = \
  "Couldn't find enough metadata, please implement metadata() or get_stream_title() and get_current_track() methods.`"


class Player(MprisInterface):
  INTERFACE: ClassVar[Interface] = Interface.Player

  __doc__: Final[str] = f"""
  <node>
    <interface name="{INTERFACE}">
      <method name="{Method.Next}"/>
      <method name="{Method.Pause}"/>
      <method name="{Method.PlayPause}"/>
      <method name="{Method.Play}"/>
      <method name="{Method.Previous}"/>
      <method name="{Method.Stop}"/>
      <method name="{Method.OpenUri}">
        <arg name="{Arg.Uri}" type="{DbusTypes.STRING}" direction="{Direction.IN}"/>
      </method>
        <method name="{Method.Seek}">
        <arg name="{Arg.Offset}" type="{DbusTypes.INT64}" direction="{Direction.IN}"/>
      </method>
      <method name="{Method.SetPosition}">
        <arg name="{Arg.TrackId}" type="{DbusTypes.OBJ}" direction="{Direction.IN}"/>
        <arg name="{Arg.Position}" type="{DbusTypes.INT64}" direction="{Direction.IN}"/>
      </method>

      <property name="{Property.CanControl}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.CanGoNext}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.CanGoPrevious}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.CanPause}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.CanPlay}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.CanSeek}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.LoopStatus}" type="{DbusTypes.STRING}" access="{Access.READWRITE}"/>
      <property name="{Property.MaximumRate}" type="{DbusTypes.DOUBLE}" access="{Access.READ}"/>
      <property name="{Property.Metadata}" type="{DbusTypes.METADATA}" access="{Access.READ}"/>
      <property name="{Property.MinimumRate}" type="{DbusTypes.DOUBLE}" access="{Access.READ}"/>
      <property name="{Property.PlaybackStatus}" type="{DbusTypes.STRING}" access="{Access.READ}"/>
      <property name="{Property.Position}" type="{DbusTypes.INT64}" access="{Access.READ}"/>
      <property name="{Property.Rate}" type="{DbusTypes.DOUBLE}" access="{Access.READWRITE}"/>
      <property name="{Property.Shuffle}" type="{DbusTypes.BOOLEAN}" access="{Access.READWRITE}"/>
      <property name="{Property.Volume}" type="{DbusTypes.DOUBLE}" access="{Access.READWRITE}"/>

      <signal name="{Signal.Seeked}">
        <arg name="{Arg.Position}" type="{DbusTypes.INT64}"/>
      </signal>
    </interface>
  </node>
  """

  Seeked: Final[signal] = signal()

  def _get_metadata(self) -> Metadata | None:
    if metadata := self.adapter.metadata():
      return get_dbus_metadata(metadata)

    return None

  def _get_basic_metadata(self, track: Track) -> Metadata:
    metadata: Metadata = Metadata()

    if name := self.adapter.get_stream_title():
      update_metadata(metadata, MetadataEntries.TITLE, name)

    if art_url := self._get_art_url(track):
      update_metadata(metadata, MetadataEntries.ART_URL, art_url)

    return metadata

  def _get_art_url(self, track: DbusObj | Track | None) -> str:
    return self.adapter.get_art_url(track)

  @property
  @log_trace
  def CanControl(self) -> bool:
    return self.adapter.can_control()

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
  def CanPause(self) -> bool:
    return self.adapter.can_pause()
    # if not self.CanControl:
    # return False

    # return True

  @property
  @log_trace
  def CanPlay(self) -> bool:
    # if not self.CanControl:
    # return False

    return self.adapter.can_play()

  @property
  @log_trace
  def CanSeek(self) -> bool:
    return self.adapter.can_seek()
    # if not self.CanControl:
    # return False

    # return True

  @property
  @log_trace
  def LoopStatus(self) -> LoopStatus:
    if not self.adapter.is_repeating():
      return LoopStatus.NONE

    elif not self.adapter.is_playlist():
      return LoopStatus.TRACK

    else:
      return LoopStatus.PLAYLIST

  @LoopStatus.setter
  @log_trace
  def LoopStatus(self, value: LoopStatus):
    if not self.CanControl:
      log.debug(f"Setting {self.INTERFACE}.{Property.LoopStatus} not allowed")
      return

    log.debug(f"Setting {self.INTERFACE}.{Property.LoopStatus} to {value}")

    self.adapter.set_loop_status(value)

  @property
  @log_trace
  def MinimumRate(self) -> Rate:
    if rate := self.adapter.get_minimum_rate():
      return rate

    return MIN_RATE

  @property
  @log_trace
  def MaximumRate(self) -> Rate:
    if rate := self.adapter.get_maximum_rate():
      return rate

    return MAX_RATE

  @property
  @log_trace
  def Metadata(self) -> Metadata:
    # prefer adapter's metadata to building our own
    if metadata := self._get_metadata():
      return metadata

    # build metadata if no metadata supplied by adapter
    log.debug(f"Building {self.INTERFACE}.{Property.Metadata}")

    track = self.adapter.get_current_track()
    metadata: Metadata = self._get_basic_metadata(track)

    if not track:
      log.warning(ERR_NOT_ENOUGH_METADATA)
      return metadata

    return create_metadata_from_track(track, metadata)

  @property
  @log_trace
  def PlaybackStatus(self) -> PlayState:
    state = self.adapter.get_playstate()
    return state.value.title()

  @property
  @log_trace
  def Position(self) -> Position:
    return self.adapter.get_current_position()

  @property
  @log_trace
  def Rate(self) -> Rate:
    return self.adapter.get_rate()

  @Rate.setter
  @log_trace
  def Rate(self, value: Rate):
    if not self.CanControl:
      log.debug(f"Setting {self.INTERFACE}.Rate not allowed")
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
      log.debug(f"Setting {self.INTERFACE}.{Property.Shuffle} not allowed")
      return

    log.debug(f"Setting {self.INTERFACE}.{Property.Shuffle} to {value}")
    self.adapter.set_shuffle(value)

  @property
  @log_trace
  def Volume(self) -> Volume:
    if self.adapter.is_mute():
      return MUTE_VOLUME

    match volume := self.adapter.get_volume():
      case Volume():
        return volume

      case _ if not volume:
        return MUTE_VOLUME

    return volume

  @Volume.setter
  @log_trace
  def Volume(self, value: Volume | None):
    if not self.CanControl:
      log.debug(f"Setting {self.INTERFACE}.{Property.Volume} not allowed")
      return

    match volume := value:
      case None:
        return

      case Volume() | int() | float() | Fraction():
        volume = Volume(volume)

      case unknown:
        log.warning(f"Unknown volume type: {type(unknown)}, continuing anyway.")

    if volume < MUTE_VOLUME:
      volume = MUTE_VOLUME

    elif volume > MAX_VOLUME:
      volume = MAX_VOLUME

    self.adapter.set_volume(volume)

    if volume > MUTE_VOLUME:
      self.adapter.set_mute(False)

    elif volume <= MUTE_VOLUME:
      self.adapter.set_mute(True)

  @log_trace
  def Next(self):
    if not self.CanGoNext:
      log.debug(f"{self.INTERFACE}.{Method.Next} not allowed")
      return

    self.adapter.next()

  @log_trace
  def OpenUri(self, uri: str):
    if not self.CanControl:
      log.debug(f"{self.INTERFACE}.{Method.OpenUri} not allowed")
      return

    # NOTE Check if URI has MIME type known to the backend, if MIME support
    # is added to the backend.
    self.adapter.open_uri(uri)

  @log_trace
  def Previous(self):
    if not self.CanGoPrevious:
      log.debug(f"{self.INTERFACE}.{Method.Previous} not allowed")
      return

    self.adapter.previous()

  @log_trace
  def Pause(self):
    if not self.CanPause:
      log.debug(f"{self.INTERFACE}.{Method.Pause} not allowed")
      return

    self.adapter.pause()

  @log_trace
  def Play(self):
    if not self.CanPlay:
      log.debug(f"{self.INTERFACE}.{Method.Play} not allowed")
      return

    match self.adapter.get_playstate():
      case PlayState.PAUSED:
        self.adapter.resume()

      case _:
        self.adapter.play()

  @log_trace
  def PlayPause(self):
    if not self.CanPause:
      log.debug(f"{self.INTERFACE}.{Method.PlayPause} not allowed")
      return

    match self.adapter.get_playstate():
      case PlayState.PLAYING:
        self.adapter.pause()

      case PlayState.PAUSED:
        self.adapter.resume()

      case PlayState.STOPPED:
        self.adapter.play()

  @log_trace
  def Seek(self, offset: Position):
    if not self.CanSeek:
      log.debug(f"{self.INTERFACE}.{Method.Seek} not allowed")
      return

    current_position = self.adapter.get_current_position()
    new_position = current_position + offset

    if new_position < BEGINNING:
      new_position = BEGINNING

    self.adapter.seek(new_position)

  @log_trace
  def SetPosition(self, track_id: str, position: Position):
    if not self.CanSeek:
      log.debug(f"{self.INTERFACE}.{Method.SetPosition} not allowed")
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
  def Stop(self):
    if not self.CanControl:
      log.debug(f"{self.INTERFACE}.{Method.Stop} not allowed")
      return

    self.adapter.stop()
