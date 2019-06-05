#!/usr/bin/env python3

import platform
import pickle


class Settings:
    def __init__(self):
        # ------------- Functionality
        self.session = True
        self.last_save = 0
        # ------------- Front End
        #self.show_error_messages = True
        #self.ongoing_rows = 111111
        #self.paused_rows = 111111
        #self.theme = 'Default'
        # ------------- dynamic non editable

        self.import_error = False
        try:
            self = Settings.load()
            self.import_error = False  # this needs to be here else the import error is saved
        except:
            self.import_error = True
        finally:
            self.windows = platform.system() == 'Windows'

    def load_info(self):
        """
        Loads the app info from the info.txt
        :return: None
        """
        try:
            with open(self.path_info, 'r') as infofile:
                for line in infofile:
                    self.info.append(line.rstrip())
        except (FileNotFoundError, UnicodeDecodeError, ValueError):
            self.info = ['Info file could not be read.']

    def save(self):
        """
        saves the settings into a pickeled file
        :return: None
        """
        with open("settings.p", "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load():
        """
        Loads settings from he file
        :return: A settings object from the file
        """
        with open("settings.p", "rb") as f:
            return pickle.load(f)

