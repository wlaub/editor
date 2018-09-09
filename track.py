import tkutil
from tkinter import *

import math


class GridCanvas(tkutil.DragCanvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.halo= 10

        def create_token(tag, coord, color):
            x,y = coord
            self.create_line(x, 0, x, self.cget('height'), fill=color, tags=tag)

        self.register_draggable('line', dragy=False, halo=10, create= create_token)



class Editor():
    """
    Track timeline editor class
    """

    def __init__(self, parent):
        timing_frame = Frame(parent, height=200)
        timing_frame.pack(side=BOTTOM, fill=BOTH, expand=1)

        timing_control_frame = Frame(timing_frame, width=128, bg='green')
        timing_control_frame.pack(side=LEFT)

        #Timing control frame

        button= Button(timing_control_frame, text='grid')
        button.pack(side=LEFT)

        #timing pane

        scrollbar = Scrollbar(timing_frame, orient=HORIZONTAL)
        scrollbar.pack(side=BOTTOM, fill=X)

        self.track_canvas = GridCanvas(timing_frame, height=300, background='black', xscrollcommand=scrollbar.set, scrollregion=(0,0,1000,100))
        self.track_canvas.pack(side=TOP, fill=BOTH)

        self.track_canvas.create_token('line', (50,0), 'white')
        self.track_canvas.create_token('line', (100,0), 'white')
        self.track_canvas.create_token('line', (5000,0), 'white')

        scrollbar.config(command=self.track_canvas.xview)

    def load_keyframes(self, kfs):
        pass



