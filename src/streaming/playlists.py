"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.__tracks= []
    def add_track(self, track):
        pass
    def remove_track(self, track_id):
        pass
    def total_duration_seconds(self):
        return 0

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner):
        super().__init__(playlist_id, name, owner)
        self.__contributors = []
    def add_contributor(self, user):
        self.__contributors.append(user)

    def remove_contributor(self, user):
        self.__contributors = [u for u in self.__contributors if u != user]