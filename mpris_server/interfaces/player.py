from __future__ import annotations
from typing import Optional
import logging

from gi.repository.GLib import Variant
from pydbus.generic import signal

from ..types import Final
from ..base import PlayState, MUTE_VOL, MAX_VOL, PAUSE_RATE, BEGINNING, \
  Microseconds, RateDecimal, VolumeDecimal, MAX_RATE, MIN_RATE, \
  Track, ROOT_INTERFACE
from ..mpris.metadata import Metadata, DbusMetadata, DbusTypes, \
  get_dbus_metadata, METADATA_TYPES, DEFAULT_METADATA, \
  ValidMetadata, MetadataObj
from .interface import MprisInterface, log_trace


class LoopStatus:
  NONE: Final[str] = 'None'
  TRACK: Final[str] = 'Track'
  PLAYLIST: Final[str] = 'Playlist'


class Player(MprisInterface):
  """
  <node>
    <interface name="org.mpris.MediaPlayer2.Player">
      <method name="Next"/>
      <method name="Previous"/>
      <method name="Pause"/>
      <method name="PlayPause"/>
      <method name="Stop"/>
      <method name="Play"/>
      <method name="Seek">
        <arg name="Offset" type="x" direction="in"/>
      </method>
      <method name="SetPosition">
        <arg name="TrackId" type="o" direction="in"/>
        <arg name="Position" type="x" direction="in"/>
      </method>
      <method name="OpenUri">
        <arg name="Uri" type="s" direction="in"/>
      </method>
      <signal name="Seeked">
        <arg name="Position" type="x"/>
      </signal>
      <property name="PlaybackStatus" type="s" access="read"/>
      <property name="LoopStatus" type="s" access="readwrite"/>
      <property name="Rate" type="d" access="readwrite"/>
      <property name="Shuffle" type="b" access="readwrite"/>
      <property name="Metadata" type="a{sv}" access="read"/>
      <property name="Volume" type="d" access="readwrite"/>
      <property name="Position" type="x" access="read"/>
      <property name="MinimumRate" type="d" access="read"/>
      <property name="MaximumRate" type="d" access="read"/>
      <property name="CanGoNext" type="b" access="read"/>
      <property name="CanGoPrevious" type="b" access="read"/>
      <property name="CanPlay" type="b" access="read"/>
      <property name="CanPause" type="b" access="read"/>
      <property name="CanSeek" type="b" access="read"/>
      <property name="CanControl" type="b" access="read"/>
    </interface>
  </node>
  """

  INTERFACE: Final[str] = f"{ROOT_INTERFACE}.Player"

  Seeked: Final[signal] = signal()

  def _dbus_metadata(self) -> Optional[DbusMetadata]:
    metadata = self.adapter.metadata()

    if metadata:
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
  def Seek(self, offset: Microseconds):
    if not self.CanSeek:
      logging.debug(f"{self.INTERFACE}.Seek not allowed")
      return

    current_position = self.adapter.get_current_position()
    new_position = current_position + offset

    if new_position < BEGINNING:
      new_position = BEGINNING

    self.adapter.seek(new_position)

  @log_trace
  def SetPosition(self, track_id: str, position: Microseconds):
    if not self.CanSeek:
      logging.debug(f"{self.INTERFACE}.SetPosition not allowed")
      return

    self.adapter.seek(position, track_id=track_id)

    #metadata = self.adapter.metadata()
    #current_track: Optional[Track] = None

    ##use metadata from adapter if available
    #if metadata \
      #and 'mpris:trackid' in metadata \
      #and 'mpris:length' in metadata:
        #current_track = Track(
            #track_id=metadata['mpris:trackid'],
            #length=metadata['mpris:length']
        #)

    ##if no metadata, build metadata from Track interface
    #else:
        #current_track = self.adapter.get_current_track()

    #if current_track is None:
        #return

    #if track_id != current_track.track_id:
        #return

    #if position < BEGINNING:
        #return

    #if current_track.length < position:
        #return

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
  def Rate(self) -> float:
      return self.adapter.get_rate()

  @Rate.setter
  @log_trace
  def Rate(self, value: RateDecimal):
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
    self.log_trace(f"Building {self.INTERFACE}.Metadata")
    track = self.adapter.get_current_track()
    stream_title = self.adapter.get_stream_title()

    if track is None:
      return DEFAULT_METADATA

    track_id = track.track_id
    res = {"mpris:trackid": Variant("o", track_id)}

    if track.length:
      res["mpris:length"] = Variant("x", track.length)

    if track.uri:
      res["xesam:url"] = Variant("s", track.uri)

    if stream_title or track.name:
      res["xesam:title"] = Variant("s", stream_title or track.name)

    if track.artists:
      artists = list(track.artists)
      artists.sort(key=lambda a: a.name or "")
      res["xesam:artist"] = Variant("as", [a.name for a in artists if a.name])

    if track.album and track.album.name:
      res["xesam:album"] = Variant("s", track.album.name)

    if track.album and track.album.artists:
      artists = list(track.album.artists)
      artists.sort(key=lambda a: a.name or "")
      res["xesam:albumArtist"] = Variant(
        "as", [a.name for a in artists if a.name]
      )

    art_url = self._get_art_url(track)

    if art_url:
      res["mpris:artUrl"] = Variant("s", art_url)

    if track.disc_no:
      res["xesam:discNumber"] = Variant("i", track.disc_no)

    if track.track_no:
      res["xesam:trackNumber"] = Variant("i", track.track_no)

    return res

  @property
  @log_trace
  def Volume(self) -> float:
    mute = self.adapter.is_mute()
    volume = self.adapter.get_volume()

    if volume is None or mute is True:
      return MUTE_VOL

    return volume

  @Volume.setter
  @log_trace
  def Volume(self, value: VolumeDecimal):
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

    elif value == MUTE_VAL:
      self.adapter.set_mute(True)

  @property
  @log_trace
  def Position(self) -> float:
    return self.adapter.get_current_position()

  @property
  @log_trace
  def MinimumRate(self) -> float:
    rate = self.adapter.get_minimum_rate()

    if rate is None:
      return MIN_RATE

    return rate

  @property
  @log_trace
  def MaximumRate(self) -> float:
    rate = self.adapter.get_minimum_rate()

    if rate is None:
      return MAX_RATE

    return rate

  @property
  @log_trace
  def CanGoNext(self) -> bool:
    #if not self.CanControl:
      #return False

    return self.adapter.can_go_next()

  @property
  @log_trace
  def CanGoPrevious(self) -> bool:
    #if not self.CanControl:
      #return False

    return self.adapter.can_go_previous()

  @property
  @log_trace
  def CanPlay(self) -> bool:
    #if not self.CanControl:
      #return False

    return self.adapter.can_play()

  @property
  @log_trace
  def CanPause(self) -> bool:
    return self.adapter.can_pause()
    #if not self.CanControl:
        #return False

    #return True

  @property
  @log_trace
  def CanSeek(self) -> bool:
    return self.adapter.can_seek()
    #if not self.CanControl:
        #return False

    #return True

  @property
  @log_trace
  def CanControl(self) -> bool:
    return self.adapter.can_control()
