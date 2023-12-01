from __future__ import annotations

from typing import ClassVar, Final

from pydbus.generic import signal

from .interface import MprisInterface
from ..base import DbusObj, DbusTypes, Interface, NoTrack
from ..enums import Access, Arg, Direction, Method, Property, Signal
from ..mpris.metadata import Metadata


class TrackList(MprisInterface):
  INTERFACE: ClassVar[Interface] = Interface.TrackList

  __doc__: Final[str] = f"""
  <node>
    <interface name="{INTERFACE}">
      <method name="{Method.AddTrack}">
        <arg name="{Arg.Uri}" type="{DbusTypes.STRING}" direction="{Direction.IN}"/>
        <arg name="{Arg.AfterTrack}" type="{DbusTypes.OBJ}" direction="{Direction.IN}"/>
        <arg name="{Arg.SetAsCurrent}" type="{DbusTypes.BOOLEAN}" direction="{Direction.IN}"/>
      </method>
      <method name="{Method.GetTracksMetadata}">
        <arg name="{Arg.TrackIds}" type="{DbusTypes.OBJ_ARRAY}" direction="{Direction.IN}"/>
        <arg name="{Arg.Metadata}" type="{DbusTypes.METADATA_ARRAY}" direction="{Direction.OUT}"/>
      </method>
      <method name="{Method.GoTo}">
        <arg name="{Arg.TrackId}" type="{DbusTypes.OBJ}" direction="{Direction.IN}"/>
      </method>
      <method name="{Method.RemoveTrack}">
        <arg name="{Arg.TrackId}" type="{DbusTypes.OBJ}" direction="{Direction.IN}"/>
      </method>

      <property name="{Property.CanEditTracks}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.Tracks}" type="{DbusTypes.OBJ_ARRAY}" access="{Access.READ}"/>

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
    </interface>
  </node>
  """

  TrackAdded: Final[signal] = signal()
  TrackListReplaced: Final[signal] = signal()
  TrackMetadataChanged: Final[signal] = signal()
  TrackRemoved: Final[signal] = signal()

  @property
  def CanEditTracks(self) -> bool:
    return self.adapter.can_edit_tracks()

  @property
  def Tracks(self) -> list[DbusObj]:
    if not (tracks := self.adapter.get_tracks()):
      return [NoTrack]

    return tracks

  def AddTrack(
    self,
    uri: str,
    after_track: DbusObj,
    set_as_current: bool
  ):
    self.adapter.add_track(uri, after_track, set_as_current)

  def GetTracksMetadata(self, track_ids: list[DbusObj]) -> list[Metadata]:
    return self.adapter.get_tracks_metadata(track_ids)

  def GoTo(self, track_id: DbusObj):
    self.adapter.go_to(track_id)

  def RemoveTrack(self, track_id: DbusObj):
    self.adapter.remove_track(track_id)



