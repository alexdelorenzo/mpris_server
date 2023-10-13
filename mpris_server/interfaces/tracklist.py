from __future__ import annotations

from typing import ClassVar

from pydbus.generic import signal

from .interface import MprisInterface
from ..base import DbusObj, DbusTypes, NoTrack, ROOT_INTERFACE
from ..enums import Access, Arg, Direction, Method, Property, Signal
from ..mpris.metadata import Metadata


class TrackList(MprisInterface):
  __doc__ = f"""
  <node>
    <interface name="{ROOT_INTERFACE}.TrackList">
      <method name="{Method.GetTracksMetadata}">
        <arg name="{Arg.TrackIds}" type="{DbusTypes.OBJ_ARRAY}" direction="{Direction.In}"/>
        <arg name="{Arg.Metadata}" type="{DbusTypes.METADATA_ARRAY}" direction="{Direction.out}"/>
      </method>
      <method name="{Method.AddTrack}">
        <arg name="{Arg.Uri}" type="{DbusTypes.STRING}" direction="{Direction.In}"/>
        <arg name="{Arg.AfterTrack}" type="{DbusTypes.OBJ}" direction="{Direction.In}"/>
        <arg name="{Arg.SetAsCurrent}" type="{DbusTypes.BOOLEAN}" direction="{Direction.In}"/>
      </method>
      <method name="{Method.RemoveTrack}">
        <arg name="{Arg.TrackId}" type="{DbusTypes.OBJ}" direction="{Direction.In}"/>
      </method>
      <method name="{Method.GoTo}">
        <arg name="{Arg.TrackId}" type="{DbusTypes.OBJ}" direction="{Direction.In}"/>
      </method>
      <signal name="{Signal.TrackListReplaced}">
        <arg name="{Arg.Tracks}" type="{DbusTypes.OBJ_ARRAY}"/>
        <arg name="{Arg.CurrentTrack}" type="{DbusTypes.OBJ}"/>
      </signal>
      <signal name="{Signal.TrackAdded}">
        <arg name="{Arg.Metadata}" type="{DbusTypes.METADATA}"/>
        <arg name="{Arg.AfterTrack}" type="{DbusTypes.OBJ}"/>
      </signal>
      <signal name="{Signal.TrackRemoved}">
        <arg name="{Arg.TrackId}" type="{DbusTypes.OBJ}"/>
      </signal>
      <signal name="{Signal.TrackMetadataChanged}">
        <arg name="{Arg.TrackId}" type="{DbusTypes.OBJ}"/>
        <arg name="{Arg.Metadata}" type="{DbusTypes.METADATA}"/>
      </signal>
      <property name="{Property.Tracks}" type="{DbusTypes.OBJ_ARRAY}" access="{Access.read}"/>
      <property name="{Property.CanEditTracks}" type="{DbusTypes.BOOLEAN}" access="{Access.read}"/>
    </interface>
  </node>
  """

  INTERFACE: ClassVar[str] = f"{ROOT_INTERFACE}.TrackList"

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
