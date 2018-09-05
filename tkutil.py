from tkinter import *

class DragCanvas(Canvas):

    def __init__(self, *args, **kwargs):
        self.halo = kwargs.pop('halo', 0)

        super().__init__(*args, **kwargs)

        self._drag_data = {"x": 0, "y": 0, "item": None, 'opts': None}
        self._drag_opts = {}

        self.bind( "<ButtonPress-1>", self.on_press)
        self.bind( "<ButtonRelease-1>", self.on_release)
        self.bind( "<B1-Motion>", self.on_motion)

    def register_draggable(self, tag, create=None, dragx = True, dragy=True, halo=0):
        if create == None: create = self._create_token
        self._drag_opts[tag] = {
            'dragx': dragx,
            'dragy': dragy,
            'halo': halo,
            'create': create
            }

    def create_token(self, tag, coord, *args, **kwargs):
        self._drag_opts[tag]['create'](tag, coord, *args, **kwargs)

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
        # record the new position
        self._drag_data["x"] = self.canvasx(event.x)
        self._drag_data["y"] = self.canvasy(event.y)


