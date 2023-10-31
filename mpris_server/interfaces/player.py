from __future__ import annotations

import logging
from typing import ClassVar, Final

from gi.repository.GLib import Variant
from pydbus.generic import signal

from .interface import MprisInterface, log_trace
from ..base import Artist, BEGINNING, DbusMetadata, DbusTypes, Interfaces, MAX_RATE, MAX_VOL, MIN_RATE, MUTE_VOL, \
  PAUSE_RATE, PlayState, Position, Rate, Track, Volume
from ..enums import Access, Arg, Direction, LoopStatus, Method, Property, Signal
from ..mpris.metadata import Metadata, MetadataEntries, MprisMetadata, get_dbus_metadata


NO_NAME: Final[str] = ''

log = logging.getLogger(__name__)


class Player(MprisInterface):
  INTERFACE: ClassVar[Interfaces] = Interfaces.Player

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

  def _get_metadata(self) -> Metadata | None:
    if metadata := self.adapter.metadata():
      return get_dbus_metadata(metadata)

    return None

  def _get_art_url(self, track: Track) -> str:
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

    metadata: Metadata = {}

    track = self.adapter.get_current_track()
    stream_title = self.adapter.get_stream_title()

    if stream_title or track and track.name:
      metadata[MetadataEntries.TITLE] = Variant(
        DbusTypes.STRING,
        stream_title or track.name,
      )

    if track is None:
      log.warning(
        "Couldn't find metadata, please implement metadata() or get_stream_title() and get_current_track() methods."
      )
      return metadata

    metadata[MetadataEntries.TRACK_ID] = Variant(
      DbusTypes.OBJ,
      track.track_id,
    )

    if track.length:
      metadata[MetadataEntries.LENGTH] = Variant(
        DbusTypes.INT64,
        track.length,
      )

    if track.uri:
      metadata[MetadataEntries.URL] = Variant(
        DbusTypes.STRING,
        track.uri,
      )

    if track.artists:
      artists = list(track.artists)
      artists.sort(key=sort_names)

      metadata[MetadataEntries.ARTISTS] = Variant(
        DbusTypes.STRING_ARRAY,
        [a.name for a in artists if a.name],
      )

    if track.album and track.album.name:
      metadata[MetadataEntries.ALBUM] = Variant(
        DbusTypes.STRING,
        track.album.name,
      )

    if track.album and track.album.artists:
      artists = list(track.album.artists)
      artists.sort(key=sort_names)

      metadata[MetadataEntries.ALBUM_ARTISTS] = Variant(
        DbusTypes.STRING_ARRAY,
        [a.name for a in artists if a.name],
      )

    art_url = self._get_art_url(track)

    if art_url:
      metadata[MetadataEntries.ART_URL] = Variant(
        DbusTypes.STRING,
        art_url,
      )

    if track.disc_no:
      metadata[MetadataEntries.DISC_NUMBER] = Variant(
        DbusTypes.INT32,
        track.disc_no,
      )

    if track.track_no:
      metadata[MetadataEntries.TRACK_NUMBER] = Variant(
        DbusTypes.INT32,
        track.track_no,
      )

    return metadata

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
      return MUTE_VOL

    if not (volume := self.adapter.get_volume()):
      return MUTE_VOL

    return volume

  @Volume.setter
  @log_trace
  def Volume(self, value: Volume):
    if not self.CanControl:
      log.debug(f"Setting {self.INTERFACE}.{Property.Volume} not allowed")
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

    elif value <= MUTE_VOL:
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


def sort_names(artist: Artist) -> str:
  return artist.name or NO_NAME
