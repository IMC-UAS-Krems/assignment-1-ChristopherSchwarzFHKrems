"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self.catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self.sessions = []

    def add_track(self, track):
        if track and hasattr(track, "track_id"):
            self.catalogue[track.track_id] = track

    def add_user(self, user):
        if user and hasattr(user, "user_id"):
            self._users[user.user_id] = user

    def add_artist(self, artist):
        if artist and hasattr(artist, "artist_id"):
            self._artists[artist.artist_id] = artist

    def add_album(self, album):
        if album and hasattr(album, "album_id"):
            self._albums[album.album_id] = album

    def add_playlist(self, playlist):
        if playlist and hasattr(playlist, "playlist_id"):
            self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        if session:
            self.sessions.append(session)
            if hasattr(session.user, "add_session"):
                session.user.add_session(session)

    def get_track(self, track_id):
        return self.catalogue.get(track_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def get_artist(self, artist_id):
        return self._artists.get(artist_id)

    def get_album(self, album_id):
        return self._albums.get(album_id)

    def get_playlist(self, playlist_id):
        return self._playlists.get(playlist_id)

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self.catalogue.values())