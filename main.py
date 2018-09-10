
from tkinter import  *
import tkutil
import keyframe
import track
import meta

import json
import math
import os
import sys


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack(fill=BOTH, expand=1)


        edit_frame = Frame(frame, height=200)
        edit_frame.pack(side=TOP)

        #song info frame
        self.meta_editor = meta.Editor(self, edit_frame)

        #keyframe editor

        self.keyframe_editor = keyframe.Editor(edit_frame)

        #timing frame

        self.track_editor = track.Editor(frame)

        self.track_editor.set_callback('send_keyframe', self.keyframe_editor.load_keyframe)

        self.load_song('./The Fox')
#        self.load_track('./The Fox/Expert.json')

    def load_song(self, loc):
        self.song_dir = loc
        filename = os.path.join(loc, 'info.json')

        data = json.load(open(filename, 'r'))
        self.meta_editor.load_song(data)
        self.load_track()

    def load_track(self):
        loc = self.song_dir
        track = self.meta_editor.active_track
        track_file = os.path.join(loc, track['jsonPath'])
        print('loading {}'.format(track_file))

        self._load_track(track_file)

    def create_track(self, json_path):
        filename = os.path.join(self.song_dir, json_path)
        #TODO Check if it exists?
        data = {
            '_version': '1.5.0',
            '_beatsPerMinute': 120, #TODO inherit
            '_beatsPerBar': 4,
            '_noteJumpSpeed': 10,
            '_shuffle': 0,
            '_shufflePeriod': 0.5,
            '_notes': [],
            '_events': [],
            '_obstacles': [],
        }
        json.dump(data, open(filename,'w'))

    def _load_track(self, filename):
        """
        Load up the given track.
        """

        data = json.load(open(filename, 'r'))
        self.meta_editor.load_track()
        self.track_editor.clear()
        self.keyframes = keyframe.Keyframe.load_keyframes(data)
        self.track_editor.load_keyframes(self.keyframes)



root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
