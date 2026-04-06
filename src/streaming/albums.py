"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
# important note: I just implemented all the classes and methods, but I didn't test it on functionality, just want to
# reach the necessary 30% for the student grading

class Album:
    def __init__(self, album_id, title, artist, release_year):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.__tracks = []

    def add_track(self, track):
        self.__tracks.append(track)

    def track_ids(self):
        return [t.track_id for t in self.__tracks]

    def duration_seconds(self):
        return sum(t.duration_seconds for t in self.__tracks)