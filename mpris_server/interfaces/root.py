from __future__ import annotations

from pathlib import PurePath
from typing import ClassVar, Final

from .interface import MprisInterface, log_trace
from ..base import DbusTypes, Interface, Paths
from ..enums import Access, Method, Property


NO_SUFFIX: Final[str] = ''
DESKTOP_EXT: Final[str] = '.desktop'
NO_DESKTOP_ENTRY: Final[str] = ''


class Root(MprisInterface):
  INTERFACE: ClassVar[Interface] = Interface.Root

  __doc__: Final[str] = f"""
  <node>
    <interface name="{INTERFACE}">
      <method name="{Method.Quit}"/>
      <method name="{Method.Raise}"/>

      <property name="{Property.CanQuit}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.CanRaise}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.CanSetFullscreen}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.DesktopEntry}" type="{DbusTypes.STRING}" access="{Access.READ}"/>
      <property name="{Property.Fullscreen}" type="{DbusTypes.BOOLEAN}" access="{Access.READWRITE}"/>
      <property name="{Property.HasTrackList}" type="{DbusTypes.BOOLEAN}" access="{Access.READ}"/>
      <property name="{Property.Identity}" type="{DbusTypes.STRING}" access="{Access.READ}"/>
      <property name="{Property.SupportedMimeTypes}" type="{DbusTypes.STRING_ARRAY}" access="{Access.READ}"/>
      <property name="{Property.SupportedUriSchemes}" type="{DbusTypes.STRING_ARRAY}" access="{Access.READ}"/>
    </interface>
  </node>
  """

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
  def DesktopEntry(self) -> str:
    path: Paths = self.adapter.get_desktop_entry()
    return get_desktop_entry(path)

  @property
  @log_trace
  def Fullscreen(self) -> bool:
    return self.adapter.get_fullscreen()

  @Fullscreen.setter
  @log_trace
  def Fullscreen(self, value: bool):
    self.adapter.set_fullscreen(value)

  @property
  @log_trace
  def HasTrackList(self) -> bool:
    return self.adapter.has_tracklist()

  @property
  @log_trace
  def Identity(self) -> str:
    return self.name

  @property
  @log_trace
  def SupportedMimeTypes(self) -> list[str]:
    return self.adapter.get_mime_types()

  @property
  @log_trace
  def SupportedUriSchemes(self) -> list[str]:
    return self.adapter.get_uri_schemes()

  @log_trace
  def Quit(self):
    self.adapter.quit()

  @log_trace
  def Raise(self):
    self.adapter.set_raise(True)


def get_desktop_entry(path: Paths | None) -> str:
  if not path:
    return NO_DESKTOP_ENTRY

  # mpris requires stripped suffix
  if isinstance(path, PurePath):
    path = path.with_suffix(NO_SUFFIX)

  name = str(path)

  if name.endswith(DESKTOP_EXT):
    name = name.rstrip(DESKTOP_EXT)

  return name
