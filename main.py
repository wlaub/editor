
from tkinter import  *

def make_form(parent, rows):
    for row in rows:
        tframe = Frame(parent)
        for item in row:
            if len(item[0]) > 0:
                label = Label(tframe, text=item[0])
                label.pack(side=LEFT)
            args = []
            kwargs = {}
            try:
                for ak in item[2:]:
                    if isinstance(ak, dict):
                        kwargs = ak
                    else:
                        args = ak
            except: pass
            try:
                control = item[1](tframe, *args, **kwargs)
                control.pack(side=LEFT)
            except:
                print('Form Warning: {}'.format(item[0]))
        tframe.pack(side=TOP)

class BlockCanvas(Canvas):

    def __init__(self, *args, **kwargs):
        self.size = kwargs.pop('size', 100)
        kwargs['width'] = self.size*4+5
        kwargs['height'] = self.size*3+4
        super().__init__(*args, **kwargs)

        self.items = [[0 for x in range(3)] for y in range(4)]

        self.tag_bind('token', "<ButtonPress>", self.on_token_press)
        self.tag_bind('token', "<ButtonRelease>", self.on_token_release)

        for x in range(4):
            for y in range(3):
                self.create_token((1+x*(self.size+1), 1+y*(self.size+1)), 'gray')

    def create_token(self, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        self.create_rectangle( x, y, x+self.size, y+self.size,
                                fill=color, tags="token")

    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        x = event.x
        y = event.y

        item = self.find_closest(x, y)[0]

        if event.num == 1:
            self.itemconfig(item, fill='blue')
        elif event.num == 2:
            pass
        else:
            self.itemconfig(item, fill='red')

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        pass



class DragCanvas(Canvas):
#TODO Move to new file

    def __init__(self, *args, **kwargs):
        self.drag_x = kwargs.pop('drag_x', True)
        self.drag_y = kwargs.pop('drag_y', True)
        self.halo = kwargs.pop('halo', 0)

        super().__init__(*args, **kwargs)

        self._drag_data = {"x": 0, "y": 0, "item": None, 'tag': None}
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
        self._drag_data['tag'] = tag

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
        delta_x = 0
        delta_y = 0
        if self.drag_x:
            delta_x = self.canvasx(event.x) - self._drag_data["x"]
        if self.drag_y:
            delta_y = self.canvasy(event.y) - self._drag_data["y"]
        # move the object the appropriate amount
        self.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = self.canvasx(event.x)
        self._drag_data["y"] = self.canvasy(event.y)


class GridCanvas(DragCanvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.halo= 10

        def create_token(tag, coord, color):
            x,y = coord
            self.create_line(x, 0, x, self.cget('height'), fill=color, tags=tag)

        self.register_draggable('line', dragy=False, halo=10, create= create_token)


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack(fill=BOTH, expand=1)


        edit_frame = Frame(frame, height=200)
        edit_frame.pack(side=TOP)

        #song info frame
        info_frame = Frame(edit_frame)
        info_frame.pack(side=LEFT)

        make_form(info_frame, [
            [['Song Info']],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['', Button, {'text':'button'}]],
            ]) 

        make_form(info_frame, [
            [['Track Info']],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['', Button, {'text':'button'}]],
            ]) 

        #keyframe editor
        key_frame = Frame(edit_frame) #TODO: min width?
        key_frame.pack(side=LEFT)

        self.block_canvas = BlockCanvas(key_frame, bg='gray')
        self.block_canvas.pack(side=LEFT)


        #timing frame

        timing_frame = Frame(frame, height=200)
        timing_frame.pack(side=BOTTOM, fill=BOTH, expand=1)

        timing_control_frame = Frame(timing_frame, width=128, bg='green')
        timing_control_frame.pack(side=LEFT)

        #Timing control frame

        button= Button(timing_control_frame, text='grid')
        button.pack(side=LEFT)

        #timing pane

        scrollbar = Scrollbar(timing_frame, orient=HORIZONTAL)
        scrollbar.pack(side=BOTTOM, fill=X)

        self.track_canvas = GridCanvas(timing_frame, height=300, background='black', xscrollcommand=scrollbar.set, drag_y=False)
        self.track_canvas.pack(side=TOP, fill=BOTH)


        self.track_canvas.create_token('line', (50,0), 'white')
        self.track_canvas.create_token('line', (100,0), 'white')
        self.track_canvas.create_token('line', (5000,0), 'white')

        scrollbar.config(command=self.track_canvas.xview)



root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
