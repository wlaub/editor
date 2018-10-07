from tkinter import *
import tkutil

class Editor():

    diffs = ['Easy',
            'Normal',
            'Hard',
            'Expert',
            'Expert+']
 

    def __init__(self, app, parent):
        self.app = app
        info_frame = Frame(parent)
        info_frame.pack(side=LEFT)

        """
            *'authorName': 'name',
            'beatsPerMinute': 120,
            *'coverImagePath': 'cover.jpg',
            'difficultyLevels': [
                ],
            *'environmentName': 'DefaultEnvironment',
            *'previewDuration': 10,
            *'previewStartTime': 12,
            *'songName': 'Song Name',
            *'songSubName': 'Sub Name',
        """

        self.song_form = song = tkutil.Form(info_frame)
        song.add_field('Song Info', None, control_pack=TOP)
        song.row()
        song.add_field('Name', Entry, _key='songName')
        song.row()
        song.add_field('Subtitle', Entry, _key='songSubName')
        song.row()
        song.add_field('Author', Entry, _key='authorName')
        song.add_field('Cover', Entry, default_value='cover.jpg', _key='coverImagePath')
        song.row()
        song.add_field('Environment', OptionMenu,
            'DefaultEnvironment', 
            'BigMirrorEnvironment',
            'TriangleEnvironment',
            'NiceEnvironment',
            default_value='DefaultEnvironment', _key='environmentName')
        song.row()
        song.add_field('Preview Duration', Entry, default_value=10, width = 4, _key='previewDuration')
        song.add_field('Start', Entry, default_value=12, width = 4, _key='previewStartTime')
        song.add_field('BPM', Entry, default_value=120, width=4, _key='beatsPerMinute')

        song.row()

        song.add_field('', Button, show_label=False, text='Add Difficulty',
            command = self.add_track
            )

        song.add_field('Difficulty', OptionMenu,
            'None',
            default_value='None',
            _key = 'difficulty',
            show_label=False
            )

         

        song.end()


        """
        self.spec = {
            'audioPath': 'song.ogg',
            'difficulty': 'Expert',
            'difficultyRank': 4,
            'jsonPath': 'Expert.json',
            'offset': 0,
            'oldOffset': 0
            }
        """
        self.track_form = track = tkutil.Form(info_frame)
        track.add_field('Track Info', None, control_pack=TOP)

        track.row()

        self.track_menu = track.add_field('Difficulty', OptionMenu,
            *self.diffs,
            default_value='Expert+',
            _key = 'difficulty',
            trace=self.sel_track,
            )

        track.row()
        track.add_field('Song File', Entry, default_value='song.ogg',_key='audioPath')
        track.add_field('Offset', Entry, default_value='0', _key='offset', width=8)

        track.end()

        """
        tkutil.make_form(info_frame, [
            [['Track Info']],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['Name', Entry], ['Name2', Entry]],
            [['', Button, {'text':'button'}]],
            ]) 
        """

    def add_track(self):
        diff = self.song_form.get_dict()['difficulty']
        if diff == None: return
        json_path = diff+'.json'
        self.app.create_track(json_path)
        #make new json file at path
        ntrack = {
            'difficulty': diff,
            'jsonPath': json_path,
            }
        self.track_list.append(ntrack)

        self.update_difficulties()
        self.song_form.set_val('difficulty', 'None')
        self.track_form.set_val('difficulty', diff)

    def sel_track(self, *args):
        val = self.track_form.get_dict()['difficulty']
        for track in self.track_list:
            if track['difficulty'] == val:
                self.active_track = track
                self.app.load_track()
                return

    def update_difficulties(self):
        """
        Just update the dropdowns
        """
        nvals = [x['difficulty'] for x in self.track_list]
        self.track_form.reset_om('difficulty', nvals)

        mvals = [x for x in ['None', *self.diffs] if not x in nvals]
        self.song_form.reset_om('difficulty', mvals)

        self.active_track = self.track_list[0]


    def load_song(self, data):
        self.song_form.load_dict(data)
        self.track_list = data['difficultyLevels']
        self.update_difficulties()


    def load_track(self):
        self.track_form.load_dict(self.active_track)

