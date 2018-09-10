from tkinter import *

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


class Form():
    """
    Form class that returns and loads dictionaries.
    """

    def __init__(self, parent):
        self.root = Frame(parent)
        self.active_frame = Frame(self.root)
        self.controls = {}

    def add_field(self, label, control, *args, **kwargs):
        default = kwargs.pop('default_value', '')
        key = kwargs.pop('_key', label)
        show_label = kwargs.pop('show_label', True)
        side = kwargs.pop('control_pack', LEFT)

        trace = kwargs.pop('trace', None)

        ctrl_data = {
            'default': default,
            }

        if show_label:
            tlabel = Label(self.active_frame, text=label)
            tlabel.pack(side=side)

        if control == None: return None
        content = StringVar()
        if trace != None:
            content.trace('w', trace)
        ctrl_data['data'] = content
        content.set(default)
        if control == Entry:
            kwargs['textvariable'] = content
        elif control == OptionMenu:
            args= [content, *args]
        ctrl = control(self.active_frame, *args, **kwargs)
        ctrl.pack(side=side, expand=1, fill=X)
        ctrl_data['ctrl'] = ctrl

        self.controls[key] = ctrl_data

        return ctrl


    def row(self):
        self.active_frame.pack(side=TOP, expand=1, fill=X)
        self.active_frame = Frame(self.root)

    def end(self, side=TOP):
        self.active_frame.pack(side=TOP)
        self.root.pack(side=side)

    def set_val(self, key, val):
        self.controls[key]['data'].set(val)

    def reset_om(self, key, nvals):
        om = self.controls[key]
        menu = om['ctrl']['menu']
        lastval = om['data'].get()
        menu.delete(0, 'end')
        for val in nvals:
            menu.add_command(label=val, command = lambda value=val:om['data'].set(value), )


    def get_dict(self):
        return {k:v['data'].get() for k,v in self.controls.items()}
   
    def load_dict(self, data):
        for k,v in self.controls.items():
            if not k in data.keys(): continue
            v['data'].set(data[k])




