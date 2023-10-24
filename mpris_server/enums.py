from __future__ import annotations

from enum import StrEnum, auto
from typing import Self

from strenum import StrEnum


class Access(StrEnum):
  read = auto()
  readwrite = auto()


class Arg(StrEnum):
  AfterTrack = auto()
  CurrentTrack = auto()
  Index = auto()
  MaxCount = auto()
  Metadata = auto()
  Offset = auto()
  Order = auto()
  Playlist = auto()
  PlaylistId = auto()
  Playlists = auto()
  Position = auto()
  ReverseOrder = auto()
  SetAsCurrent = auto()
  TrackId = auto()
  TrackIds = auto()
  Tracks = auto()
  Uri = auto()


class BusType(StrEnum):
  session = auto()
  system = auto()
  default = session


class Direction(StrEnum):
  In = 'in'
  out = auto()


class LoopStatus(StrEnum):
  NONE: str = 'None'
  TRACK: str = 'Track'
  PLAYLIST: str = 'Playlist'


class Method(StrEnum):
  ActivatePlaylist = auto()
  AddTrack = auto()
  GetPlaylists = auto()
  GetTracksMetadata = auto()
  GoTo = auto()
  Next = auto()
  OpenUri = auto()
  Pause = auto()
  Play = auto()
  PlayPause = auto()
  Previous = auto()
  Quit = auto()
  Raise = auto()
  RemoveTrack = auto()
  Seek = auto()
  SetPosition = auto()
  Stop = auto()


class Property(StrEnum):
  ActivePlaylist = auto()
  CanControl = auto()
  CanEditTracks = auto()
  CanGoNext = auto()
  CanGoPrevious = auto()
  CanPause = auto()
  CanPlay = auto()
  CanQuit = auto()
  CanRaise = auto()
  CanSeek = auto()
  CanSetFullscreen = auto()
  DesktopEntry = auto()
  Fullscreen = auto()
  HasTrackList = auto()
  Identity = auto()
  LoopStatus = auto()
  MaximumRate = auto()
  Metadata = auto()
  MinimumRate = auto()
  Orderings = auto()
  PlaybackStatus = auto()
  PlaylistCount = auto()
  Position = auto()
  Rate = auto()
  Shuffle = auto()
  SupportedMimeTypes = auto()
  SupportedUriSchemes = auto()
  Tracks = auto()
  Volume = auto()


class Signal(StrEnum):
  PlaylistChanged = auto()
  Seeked = auto()
  TrackAdded = auto()
  TrackListReplaced = auto()
  TrackMetadataChanged = auto()
  TrackRemoved = auto()
