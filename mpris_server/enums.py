from __future__ import annotations

from enum import StrEnum, auto
from typing import Self

from strenum import StrEnum


class Access(StrEnum):
  read: Self = auto()
  readwrite: Self = auto()


class Arg(StrEnum):
  AfterTrack: Self = auto()
  CurrentTrack: Self = auto()
  Index: Self = auto()
  MaxCount: Self = auto()
  Metadata: Self = auto()
  Offset: Self = auto()
  Order: Self = auto()
  Playlist: Self = auto()
  PlaylistId: Self = auto()
  Playlists: Self = auto()
  Position: Self = auto()
  ReverseOrder: Self = auto()
  SetAsCurrent: Self = auto()
  TrackId: Self = auto()
  TrackIds: Self = auto()
  Tracks: Self = auto()
  Uri: Self = auto()


class Direction(StrEnum):
  In: Self = 'in'
  out: Self = auto()


class LoopStatus(StrEnum):
  NONE: str = 'None'
  TRACK: str = 'Track'
  PLAYLIST: str = 'Playlist'


class Method(StrEnum):
  ActivatePlaylist: Self = auto()
  AddTrack: Self = auto()
  GetPlaylists: Self = auto()
  GetTracksMetadata: Self = auto()
  GoTo: Self = auto()
  Next: Self = auto()
  OpenUri: Self = auto()
  Pause: Self = auto()
  Play: Self = auto()
  PlayPause: Self = auto()
  Previous: Self = auto()
  Quit: Self = auto()
  Raise: Self = auto()
  RemoveTrack: Self = auto()
  Seek: Self = auto()
  SetPosition: Self = auto()
  Stop: Self = auto()


class Property(StrEnum):
  ActivePlaylist: Self = auto()
  CanControl: Self = auto()
  CanEditTracks: Self = auto()
  CanGoNext: Self = auto()
  CanGoPrevious: Self = auto()
  CanPause: Self = auto()
  CanPlay: Self = auto()
  CanQuit: Self = auto()
  CanRaise: Self = auto()
  CanSeek: Self = auto()
  CanSetFullscreen: Self = auto()
  DesktopEntry: Self = auto()
  Fullscreen: Self = auto()
  HasTrackList: Self = auto()
  Identity: Self = auto()
  LoopStatus: Self = auto()
  MaximumRate: Self = auto()
  Metadata: Self = auto()
  MinimumRate: Self = auto()
  Orderings: Self = auto()
  PlaybackStatus: Self = auto()
  PlaylistCount: Self = auto()
  Position: Self = auto()
  Rate: Self = auto()
  Shuffle: Self = auto()
  SupportedMimeTypes: Self = auto()
  SupportedUriSchemes: Self = auto()
  Tracks: Self = auto()
  Volume: Self = auto()


class Signal(StrEnum):
  PlaylistChanged: Self = auto()
  Seeked: Self = auto()
  TrackAdded: Self = auto()
  TrackListReplaced: Self = auto()
  TrackMetadataChanged: Self = auto()
  TrackRemoved: Self = auto()


