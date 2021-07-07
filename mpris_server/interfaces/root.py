from __future__ import annotations
from pathlib import PurePath
import logging

from ..base import ROOT_INTERFACE, NAME, Paths
from ..types import Final
from .interface import MprisInterface, log_trace


NO_SUFFIX: Final[str] = ''
DESKTOP_EXT: Final[str] = '.desktop'


class Root(MprisInterface):
  """
  <node>
    <interface name="org.mpris.MediaPlayer2">
      <method name="Raise"/>
      <method name="Quit"/>
      <property name="CanQuit" type="b" access="read"/>
      <property name="CanRaise" type="b" access="read"/>
      <property name="Fullscreen" type="b" access="readwrite"/>
      <property name="CanSetFullscreen" type="b" access="read"/>
      <property name="HasTrackList" type="b" access="read"/>
      <property name="Identity" type="s" access="read"/>
      <property name="DesktopEntry" type="s" access="read"/>
      <property name="SupportedUriSchemes" type="as" access="read"/>
      <property name="SupportedMimeTypes" type="as" access="read"/>
    </interface>
  </node>
  """

  INTERFACE: Final[str] = ROOT_INTERFACE

  @log_trace
  def Raise(self):
    self.adapter.set_raise(True)

  @log_trace
  def Quit(self):
    self.adapter.quit()

  @property
  @log_trace
  def Fullscreen(self) -> bool:
    return self.adapter.get_fullscreen()

  @Fullscreen.setter
  @log_trace
  def Fullscreen(self, value):
    self.adapter.set_fullscreen(value)

  @property
  @log_trace
  def DesktopEntry(self) -> str:
    path: Paths = self.adapter.get_desktop_entry()
    return get_desktop_entry(path)

  @property
  @log_trace
  def SupportedUriSchemes(self) -> list[str]:
    return self.adapter.get_uri_schemes()

  @property
  @log_trace
  def SupportedMimeTypes(self) -> list[str]:
    return self.adapter.get_mime_types()

  @property
  @log_trace
  def Identity(self) -> str:
    return self.name

  @property
  @log_trace
  def CanQuit(self) -> bool:
    return self.adapter.can_quit()

  @property
  @log_trace
  def CanRaise(self) -> bool:
    return self.adapter.can_raise()

  @property
  @log_trace
  def CanSetFullscreen(self) -> bool:
    return self.adapter.can_fullscreen()

  @property
  @log_trace
  def HasTrackList(self) -> bool:
    return self.adapter.has_tracklist()


def get_desktop_entry(path: Paths) -> str:
  # mpris requires stripped suffix
  if isinstance(path, PurePath):
    path = path.with_suffix(NO_SUFFIX)

  name = str(path)

  if name.endswith(DESKTOP_EXT):
    name = name.rstrip(DESKTOP_EXT)

  return name
