
from tkinter import  *
import tkutil

import math

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
        kwargs['takefocus'] = True
        super().__init__(*args, **kwargs)

        self.items = [[0 for x in range(3)] for y in range(4)]

        self.bind("<ButtonPress>", self.on_press)
        self.bind("<ButtonRelease>", self.on_release)
        self.bind('<Key>', self.key_down)
        self.bind('<KeyRelease>', self.key_up)
        self.bind('<Enter>', lambda x: self.focus_set())
        self.bind('<Motion>', self.mouse_move)

        self.blue = '#0000cc'
        self.red = '#cc0000'
        self.black = '#000000'

        self.dir = 8
        self.keys_down = []

        self.blocks = {}

        for x in range(4):
            for y in range(3):
                self.blocks[(x,y)] = {'sel': None}
                for i in range(9):
                    items = self.create_token((x,y), self.blue, i)
                    self.blocks[(x,y)][i] = items

    def create_token(self, coord, color, direction=0):
        """
        Token represents the direction (0-8). Color is self.red/blue/black
        0 Up
        1 Down
        2 Left
        3 Right
        4 Up Left
        5 Up Right
        6 Down left
        7 Down Right
        8 No Direction
        """
        (x,y) = coord
#        self.create_rectangle( x, y, x+self.size, y+self.size,
#                                fill=color, tags="token")
#0 is cut up, 1 is cut down, 2 is cut left, 3 is cut right, 4 is cut up left, 5 is cut up right, 6 is cut down left, 7 is cut down right, 8 is cut any direction)

        tag = ('d{}'.format(direction), 'x{}'.format(x), 'y{}'.format(y))

        self.mpos = (0,0)

        x = 1+x*(self.size+1)
        y = 1+y*(self.size+1)

        x+=self.size/2
        y+=self.size/2

        a = [1,0,.5,1.5,.75, 1.25,.25, 1.75, 0][direction]*3.14
        size = self.size*.75
        r = size/2
        verts = [[
            x+r*math.cos(a+3.14/4+3.14*i/2),
            y+r*math.sin(a+3.14/4+3.14*i/2)
            ] for i in range(4)] 
        item = self.create_polygon(*verts, fill=color, tags=(*tag, 'block'))
        self.itemconfigure(item, state=HIDDEN)
        block = item

        if direction < 8:
            verts = [[
                x+r*math.cos(a+3.14/4+3.14*i/2),
                y+r*math.sin(a+3.14/4+3.14*i/2)
                ] for i in range(2,4)]
            i=2.5
            r/=4
            verts.append([
                x+r*math.cos(a+3.14/4+3.14*i/2),
                y+r*math.sin(a+3.14/4+3.14*i/2)
                ])
            item = self.create_polygon(*verts, fill='white', tags=tag)
        elif direction == 8:
            item = self.create_oval(x-r/2, y-r/2, x+r/2, y+r/2, fill='white', tags=tag)
        self.itemconfigure(item, state=HIDDEN)
        arrow = item
        return block,arrow

    def mouse_move(self, event):
        self.mpos = (event.x, event.y)

    def key_down(self, event):
        if event.char in 'wasd': self.keys_down.append(event.char)
        self.dir = self.get_key_dir()
        x, y = self.mpos
        x = math.floor(x/self.size)
        y = math.floor(y/self.size)
        self.update_block_dir(x,y, create=False)

    def key_up(self, event):
        if event.char in self.keys_down: self.keys_down.remove(event.char)
        self.dir = self.get_key_dir()

    def get_key_dir(self):
        keys =''.join(sorted(self.keys_down))
        dirmap = {
            '': 8,
            'w': 0,
            's': 1,
            'a': 2,
            'd': 3,
            'aw':4,
            'dw':5,
            'as':6,
            'ds':7,
            }
        return dirmap.get(keys, self.dir)

    def get_block_stack(self, x, y):
        gentags = ('x{}'.format(x), 'y{}'.format(y))
        dirtag ='d{}'.format(self.dir)
        tagmap = {x: self.gettags(x) for x in self.find_all()}
        result = []
        dmatch = []
        for item, tags in tagmap.items():
            if gentags[0] in tags and gentags[1] in tags:
                result.append(item)
                if dirtag in tags:
                    dmatch.append(item)
        return result, dmatch


    def update_block_dir(self, x, y, create=True):
        blocks = self.blocks[(x,y)]
     

        items, selitems = self.get_block_stack(x,y)
        if create or blocks['sel']!=None:
            blocks['sel'] = self.dir
            for i in range(9):
                if i != self.dir:
                    [self.itemconfig(x, state=HIDDEN) for x in blocks[i]]
                else:
                    selfitems = blocks[i]
                    [self.itemconfig(x, state=NORMAL) for x in blocks[i]]

        return selitems


    def on_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        x = event.x
        y = event.y

        x = math.floor(x/self.size)
        y = math.floor(y/self.size)
        print(x,y)

        items = self.update_block_dir(x,y)
        selitem = list(filter(lambda i: 'block' in self.gettags(i), items))[0]
        if event.num == 1:
            self.itemconfig(selitem, fill=self.blue)
        elif event.num == 2:
            pass
        else:
            self.itemconfig(selitem, fill=self.red)

    def on_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        pass


class GridCanvas(tkutil.DragCanvas):

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

        self.track_canvas = GridCanvas(timing_frame, height=300, background='black', xscrollcommand=scrollbar.set, scrollregion=(0,0,1000,100))
        self.track_canvas.pack(side=TOP, fill=BOTH)


        self.track_canvas.create_token('line', (50,0), 'white')
        self.track_canvas.create_token('line', (100,0), 'white')
        self.track_canvas.create_token('line', (5000,0), 'white')

        scrollbar.config(command=self.track_canvas.xview)



root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
