
from tkinter import  *
import tkutil
import keyframe
import track
import meta

import json
import math



class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack(fill=BOTH, expand=1)


        edit_frame = Frame(frame, height=200)
        edit_frame.pack(side=TOP)

        #song info frame
        self.meta_editor = meta.Editor(edit_frame)

        #keyframe editor

        self.keyframe_editor = keyframe.Editor(edit_frame)

        #timing frame

        self.track_editor = track.Editor(frame)

        self.track_editor.set_callback('send_keyframe', self.keyframe_editor.load_keyframe)

        self.load_song('./The Fox/info.json')
        self.load_track('./The Fox/Expert.json')

    def load_song(self, filename):
        data = json.load(open(filename, 'r'))
        self.meta_editor.load_song(data)

    def load_track(self, filename):
        """
        Load up the given track.
        """
        data = json.load(open(filename, 'r'))
        self.keyframes = keyframe.Keyframe.load_keyframes(data)
        self.track_editor.load_keyframes(self.keyframes)


root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
