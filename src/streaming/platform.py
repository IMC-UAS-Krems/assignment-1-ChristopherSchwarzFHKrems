"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from __future__ import annotations
from .tracks import Track
from .users import User
from .artists import Artist
from .albums import Album
from .playlists import Playlist
from .sessions import ListeningSession
from typing import Optional
from datetime import datetime
from .users import PremiumUser
from .users import FamilyMember
from .tracks import Song
from .playlists import CollaborativePlaylist
from collections import defaultdict
class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self._catalogue: dict[str, Track] = {}
        self._users: dict[str, User] = {}
        self._artists: dict[str, Artist] = {}
        self._albums: dict[str, Album] = {}
        self._playlists: dict[str, Playlist] = {}
        self._sessions: list[ListeningSession] = []

    def add_track(self, track: Track) -> None:
        self._catalogue[track.track_id] = track

    def add_user(self, user: User) -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist) -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album) -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist) -> None:
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession) -> None:
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str) -> Optional[Track]:
        return self._catalogue.get(track_id)

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_artist(self, artist_id: str) -> Optional[Artist]:
        return self._artists.get(artist_id)

    def get_album(self, album_id: str) -> Optional[Album]:
        return self._albums.get(album_id)

    def all_users(self) -> list[User]:
        return list(self._users.values())

    def all_tracks(self) -> list[Track]:
        return list(self._catalogue.values())

    # Q1: Return the total cumulative listening time (in minutes) across all users
    # for a given time period. Sum up the listening duration for all sessions that
    # fall within the specified datetime window (inclusive on both ends).
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        #sums the duration in the time window from start to end
        return float(sum(
            s.duration_listened_seconds / 60
            for s in self._sessions
            if start <= s.timestamp <= end
        ))
    # Q2: Compute the average number of unique tracks listened to per PremiumUser in the
    #last days days (default 30). Only count distinct tracks for sessions within the
    # time window. Return 0.0 if there are no premium users.
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)

        premium_users = [
            pu for pu in self._users.values() if isinstance(pu, PremiumUser)
        ]
        if not premium_users:
            return 0.0

        total_unique = sum(
            len({s.track.track_id for s in pu.sessions if s.timestamp >= cutoff})
            for pu in premium_users
        )
        # returns the avg unique track count per premium user
        return total_unique / len(premium_users)

    # Q3: Return the track with the highest number of distinct listeners
    # (not total plays) in the catalogue. Count the number of unique users who
    # have listened to each track and return the one with the most. Return None if
    # no sessions exist.
    def track_with_most_distinct_listeners(self) -> Optional[Track]:
        if not self._sessions:
            return None
        listener_counts: dict[str, set[str]] = {}
        for s in self._sessions:
            tid = s.track.track_id
            listener_counts.setdefault(tid, set()).add(s.user.user_id)

        best_id = max(listener_counts, key=lambda tid: len(listener_counts[tid]))
        # returns the first track listende by different users
        return self._catalogue.get(best_id)

    # Q4: For each user subtype (e.g., FreeUser, PremiumUser, FamilyAccountUser,
    # FamilyMember), compute the average session duration (in seconds) and return
    # them ranked from longest to shortest. Return as a list of (type_name,
    # average_duration_seconds) tuples.
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        buckets: dict[str, list[int]] = defaultdict(list)

        for s in self._sessions:
            type_name = type(s.user).__name__
            buckets[type_name].append(s.duration_listened_seconds)

        result = [
            (type_name, sum(durations) / len(durations))
            for type_name, durations in buckets.items()
        ]
        #returns the reversed list of avg session dur. per uiser type
        return sorted(result, key=lambda x: x[1], reverse=True)

    # Q5: Return the total listening time (in minutes) attributed to tracks
    # associated with FamilyAccountUser sub-accounts where the sub-account holder
    # (i.e., FamilyMember) is under the specified age threshold (default 18, exclusive).
    # For example, with threshold 18, count only family members with age < 18.
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total = 0
        for u in self._users.values():
            if isinstance(u, FamilyMember) and u.age < age_threshold:
                total += u.total_listening_seconds()
        return total / 60

    # Q6: Identify the top n artists (default 5) ranked by total cumulative listening
    # time across all their tracks. Only count listening time for tracks where
    # isinstance(track, Song) is true (exclude podcasts and audiobooks). Return as a
    # list of (Artist, total_minutes) tuples, sorted from highest to lowest listening
    # time.
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        artist_seconds: dict[str, float] = defaultdict(float)

        for s in self._sessions:
            if isinstance(s.track, Song):
                artist_seconds[s.track.artist.artist_id] += s.duration_listened_seconds

        ranked = sorted(artist_seconds.items(), key=lambda x: x[1], reverse=True)
        return [
            (self._artists[aid], secs / 60)
            for aid, secs in ranked[:n]
            if aid in self._artists
        ]

    # Q7: Given a user ID, return their most frequently listened-to genre and the
    # percentage of their total listening time it accounts for. Return a (genre,
    # percentage) tuple where percentage is in the range [0, 100], or None if the
    # user doesn't exist or has no listening history.

    def user_top_genre(self, user_id: str) -> Optional[tuple[str, float]]:
        user = self._users.get(user_id)
        if not user or not user.sessions:
            return None

        genre_seconds: dict[str, float] = defaultdict(float)
        total = 0.0

        for s in user.sessions:
            genre_seconds[s.track.genre] += s.duration_listened_seconds
            total += s.duration_listened_seconds

        top_genre = max(genre_seconds, key=lambda g: genre_seconds[g])
        percentage = (genre_seconds[top_genre] / total) * 100
        return top_genre, percentage

    # Q8:Return all CollaborativePlaylist instances that contain tracks from more
    # than threshold (default 3) distinct artists. Only Song tracks count toward
    # the artist count (exclude Podcast and AudiobookTrack which don't have artists).
    # Return playlists in the order they were registered.

    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        result = []
        for pl in self._playlists.values():
            if not isinstance(pl, CollaborativePlaylist):
                continue
            artists = {
                a.artist.artist_id
                for a in pl.tracks
                if isinstance(a, Song)
            }
            if len(artists) > threshold:
                result.append(pl)
        return result

    # Q9:Compute the average number of tracks per playlist, distinguishing between
    # standard Playlist and CollaborativePlaylist instances. Return a dictionary with
    # keys "Playlist" and "CollaborativePlaylist" mapped to their respective averages.
    # Return 0.0 for a type with no instances.

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        standard = [
            pl for pl in self._playlists.values()
            if type(pl) is Playlist
        ]
        collab = [
            pl for pl in self._playlists.values()
            if isinstance(pl, CollaborativePlaylist)
        ]
        return {
            "Playlist": (
                sum(len(pl.tracks) for pl in standard) / len(standard)
                if standard else 0.0
            ),
            "CollaborativePlaylist": (
                sum(len(pl.tracks) for pl in collab) / len(collab)
                if collab else 0.0
            ),
        }
    # Q10: Identify users who have listened to every track on at least one complete
    # Album and return the corresponding album titles. A user "completes" an album
    # if their session history includes at least one listen to each track on that
    # album. Return as a list of (User, [album_title, ...]) tuples in registration
    # order. Albums with no tracks are ignored.
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        album_list = [a for a in self._albums.values() if a.tracks]
        result = []
        for user in self._users.values():
            listened_ids = {s.track.track_id for s in user.sessions}
            completed = [
                album.title
                for album in album_list
                if album.track_ids().issubset(listened_ids)
            ]
            if completed:
                result.append((user, completed))
        return result