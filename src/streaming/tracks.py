"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""
from __future__ import annotations
from abc import ABC
from typing import Optional, TYPE_CHECKING
from datetime import date
#fixes the circular session problem
if TYPE_CHECKING:
    from .artists import Artist
    from .albums import Album

class Track(ABC):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        return self.duration_seconds / 60

class AudiobookTrack(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, author: str, narrator: str):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator

class Podcast(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, description: str):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class InterviewEpisode(Podcast):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, description: str, guest: str):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest
class NarrativeEpisode(Podcast):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, description: str, season: int, episode_number: int):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number

class Song(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int,genre: str, artist: Artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class SingleRelease(Song):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: Artist, release_date: date):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class AlbumTrack(Song):
    def __init__(self, track_id: str, title: str, duration_seconds: int,genre: str, artist: Artist, track_number: int,album: Optional[Album] = None):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = album