from __future__ import annotations

from enum import auto

from strenum import LowercaseStrEnum, StrEnum


__all__ = [
  'Access',
  'Arg',
  'BusType',
  'Direction',
  'LoopStatus',
  'Method',
  'Property',
  'Signal',
]


class Access(LowercaseStrEnum):
  READ = auto()
  READWRITE = auto()


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


class BusType(LowercaseStrEnum):
  SESSION = auto()
  SYSTEM = auto()
  DEFAULT = SESSION


class Direction(LowercaseStrEnum):
  IN = auto()
  OUT = auto()


class LoopStatus(StrEnum):
  NONE = 'None'
  TRACK = 'Track'
  PLAYLIST = 'Playlist'


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
  PropertiesChanged = auto()
  Seeked = auto()
  TrackAdded = auto()
  TrackListReplaced = auto()
  TrackMetadataChanged = auto()
  TrackRemoved = auto()
