from tkinter import Button


class ThemedButton(Button):
    def __init__(self, theme, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self['bg'] = theme.bg2
        self['fg'] = theme.fg
        self['borderwidth'] = 10
        self['relief'] = 'flat'
        self['activebackground'] = theme.fg
        self['activeforeground'] = theme.bg
        self['pady'] = 0
        self['padx'] = 2