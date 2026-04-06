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
class User:
    def __init__(self, user_id, name, age, sessions):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = [] #reference to ListeningSession

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        return sum(s.duration_listened_seconds for s in self.sessions)

    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self):
        return {s.track.track_id for s in self.sessions}

class PremiumUser(User):
    def __init__(self, user_id, name, age, sessions, subscription_start):
        super().__init__(user_id, name, age, sessions)
        self.subscription_start = subscription_start

class FreeUser(User):
    def __init__(self, user_id, name, age, sessions, max_skips_per_hour):
        super().__init__(user_id, name, age, sessions)
        self.max_skips_per_hour = 6

class FamilyAccountUser(User):
    def __init__(self, user_id, name, age, sessions, sub_users):
        super().__init__(user_id, name, age, sessions)
        self.sub_users = [] #add FamilyMember as list item

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        return [self] + self.sub_users
class FamilyMember(User):
    def __init__(self, user_id, name, age, sessions, parent):
        super().__init__(user_id, name, age, sessions)
        self.parent = parent # replace later with FamilyAccountUser