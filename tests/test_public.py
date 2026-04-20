"""
test_public.py
--------------
Public test suite template.

This file provides a minimal framework and examples to guide you in writing
comprehensive tests for your StreamingPlatform implementation. Each test class
corresponds to one of the 10 query methods (Q1-Q10).

You should:
1. Study the examples provided
2. Complete the stub tests (marked with TODO or pass statements)
3. Add additional test cases for edge cases and boundary conditions
4. Verify your implementation passes all tests

Run with:
    pytest tests/test_public.py -v
"""

from datetime import timedelta, date

from streaming.platform import StreamingPlatform
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.playlists import CollaborativePlaylist
from tests.conftest import FIXED_NOW, RECENT, OLD
from streaming.tracks import AlbumTrack, Song
from streaming.artists import Artist
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist

#Disclaimer: this is my first time working with tests, I have no idea if I did everything right or totally wrong, but all the tests passed

# ===========================================================================
# Q1 - Total cumulative listening time for a given period
# ===========================================================================

class TestTotalListeningTime:
    """Test the total_listening_time_minutes(start, end) method.
    
    This method should sum up all session durations that fall within
    the specified datetime window (inclusive on both ends).
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        start = RECENT - timedelta(hours=1)
        end = FIXED_NOW
        result = platform.total_listening_time_minutes(start, end)
        assert isinstance(result, float)

    def test_empty_window_returns_zero(self, platform: StreamingPlatform) -> None:
        """Test that a time window with no sessions returns 0.0."""
        far_future = FIXED_NOW + timedelta(days=365)
        result = platform.total_listening_time_minutes(
            far_future, far_future + timedelta(hours=1)
        )
        assert result == 0.0

    # TODO: Add a test that verifies the correct value for a known time period.
    #       Calculate the expected total based on the fixture data in conftest.py.
    def test_known_period_value(self, platform: StreamingPlatform) -> None:
        #values from conftest.py
        fu = FreeUser("fu1", "Alice", age=18)
        a = Artist("a1", "Pixels", "pop")
        s = Song("s1", "Pixel Rain", 180, "pop", a)
        platform.add_user(fu)
        platform.add_track(s)

        session = ListeningSession("s1", fu, s, FIXED_NOW, 150)
        platform.record_session(session)

        start = FIXED_NOW - timedelta(hours=1)
        end = FIXED_NOW + timedelta(hours=1)

        baseline = platform.total_listening_time_minutes(start, end)
        assert baseline >= 2.5


# ===========================================================================
# Q2 - Average unique tracks per PremiumUser in the last N days
# ===========================================================================

class TestAvgUniqueTracksPremium:
    """Test the avg_unique_tracks_per_premium_user(days) method.
    
    This method should:
    - Count distinct tracks per PremiumUser in the last N days
    - Exclude FreeUser, FamilyAccountUser, and FamilyMember
    - Return 0.0 if there are no premium users
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        result = platform.avg_unique_tracks_per_premium_user(days=30)
        assert isinstance(result, float)

    def test_no_premium_users_returns_zero(self) -> None:
        """Test with a platform that has no premium users."""
        p = StreamingPlatform("EmptyPlatform")
        p.add_user(FreeUser("u99", "Nobody", age=25))
        assert p.avg_unique_tracks_per_premium_user() == 0.0

    # TODO: Add a test with the fixture platform that verifies the correct
    #       average for premium users. You'll need to count unique tracks
    #       per premium user and calculate the average.
    def test_correct_value(self, platform: StreamingPlatform) -> None:
        #premium user
        bob = None
        for user in platform.all_users():
            if isinstance(user, PremiumUser):
                bob = user
                break

        assert bob is not None

        # load tracks
        tracks = platform.all_tracks()
        t1, t2, _ = tracks

        # listining history
        platform.record_session(ListeningSession("s1", bob, t1, FIXED_NOW, 100))
        platform.record_session(ListeningSession("s2", bob, t1, FIXED_NOW, 200))
        platform.record_session(ListeningSession("s3", bob, t2, FIXED_NOW, 150))

        result = platform.avg_unique_tracks_per_premium_user()

        assert result == 2.0


# ===========================================================================
# Q3 - Track with the most distinct listeners
# ===========================================================================

class TestTrackMostDistinctListeners:
    """Test the track_with_most_distinct_listeners() method.
    
    This method should:
    - Count the number of unique users who have listened to each track
    - Return the track with the highest count
    - Return None if the platform has no sessions
    """

    def test_empty_platform_returns_none(self) -> None:
        """Test that an empty platform returns None."""
        p = StreamingPlatform("Empty")
        assert p.track_with_most_distinct_listeners() is None

    # TODO: Add a test that verifies the correct track is returned.
    #       Count listeners per track from the fixture data.
    def test_correct_track(self, platform: StreamingPlatform) -> None:
        # assign the users to users
        users = platform.all_users()
        alice = users[0]
        bob = users[1]

        # find tracks
        tracks = platform.all_tracks()
        t1, t2, t3 = tracks

        platform.record_session(ListeningSession("s1", alice, t1, RECENT, 100))
        platform.record_session(ListeningSession("s2", bob, t1, RECENT, 120))

        platform.record_session(ListeningSession("s3", alice, t2, RECENT, 150))

        result = platform.track_with_most_distinct_listeners()
        # t1 got 2 listeners, should return t1
        assert result == t1


