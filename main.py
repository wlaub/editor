
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

        self.block_canvas = Canvas(key_frame,width=400, height=300, bg='gray')
        self.block_canvas.pack(side=LEFT)

        #timing frame

        timing_frame = Frame(frame, height=800)
        timing_frame.pack(side=BOTTOM, fill=BOTH, expand=1)

        timing_control_frame = Frame(timing_frame, width=64, bg='green')
        timing_control_frame.pack(side=LEFT)

        #Timing control frame

        button= Button(timing_control_frame, text='grid')
        button.pack(side=LEFT)

        #timing pane

        self.timing_pane = PanedWindow(timing_frame, orient='vertical', bg='yellow')
        self.timing_pane.pack(side=RIGHT, fill=BOTH, expand=1)

        self.track_canvas = Canvas(height=100, background='black')
        self.timing_pane.add(self.track_canvas)

        self.keyframe_canvas = Canvas(height=100, background='black')
        self.timing_pane.add(self.keyframe_canvas)

        self.anal_canvas = Canvas(height=100, background='black')
        self.timing_pane.add(self.anal_canvas)


    def say_hi(self):
        print("hi there, everyone!")

root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
