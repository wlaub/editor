
from tkinter import  *
import tkutil
import keyframe

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

        self.block_canvas = keyframe.BlockCanvas(key_frame, bg='gray')
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