# ===========================================================================
# Q4 - Average session duration per user subtype, ranked
# ===========================================================================

class TestAvgSessionDurationByType:
    """Test the avg_session_duration_by_user_type() method.
    
    This method should:
    - Calculate average session duration (in seconds) for each user type
    - Return a list of (type_name, average_duration) tuples
    - Sort results from longest to shortest duration
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (str, float) tuples."""
        result = platform.avg_session_duration_by_user_type()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], str) and isinstance(item[1], float)

    def test_sorted_descending(self, platform: StreamingPlatform) -> None:
        """Verify results are sorted by duration (longest first)."""
        result = platform.avg_session_duration_by_user_type()
        durations = [r[1] for r in result]
        assert durations == sorted(durations, reverse=True)

    # TODO: Add tests to verify all user types are present and have correct averages.
    def test_all_user_types_present(self, platform: StreamingPlatform) -> None:
       # get the users
        users = platform.all_users()
        free_user = None
        premium_user = None

        for u in users:
            if isinstance(u, FreeUser):
                free_user = u
            elif isinstance(u, PremiumUser):
                premium_user = u

        assert free_user is not None
        assert premium_user is not None
        track = platform.all_tracks()[0]

        # make both users
        platform.record_session(
            ListeningSession("s1", free_user, track, FIXED_NOW, 120)
        )
        platform.record_session(
            ListeningSession("s2", premium_user, track, FIXED_NOW, 180)
        )
        result = platform.avg_session_duration_by_user_type()
        user_types = {r[0] for r in result}

        # are both present?
        assert "FreeUser" in user_types
        assert "PremiumUser" in user_types

        # avg
        for name, avg in result:
            if name == "FreeUser":
                assert avg == 120.0
            if name == "PremiumUser":
                assert avg == 180.0

# ===========================================================================
# Q5 - Total listening time for underage sub-users
# ===========================================================================

