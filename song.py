import json

class Song():
    """
    Top level song class
    """
    def __init__(self):
        self.info = {
            'authorName': 'name',
            'beatsPerMinute': 120,
            'coverImagePath': 'cover.jpg',
            'difficultyLevels': [
                ],
            'environmentName': 'DefaultEnvironment',
            'previewDuration': 10,
            'previewStartTime': 12,
            'songName': 'Song Name',
            'songSubName': 'Sub Name',
            }
        self.tracks = []

class Track():
    """
    A single track of a song
    """

    def __init__(self):
        self.spec = {
            'audioPath': 'song.ogg',
            'difficulty': 'Expert',
            'difficultyRank': 4,
            'jsonPath': 'Expert.json',
            'offset': 0,
            'oldOffset': 0
            }

        self.data = {
                '_version': '1.5.0',
                '_beatsPerMinute': 120,
                '_beatsPerBar': 4,
                '_noteJumpSpeed': 10,
                '_shuffle': 0,
                '_sufflePeriod': 0.5,
                '_events': [],
                '_notes': [],
                '_obstacles': [],
            }

class Note():

    def __init__(self):
        self.time = 0
        self.xpos = 0
        self.ypos = 0
        self.type = 0
        self.dir = 0

    def __dict__(self):
        return {
            '_time': self.time,
            '_lineIndex': self.xpos,
            '_lineLayer': self.ypos,
            '_type': self.type,
            '_cutDirecton': self.dir
            }


"""
Obstacles:
    lineindex = 0,1,2,3 = xpos
    type = o,1 = full or half height
    width = 1 = width
"""

class Grid():
    """
    Class that handles note grids and conversions between them
    """
    def __init__(self, bpm= 120, bpb=4, offset =0):
        self.bpm = bpm
        self.bpb = bpb
        self.offset = offset

    def to_time(self, beat):
        """
        convert a decimal beat value into a global time
        """
        return 60*beat/self.bpm + offset

    def to_beat(self, timeval):
        """
        convert a time in seconds to the local beat value
        """
        return self.bpm*(timeval - offset)/60

