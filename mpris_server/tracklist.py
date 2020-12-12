import logging
from typing import List

from pydbus.generic import signal

from .base import Metadata, DbusObj
from .interface import MprisInterface

logger = logging.getLogger(__name__)


class TrackList(MprisInterface):
  """
  <node>
    <interface name="org.mpris.MediaPlayer2.TrackList">
      <method name="GetTracksMetadata">
        <arg name="TrackIds" type="ao" direction="in"/>
        <arg name="Metadata" type="aa{sv}" direction="out"/>
      </method>
      <method name="AddTrack">
        <arg name="Uri" type="s" direction="in"/>
        <arg name="AfterTrack" type="o" direction="in"/>
        <arg name="SetAsCurrent" type="b" direction="in"/>
      </method>
      <method name="RemoveTrack">
        <arg name="TrackId" type="o" direction="in"/>
      </method>
      <method name="GoTo">
        <arg name="TrackId" type="o" direction="in"/>
      </method>
      <signal name="TrackListReplaced">
        <arg name="Tracks" type="ao"/>
        <arg name="CurrentTrack" type="o"/>
      </signal>
      <signal name="TrackAdded">
        <arg name="Metadata" type="a{sv}"/>
        <arg name="AfterTrack" type="o"/>
      </signal>
      <signal name="TrackRemoved">
        <arg name="TrackId" type="o"/>
      </signal>
      <signal name="TrackMetadataChanged">
        <arg name="TrackId" type="o"/>
        <arg name="Metadata" type="a{sv}"/>
      </signal>
      <property name="Tracks" type="ao" access="read"/>
      <property name="CanEditTracks" type="b" access="read"/>
    </interface>
  </node>
  """

  INTERFACE = "org.mpris.MediaPlayer2.TrackList"
  TrackListReplaced = signal()
  TrackAdded = signal()
  TrackRemoved = signal()
  TrackMetadataChanged = signal()

  def GetTracksMetadata(self, track_ids: List[DbusObj]) -> Metadata:
    return self.adapter.get_tracks_metadata(track_ids)

  def AddTrack(self,
               uri: str,
               after_track: DbusObj,
               set_as_current: bool):
    self.adapter.add_track(uri, after_track, set_as_current)

  def RemoveTrack(self, track_id: DbusObj):
    self.adapter.remove_track(track_id)

  def GoTo(self, track_id: DbusObj):
    self.adapter.go_to(track_id)

  @property
  def Tracks(self) -> List[DbusObj]:
    return self.adapter.get_tracks()

  @property
  def CanEditTracks(self) -> bool:
    return self.adapter.can_edit_tracks()