class TestUnderageSubUserListening:
    """Test the total_listening_time_underage_sub_users_minutes(age_threshold) method.
    
    This method should:
    - Count only sessions for FamilyMember users under the age threshold
    - Convert to minutes
    - Return 0.0 if no underage users or their sessions exist
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        result = platform.total_listening_time_underage_sub_users_minutes()
        assert isinstance(result, float)

    def test_no_family_users(self) -> None:
        """Test a platform with no family accounts."""
        p = StreamingPlatform("NoFamily")
        p.add_user(FreeUser("u1", "Solo", age=20))
        assert p.total_listening_time_underage_sub_users_minutes() == 0.0

    # TODO: Add tests for correct values with default and custom thresholds.
    def test_correct_value_default_threshold(self, platform: StreamingPlatform) -> None:
        parent = FamilyAccountUser("f1", "ParentAccount", age=40, subscription_start=date(2023, 1, 1))
        child = FamilyMember("c1", "Child", age=16, parent=parent)
        adult_child = FamilyMember("c2", "Teen", age=19, parent=parent)
        parent.add_sub_user(child)
        parent.add_sub_user(adult_child)
        platform.add_user(child)
        platform.add_user(adult_child)
        track = platform.all_tracks()[0]

        #counts child under 18
        platform.record_session(ListeningSession("s1", child, track, FIXED_NOW, 180))
        platform.record_session(ListeningSession("s2", adult_child, track, FIXED_NOW, 300))

        result = platform.total_listening_time_underage_sub_users_minutes()

        assert result == 3.0

    def test_custom_threshold(self, platform: StreamingPlatform) -> None:
        parent = FamilyAccountUser("f2", "ParentAccount2", age=45, subscription_start=date(2023, 1, 1))
        kid = FamilyMember("c3", "Kid", age=12, parent=parent)
        teen = FamilyMember("c4", "Teen", age=17, parent=parent)
        parent.add_sub_user(kid)
        parent.add_sub_user(teen)
        platform.add_user(kid)
        platform.add_user(teen)
        track = platform.all_tracks()[1]

        #threshold = 15 only kids counting
        platform.record_session(ListeningSession("s1", kid, track, FIXED_NOW, 120))
        platform.record_session(ListeningSession("s2", teen, track, FIXED_NOW, 240))

        result = platform.total_listening_time_underage_sub_users_minutes(15)

        assert result == 2.0


# ===========================================================================
# Q6 - Top N artists by total listening time
# ===========================================================================

class TestTopArtistsByListeningTime:
    """Test the top_artists_by_listening_time(n) method.
    
    This method should:
    - Rank artists by total cumulative listening time (minutes)
    - Only count Song tracks (exclude Podcast and AudiobookTrack)
    - Return a list of (Artist, minutes) tuples
    - Sort from highest to lowest listening time
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (Artist, float) tuples."""
        from streaming.artists import Artist
        result = platform.top_artists_by_listening_time(n=3)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], Artist) and isinstance(item[1], float)

    def test_sorted_descending(self, platform: StreamingPlatform) -> None:
        """Verify results are sorted by listening time (highest first)."""
        result = platform.top_artists_by_listening_time(n=5)
        minutes = [r[1] for r in result]
        assert minutes == sorted(minutes, reverse=True)

    def test_respects_n_parameter(self, platform: StreamingPlatform) -> None:
        """Verify only the top N artists are returned."""
        result = platform.top_artists_by_listening_time(n=2)
        assert len(result) <= 2

    # TODO: Add a test that verifies the correct artists and values.
    def test_top_artist(self, platform: StreamingPlatform) -> None:
        artist = None
        for a in platform.all_tracks():
            if hasattr(a, "artist"):
                artist = a.artist
                break

        assert artist is not None

        t1, t2, t3 = platform.all_tracks()
        # create some listenings
        platform.record_session(ListeningSession("s1", platform.all_users()[0], t1, FIXED_NOW, 120))
        platform.record_session(ListeningSession("s2", platform.all_users()[0], t2, FIXED_NOW, 180))
        platform.record_session(ListeningSession("s3", platform.all_users()[1], t3, FIXED_NOW, 60))

        result = platform.top_artists_by_listening_time(n=1)
        assert len(result) == 1

        top_artist, minutes = result[0]
        assert top_artist == artist
        assert minutes == 6.0  # 120+180+60 = 360


# ===========================================================================
# Q7 - User's top genre and percentage
# ===========================================================================

class TestUserTopGenre:
    """Test the user_top_genre(user_id) method.
    
    This method should:
    - Find the genre with the most listening time for a user
    - Return (genre_name, percentage_of_total_time)
    - Return None if user doesn't exist or has no sessions
    """

    def test_returns_tuple_or_none(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a tuple or None."""
        result = platform.user_top_genre("u1")
        if result is not None:
            assert isinstance(result, tuple) and len(result) == 2
            assert isinstance(result[0], str) and isinstance(result[1], float)

    def test_nonexistent_user_returns_none(self, platform: StreamingPlatform) -> None:
        """Test that a nonexistent user ID returns None."""
        assert platform.user_top_genre("does_not_exist") is None

    def test_percentage_in_valid_range(self, platform: StreamingPlatform) -> None:
        """Verify percentage is between 0 and 100."""
        for user in platform.all_users():
            result = platform.user_top_genre(user.user_id)
            if result is not None:
                _, pct = result
                assert 0.0 <= pct <= 100.0

    # TODO: Add a test that verifies the correct genre and percentage for a known user.
    def test_correct_top_genre(self, platform: StreamingPlatform) -> None:
        # get user
        user = platform.all_users()[0]

        # get tracks
        t1, t2, t3 = platform.all_tracks()

        platform.record_session(ListeningSession("s1", user, t1, FIXED_NOW, 100))
        platform.record_session(ListeningSession("s2", user, t2, FIXED_NOW, 200))
        platform.record_session(ListeningSession("s3", user, t3, FIXED_NOW, 300))

        result = platform.user_top_genre(user.user_id)
        assert result is not None

        genre, pct = result
        #only pop
        assert genre == "pop"
        assert pct == 100.0


# ===========================================================================
# Q8 - CollaborativePlaylists with more than threshold distinct artists
# ===========================================================================

