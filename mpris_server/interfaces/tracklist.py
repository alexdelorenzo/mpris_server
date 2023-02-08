from __future__ import annotations
import logging
from typing import ClassVar

from pydbus.generic import signal

from ..base import DbusObj, DbusTypes, ROOT_INTERFACE, NoTrack
from ..mpris.metadata import Metadata
from ..types import Final
from .interface import MprisInterface


class TrackList(MprisInterface):
  INTERFACE: ClassVar[str] = f"{ROOT_INTERFACE}.TrackList"

  __doc__: Final[str] = f"""
  <node>
    <interface name="{INTERFACE}">
      <method name="GetTracksMetadata">
        <arg name="TrackIds" type="{DbusTypes.OBJ_ARRAY}" direction="in"/>
        <arg name="Metadata" type="{DbusTypes.METADATA_ARRAY}" direction="out"/>
      </method>
      <method name="AddTrack">
        <arg name="Uri" type="{DbusTypes.STRING}" direction="in"/>
        <arg name="AfterTrack" type="{DbusTypes.OBJ}" direction="in"/>
        <arg name="SetAsCurrent" type="{DbusTypes.BOOLEAN}" direction="in"/>
      </method>
      <method name="RemoveTrack">
        <arg name="TrackId" type="{DbusTypes.OBJ}" direction="in"/>
      </method>
      <method name="GoTo">
        <arg name="TrackId" type="{DbusTypes.OBJ}" direction="in"/>
      </method>
      <signal name="TrackListReplaced">
        <arg name="Tracks" type="{DbusTypes.OBJ_ARRAY}"/>
        <arg name="CurrentTrack" type="{DbusTypes.OBJ}"/>
      </signal>
      <signal name="TrackAdded">
        <arg name="Metadata" type="{DbusTypes.METADATA}"/>
        <arg name="AfterTrack" type="{DbusTypes.OBJ}"/>
      </signal>
      <signal name="TrackRemoved">
        <arg name="TrackId" type="{DbusTypes.OBJ}"/>
      </signal>
      <signal name="TrackMetadataChanged">
        <arg name="TrackId" type="{DbusTypes.OBJ}"/>
        <arg name="Metadata" type="{DbusTypes.METADATA}"/>
      </signal>
      <property name="Tracks" type="{DbusTypes.OBJ_ARRAY}" access="read"/>
      <property name="CanEditTracks" type="{DbusTypes.BOOLEAN}" access="read"/>
    </interface>
  </node>
  """

  TrackListReplaced = signal()
  TrackAdded = signal()
  TrackRemoved = signal()
  TrackMetadataChanged = signal()

  def GetTracksMetadata(self, track_ids: list[DbusObj]) -> list[Metadata]:
    return self.adapter.get_tracks_metadata(track_ids)

  def AddTrack(
    self,
    uri: str,
    after_track: DbusObj,
    set_as_current: bool
  ):
    self.adapter.add_track(uri, after_track, set_as_current)

  def RemoveTrack(self, track_id: DbusObj):
    self.adapter.remove_track(track_id)

  def GoTo(self, track_id: DbusObj):
    self.adapter.go_to(track_id)

  @property
  def Tracks(self) -> list[DbusObj]:
    items = self.adapter.get_tracks()

    if not items:
      return [NoTrack]

    return items

  @property
  def CanEditTracks(self) -> bool:
    return self.adapter.can_edit_tracks()
