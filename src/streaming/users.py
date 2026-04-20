"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from __future__ import annotations
from abc import ABC
from .sessions import ListeningSession
from datetime import date

class User(ABC):
    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions: list[ListeningSession] = []

    def add_session(self, session: ListeningSession) -> None:
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        return sum(s.duration_listened_seconds for s in self.sessions)

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self) -> set[str]:
        return {s.track.track_id for s in self.sessions}

class PremiumUser(User):
    def __init__(self, user_id: str, name: str, age: int, subscription_start: date):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FreeUser(User):
    MAX_SKIPS_PER_HOUR: int = 6
    def __init__(self, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)

class FamilyAccountUser(PremiumUser):
    def __init__(self, user_id: str, name: str, age: int, subscription_start: date):
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users: list[FamilyMember] = []

    def add_sub_user(self, sub_user: FamilyMember) -> None:
        self.sub_users.append(sub_user)

    def all_members(self) -> list[User]:
        return [self] + list(self.sub_users)

class FamilyMember(User):
    def __init__(self, user_id: str, name: str, age: int, parent: FamilyAccountUser):
        super().__init__(user_id, name, age)
        self.parent = parent