class TestCollaborativePlaylistsManyArtists:
    """Test the collaborative_playlists_with_many_artists(threshold) method.
    
    This method should:
    - Return all CollaborativePlaylist instances with >threshold distinct artists
    - Only count Song tracks (exclude Podcast and AudiobookTrack)
    - Return playlists in registration order
    """

    def test_returns_list_of_collaborative_playlists(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify the method returns a list of CollaborativePlaylist objects."""
        result = platform.collaborative_playlists_with_many_artists()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, CollaborativePlaylist)

    def test_higher_threshold_returns_empty(
        self, platform: StreamingPlatform
    ) -> None:
        """Test that a high threshold returns an empty list."""
        result = platform.collaborative_playlists_with_many_artists(threshold=100)
        assert result == []

    # TODO: Add tests that verify the correct playlists are returned with
    #       different threshold values.
    def test_default_threshold(self, platform: StreamingPlatform) -> None:
        # dummy artists
        a2 = Artist("a2", "Artist2", "rock")
        a3 = Artist("a3", "Artist3", "jazz")
        a4 = Artist("a4", "Artist4", "edm")

        platform.add_artist(a2)
        platform.add_artist(a3)
        platform.add_artist(a4)

        #collaborative playlist
        #owner is always platform (just a filler)
        cp = CollaborativePlaylist("cp1", "Collab", owner=platform)

        # new and excisting artists
        t1 = platform.all_tracks()[0]
        t2 = AlbumTrack("x1", "Track2", 120, "rock", a2, 1)
        t3 = AlbumTrack("x2", "Track3", 120, "jazz", a3, 1)
        t4 = AlbumTrack("x3", "Track4", 120, "edm", a4, 1)

        cp.add_track(t1)
        cp.add_track(t2)
        cp.add_track(t3)
        cp.add_track(t4)

        platform.add_playlist(cp)

        result = platform.collaborative_playlists_with_many_artists()

        assert cp in result
        assert len(result) == 1


# ===========================================================================
# Q9 - Average tracks per playlist type
# ===========================================================================

class TestAvgTracksPerPlaylistType:
    """Test the avg_tracks_per_playlist_type() method.
    
    This method should:
    - Calculate average track count for standard Playlist instances
    - Calculate average track count for CollaborativePlaylist instances
    - Return a dict with keys "Playlist" and "CollaborativePlaylist"
    - Return 0.0 for types with no instances
    """

    def test_returns_dict_with_both_keys(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify the method returns a dict with both playlist types."""
        result = platform.avg_tracks_per_playlist_type()
        assert isinstance(result, dict)
        assert "Playlist" in result
        assert "CollaborativePlaylist" in result

    # TODO: Add tests that verify the correct averages for each playlist type.
    def test_standard_playlist_average(self, platform: StreamingPlatform) -> None:
        # playlists
        p1 = Playlist("p1", "Mix1", owner=platform)
        p2 = Playlist("p2", "Mix2", owner=platform)
        t1, t2 = platform.all_tracks()[0], platform.all_tracks()[1]
        p1.add_track(t1)
        p1.add_track(t2)
        p2.add_track(t1)
        platform.add_playlist(p1)
        platform.add_playlist(p2)

        result = platform.avg_tracks_per_playlist_type()
        assert result["Playlist"] == 1.5

    def test_collaborative_playlist_average(self, platform: StreamingPlatform) -> None:
        # more artists
        a2 = Artist("a2", "Artist2", "rock")
        platform.add_artist(a2)

        # coll playl.
        cp1 = CollaborativePlaylist("c1", "C1", owner=platform)
        cp2 = CollaborativePlaylist("c2", "C2", owner=platform)

        t1 = platform.all_tracks()[0]
        t2 = AlbumTrack("x1", "Extra", 120, "rock", a2, 1)
        cp1.add_track(t1)
        cp1.add_track(t2)
        cp2.add_track(t1)
        platform.add_playlist(cp1)
        platform.add_playlist(cp2)

        result = platform.avg_tracks_per_playlist_type()
        assert result["CollaborativePlaylist"] == 1.5


# ===========================================================================
# Q10 - Users who completed at least one full album
# ===========================================================================

class TestUsersWhoCompletedAlbums:
    """Test the users_who_completed_albums() method.
    
    This method should:
    - Return users who have listened to every track on at least one album
    - Return (User, [album_titles]) tuples
    - Include all completed albums for each user
    - Ignore albums with no tracks
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (User, list) tuples."""
        from streaming.users import User
        result = platform.users_who_completed_albums()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], User) and isinstance(item[1], list)

    def test_completed_album_titles_are_strings(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify all completed album titles are strings."""
        result = platform.users_who_completed_albums()
        for _, titles in result:
            assert all(isinstance(t, str) for t in titles)

    # TODO: Add tests that verify the correct users and albums are identified.
    def test_correct_users_identified(self, platform: StreamingPlatform) -> None:
        user = platform.all_users()[0]
        tracks = platform.all_tracks()

        # for tests User listens to all tracks
        for i, t in enumerate(tracks):
            platform.record_session(
                ListeningSession(f"s{i}", user, t, FIXED_NOW, 100)
            )

        result = platform.users_who_completed_albums()
        # user also included
        users = [u for u, _ in result]
        assert user in users

    def test_correct_album_titles(self, platform: StreamingPlatform) -> None:
        user = platform.all_users()[0]
        tracks = platform.all_tracks()

        # user listens again to whole album
        for i, t in enumerate(tracks):
            platform.record_session(
                ListeningSession(f"s{i}", user, t, FIXED_NOW, 100)
            )

        result = platform.users_who_completed_albums()
        assert result

        _, titles = result[0]
        assert "Digital Dreams" in titles
