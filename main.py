
from tkinter import  *
import tkutil
import keyframe
import track
import meta

import json
import math
import os
import sys

import librosa

import matplotlib as mpl
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import pyplot as plt

class Song():

    def acquire(self, filename):
        if filename != self.filename:
            return Song(filename)
        return self

    def __init__(self, filename):
        self.filename = filename
        self.y, self.sr = librosa.load(filename, sr=None, mono=True)
        self.item = None

    def set_offset(self, offset):
        if self.item != None:
            pass
        self.off = offset


    def draw_figure(self, canvas, figure, loc=(0, 0)):
        """ Draw a matplotlib figure onto a Tk canvas

        loc: location of top-left corner of figure on canvas in pixels.
        Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        """
        self.canvas = canvas
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        self.photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)

        # Position: convert from top-left anchor to center anchor
        self.item=canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=self.photo)
        canvas.tag_lower(self.item)
        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(self.photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return self.photo


    def draw_waveform(self, canvas, x, y, w, h):
        w = 100*len(self.y)/self.sr
        print('waveform:')
        print(x,y,w,h)

        fig = mpl.figure.Figure(figsize=(w/100, h/100))
        ax = fig.add_axes([0, 0, 1, 1])

        ax.plot(self.y, linewidth=0.5)
        
        ax.set_facecolor('black')
                

        ax.set_xlim(0,len(self.y))
        self.draw_figure(canvas, fig,(x,y))


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack(fill=BOTH, expand=1)


        edit_frame = Frame(frame, height=200)
        edit_frame.pack(side=TOP)

        #song info frame
        self.meta_editor = meta.Editor(self, edit_frame)

        #keyframe editor

        self.keyframe_editor = keyframe.Editor(self, edit_frame)

        #timing frame

        self.track_editor = track.Editor(self, frame)

        self.track_editor.set_callback('send_keyframe', self.keyframe_editor.load_keyframe)
        self.song = None

        self.load_song('./The Fox')
#        self.load_track('./The Fox/Expert.json')

    def load_song(self, loc):
        self.song_dir = loc
        filename = os.path.join(loc, 'info.json')

        data = json.load(open(filename, 'r'))

        self.meta_editor.load_song(data)
        self.track_editor.load_song(data)
        self.load_track()


    def load_track(self):
        loc = self.song_dir
        track = self.meta_editor.active_track
       
        print('Loading song...')
        songname = os.path.join(self.song_dir, track['audioPath'])
        if self.song == None:
            self.song = Song(songname)
        else:
            self.song = self.song.acquire(songname)

        track_file = os.path.join(loc, track['jsonPath'])
        print('loading {}'.format(track_file))

        self._load_track(track, track_file)

        self.track_editor.draw_analysis(self.song)

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

    def _load_track(self, meta, filename):
        """
        Load up the given track.
        """

        data = json.load(open(filename, 'r'))
        self.meta_editor.load_track()
        self.track_editor.clear()
#        self.keyframes = keyframe.Keyframe.load_keyframes(data)
        self.track_editor.load_track(meta, data)
#        self.track_editor.loadloload_keyframes(self.keyframes)



root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
