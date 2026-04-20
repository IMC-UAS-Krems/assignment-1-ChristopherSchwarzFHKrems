"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING
#fixes the circular track problem
if TYPE_CHECKING:
    from tracks import Track
    from users import User
class ListeningSession:
    def __init__(self, session_id: str, user: User, track: Track,timestamp: datetime, duration_listened_seconds: int):
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds
        self.tracks: list[Track] = [track]

    def duration_listened_minutes(self) -> float:
        return self.duration_listened_seconds / 60