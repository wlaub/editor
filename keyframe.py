from tkinter import *
import math
import time

def make_ui(parent):
    key_frame = Frame(parent) #TODO: min width?
    key_frame.pack(side=LEFT)

    block_canvas = BlockCanvas(key_frame, bg='gray')
    block_canvas.pack(side=LEFT)

    return key_frame, block_canvas

class Editor():
    def __init__(self, parent):
        self.frame = Frame(parent) #TODO: min width?
        self.frame.pack(side=LEFT)

        self.block_canvas = BlockCanvas(self.frame, bg='gray')
        self.block_canvas.pack(side=LEFT)

    def load_keyframe(self, kf):
        self.block_canvas.load_keyframe(kf)


class Keyframe():
    """
    Keyframe class contain a set of notes, events, and walls along with their
    timing information, and provides functions to explore json data representing
    the keyframe. The block canvas will be responsible for loading data from a
    given Keyframe.
    blocks is a dictionary of (x,y) to (direction, type)
    events is dictionary of type: value
    obs is a list of tuples (xpos, height, width, duration) containing all obstacles starting
    this frame
    """
    def __init__(self, time):
        self.time=time
        self.blocks = {}
        self.obs = []
        self.events = {}

    @staticmethod
    def load_keyframes(track):
        """
        Return a list of keyframes loaded from the given track json
        """
        result = []
        lists = {
            'notes': track['_notes'],
            'events': track['_events'],
            'obs': track['_obstacles'],
            }

        while len(lists.keys()) > 0:
            nkey = Keyframe(list(lists.values())[0][0]['_time'])
            result.append(nkey)
            lists= nkey.load_json(**lists)
            lists = {k:v for k,v in lists.items() if len(v) > 0}

        result = sorted(result, key = lambda x: x.time)

        return result

    def cmp(self, t1):
        #Compare times abstractly. Allow for tolerance in the future
        return t1 == self.time

    def load_json(self, notes=[], events=[], obs=[]):
        """
        Given json lists representing each type of item, add any items matching
        this keyframe's time, and return a dictionary of the lists excluding the
        captured items. Keyframe analysis of the song will be achieved by 
        working through the full list of each type of item from the song,
        generating a keyframe for the first item in the list, adding all the
        lists to it, retrieving the reduced lists, and repeating until the lists
        run out.
        """
        result = {'notes':[], 'events':[], 'obs':[]}
        for note in notes:
            if self.cmp(note['_time']):
                x = note['_lineIndex']
                y = note['_lineLayer']
                t = note['_type']
                d = note['_cutDirection']
                self.blocks[(x,y)] = (d,t)
            else:
                result['notes'].append(note)
        for event in events:
            if self.cmp(event['_time']):
                t = event['_type']
                v = event['_value']
                self.events[t]=v
            else:
                result['events'].append(event)
        for ob in obs:
            if self.cmp(ob['_time']):
                x = ob['_lineIndex']
                h = ob['_type']
                w = ob['_width']
                l = ob['_duration']
                self.obs.append((x, h, w, l))
            else:
                result['obs'].append(ob)

        return result

    def get_notes_json(self):
        pass

    def get_events_json(self):
        pass

    def get_obstacles_json(sef):
        pass

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

        self.kf = None

    def clear(self):
        self.delete(ALL)

    def load_keyframe(self, kf):
        self.kf = kf
        self.clear()

        for (x,y),(d,t) in kf.blocks.items():
            self.draw_block(x,y,d,t)


    def draw_block(self, x, y, d, t, kf = 0):
        """
        Draw the defined block with a tag of kf
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

        x = 1+x*(self.size+1)
        y = 1+(2-y)*(self.size+1)

        x+=self.size/2
        y+=self.size/2

        size = self.size*.75
        r = size/2
 
        items = []

        tags = (str(kf))

        if t == 3: #draw a bomb and return
            N = 12
            verts = [[
                x+r*math.cos(3.14*2*i/N)*(.5+.5*(i%2)),
                y+r*math.sin(3.14*2*i/N)*(.5+.5*(i%2)),
                ] for i in range(N)] 
     
            item = self.create_polygon(*verts, fill=self.black, tags=tags)
            return [item]

        a = [1,0,.5,1.5,.75, 1.25,.25, 1.75, 0][d]*3.14

        color = [self.red, self.blue][t]

        verts = [[
            x+r*math.cos(a+3.14/4+3.14*i/2),
            y+r*math.sin(a+3.14/4+3.14*i/2)
            ] for i in range(4)] 
        item = self.create_polygon(*verts, fill=color, tags=tags)
        items.append(item)

        if d < 8:
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
            item = self.create_polygon(*verts, fill='white', tags=tags)
        elif d == 8:
            item = self.create_oval(x-r/2, y-r/2, x+r/2, y+r/2, fill='white', tags=tags)
        items.append(item)
        return items

    def mouse_move(self, event):
        self.mpos = (event.x, event.y)

    def key_down(self, event):
        if event.char in 'wasd': self.keys_down.append(event.char)
        self.dir = self.get_key_dir()
        x, y = self.mpos
        x = math.floor(x/self.size)
        y = math.floor(y/self.size)

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


    def on_press(self, event):
        if self.kf == None: return
        x = event.x
        y = event.y

        x = math.floor(x/self.size)
        y = 2-math.floor(y/self.size)

        ntype = [-1,0,3,1][event.num]

        self.kf.blocks[(x,y)] = (self.dir, ntype)
        self.load_keyframe(self.kf)


    def on_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        pass


