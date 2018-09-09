import tkutil
from tkinter import *

import math


class GridCanvas(tkutil.DragCanvas):

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor')
        super().__init__(*args, **kwargs)
        self.halo= 10

        def create_token(tag, coord, color):
            x,y = coord
            return self.create_line(x, 0, x, self.cget('height'), fill=color, tags=tag)

        self.register_draggable('line', dragy=False, halo=10, create= create_token)

    def on_press(self, event):
        item = super().on_press(event)
        self.editor.focus_keyframe(item)        
        
    def redraw_keyframe(self, item, kf):
        tag = 'kf-{}'.format(item)

        self.delete(tag)
        x1,y1,x2,y2 = self.coords(item)
        x = (x1+x2)/2
        y = (y1+y2)/2

        text = 'B:{}\nE:{}\nO:{}'.format(
                len(kf.blocks), len(kf.events), len(kf.obs)
                )
        self.create_text((x,y), text=text, fill='blue', anchor=W) 



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

        self.track_canvas = GridCanvas(timing_frame, height=300, background='black', xscrollcommand=scrollbar.set, scrollregion=(0,0,1000,100), editor=self)
        self.track_canvas.pack(side=TOP, fill=BOTH)

        scrollbar.config(command=self.track_canvas.xview)

        self.active_keyframe = None

        self.callbacks = {}

    def set_callback(self, key, func):
        self.callbacks[key] = func

    def focus_keyframe(self, item):
        if item == None: return
        old = {v:k for k,v in self.kfmap.items()}.get(self.active_keyframe, None)
        if old == item: return
        if old != None:
            self.track_canvas.itemconfig(old, fill='white')
        self.active_keyframe = self.kfmap[item]
        self.track_canvas.itemconfig(item, fill='green')
        self.callbacks.get('send_keyframe', lambda x:x)(self.active_keyframe)

    def load_keyframes(self, kfs):
        self.keyframes = kfs
        self.kfmap = {}
        for i, kf in enumerate(kfs):
            xpos = kf.time*40
            if i == 1:
                self.active_keyframe = kf
                item = self.track_canvas.create_token('line', (xpos, 0), 'green')
            else:
                item = self.track_canvas.create_token('line', (xpos, 0), 'white')
            self.track_canvas.redraw_keyframe(item, kf)
            self.kfmap[item] = kf
        self.callbacks.get('send_keyframe', lambda x:x)(self.active_keyframe)
    





