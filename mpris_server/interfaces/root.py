from __future__ import annotations
from os import PathLike
import logging

from ..base import INTERFACE as _INTERFACE, NAME
from .interface import MprisInterface, Paths
from ..types import Final


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

  INTERFACE = _INTERFACE

  def Raise(self):
    logging.debug(f"{self.INTERFACE}.Raise called")
    self.adapter.set_raise(True)

  def Quit(self):
    logging.debug(f"{self.INTERFACE}.Quit called")
    self.adapter.quit()

  @property
  def Fullscreen(self):
    logging.debug(f"Getting {self.INTERFACE}.Fullscreen")
    return self.adapter.get_fullscreen()

  @Fullscreen.setter
  def Fullscreen(self, value):
    logging.debug(f"Setting {self.INTERFACE}.Fullscreen to {value}")
    self.adapter.set_fullscreen(value)

  @property
  def DesktopEntry(self):
    logging.debug(f"Getting {self.INTERFACE}.DesktopEntry")
    path: Paths = self.adapter.get_desktop_entry()

    if isinstance(path, PathLike):
      # mpris requires stripped suffix
      path = path.with_suffix('')

    name = str(path)

    if name.endswith(DESKTOP_EXT):
      name = name.rstrip(DESKTOP_EXT)

    return name

  @property
  def SupportedUriSchemes(self):
    logging.debug(f"Getting {self.INTERFACE}.SupportedUriSchemes")
    return self.adapter.get_uri_schemes()

  @property
  def SupportedMimeTypes(self):
    logging.debug(f"Getting {self.INTERFACE}.SupportedMimeTypes")
    return self.adapter.get_mime_types()

  @property
  def Identity(self) -> str:
    return self.name

  @property
  def CanQuit(self) -> bool:
    return self.adapter.can_quit()

  @property
  def CanRaise(self) -> bool:
    return self.adapter.can_raise()

  @property
  def CanSetFullscreen(self) -> bool:
    return self.adapter.can_fullscreen()

  @property
  def HasTrackList(self) -> bool:
    return self.adapter.has_tracklist()
