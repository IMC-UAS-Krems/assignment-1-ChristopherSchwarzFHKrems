"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from __future__ import annotations
from .artists import Artist
from .tracks import AlbumTrack
class Album:
    def __init__(self, album_id: str, title: str, artist: Artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks: list[AlbumTrack] = []

    def add_track(self, track: AlbumTrack) -> None:
        self.tracks.append(track)

    def track_ids(self) -> set[str]:
        return {t.track_id for t in self.tracks}

    def duration_seconds(self) -> int:
        return sum(t.duration_seconds for t in self.tracks)