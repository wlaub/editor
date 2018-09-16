from tkinter import *

import math


class GridCanvas(Canvas):

    def __init__(self, *args, **kwargs):
        self.halo = kwargs.pop('halo', 10)
        self.editor = kwargs.pop('editor')
        super().__init__(*args, **kwargs)

        self._drag_data = {"x": 0, "y": 0, "item": None, 'opts': None}
        self._drag_opts = {}

        self.bind( "<ButtonPress-1>", self.on_press)
        self.bind( "<ButtonRelease-1>", self.on_release)
        self.bind( "<B1-Motion>", self.on_motion)

        def create_token(tag, coord, color):
            x,y = coord
            return self.create_line(x, 0, x, self.cget('height'), fill=color, tags=tag)

        self.register_draggable('line', dragy=False, halo=10, create= create_token)

    def register_draggable(self, tag, create=None, dragx = True, dragy=True, halo=0):
        if create == None: create = self._create_token
        self._drag_opts[tag] = {
            'dragx': dragx,
            'dragy': dragy,
            'halo': halo,
            'create': create
            }

    def create_token(self, tag, coord, *args, **kwargs):
        return self._drag_opts[tag]['create'](tag, coord, *args, **kwargs)

    #TODO: Register drag data for different tokens with optional additional callbacks
    def _create_token(self, tag, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        self.create_oval(x-25, y-25, x+25, y+25, 
                                outline=color, fill=color, tags=tag)

    def on_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        h= self.halo
        rect = [x -h, y-h, x+h, y+h]
        items = self.find_overlapping(*rect)

        items =list(filter(
            lambda x: not all(y not in self._drag_opts.keys() for y in self.gettags(x)), items))

        if len(items) == 0: return
        item = items[0]
        tag = list(filter(lambda x: x in self._drag_opts.keys(), self.gettags(item)))[0]
        self._drag_data['item'] = item
        self._drag_data["x"] = x
        self._drag_data["y"] = y
        self._drag_data['opts'] = self._drag_opts[tag]

        self.editor.focus_keyframe(item)

    def on_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_motion(self, event):
        '''Handle dragging of an object'''
        if self._drag_data["item"] == None: return
        # compute how much the mouse has moved
        opts = self._drag_data['opts']

        delta_x = 0
        delta_y = 0
        if opts['dragx']:
            delta_x = self.canvasx(event.x) - self._drag_data["x"]
        if opts['dragy']:
            delta_y = self.canvasy(event.y) - self._drag_data["y"]
        # move the object the appropriate amount
        self.move(self._drag_data["item"], delta_x, delta_y)
        for item in self.find_withtag('kf-{}'.format(self._drag_data['item'])):
            self.move(item, delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = self.canvasx(event.x)
        self._drag_data["y"] = self.canvasy(event.y)

    def redraw_keyframe(self, item, kf):
        tag = 'kf-{}'.format(item)

        self.delete(tag)
        x1,y1,x2,y2 = self.coords(item)
        x = (x1+x2)/2
        y = (y1+y2)/2
       
        h = y2-y1
        grid = h/4.
        grid /= 2
        hgrid = [y1 + (n+.5)*grid for n in range(4)]

        for xi in range(4):
            for yi in range(3)[::-1]:
                if not (xi,yi) in kf.blocks.keys(): continue
                d,t = kf.blocks[(xi,yi)]
                s = grid*.4*4/(yi+4)
                fill = ['red','blue','white','black'][t]
                self.create_rectangle((
                    x-s, hgrid[xi]-s,
                    x+s, hgrid[xi]+s
                    ), fill=fill, tags=tag)




class Editor():
    """
    Track timeline editor class
    """

    def __init__(self, app, parent):
        self.app=app
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

    def clear(self):
        self.active_keyframe = None
        self.kfmap = []
        self.track_canvas.delete(ALL)

    def get_item(self, kf):
        """
        Reverse lookup on kfmap for the given keyframe
        """
        for k, v in self.kfmap.items():
            if v == kf: return k

    def update_keyframe(self):
        """
        Receive an update from the keyframe editor
        """
        kf = self.active_keyframe
        self.track_canvas.redraw_keyframe(self.get_item(kf), kf)

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
    





