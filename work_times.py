# -------------------------------------------------------------------------------------------------------------- imports
import os
import time
import platform
from tkinter import *
from tkinter import messagebox
import hashlib


# ------------------------------------------------------------------------------------------------------ Task List Class
class TaskList:
    def __init__(self):
        self.allTasks = []

    def __len__(self) -> int:
        return len(self.allTasks)

    def __repr__(self) -> str:
        return str(self.allTasks)

    def get_list(self):
        return self.allTasks

    def append_task(self, task):
        self.allTasks.append(task)

    def remove_task(self, task):
        self.allTasks.remove(task)

    def sort_alphabetically(self, reverse: bool):
        """
        sorts TaskList alphabetically a-z or z-a
        :param reverse: boolean whether a-z or z-a
        :return: None
        """
        self.allTasks.sort(key=lambda task: task.get_name(), reverse=reverse)

    def sort_time(self, reverse):
        """
        sorts TaskList by the recorded time ascending or descending
        :param reverse: boolean whether ascending or descending
        :return:
        """
        self.allTasks.sort(key=lambda task: task.get_total(), reverse=reverse)
        if settings.session:
            self.allTasks.sort(key=lambda task: task.get_session(), reverse=reverse)

    def is_ongoing(self) -> bool:
        """
        :return: boolean if there is at least 1 task that is ongoing.
        """
        return any(task.is_ongoing() for task in self.allTasks)

    def in_task_list(self, task_name: str) -> bool:
        """
        works the same as in for lists
        :param task_name: String, name of a task
        :return: boolean whether there is a task with that name in the TaskList
        """
        return any(task.get_name() == task_name for task in self.allTasks)

    def get_task(self, task_name: str):
        """
        Returns Task object with name == task_name
        :param task_name: str name of task
        :return: Task with the name task_name
        """
        for task in self.allTasks:
            if task.get_name() == task_name:
                return task
        return None

    def get_total(self) -> int:
        """
        gets sum of the total time of all tasks
        :return: int total time
        """
        return sum([task.get_total for task in self.allTasks])

    def new_session(self):
        """
        Sets the session time of all tasks to 0 Does NOT update the app0
        :return: None
        """
        for task in self.allTasks:
            task.new_session()

    def save(self):
        """
        This saves the TaskList into the data.txt file in the format:
        name_session_total
        :return: None
        """
        open(settings.path_data, 'w').close()  # delete old file
        write = ""
        for task in self.get_list():  # makes one massive string following the save format
            write += task.get_name() + "_" + str(task.get_total()) + "_" + str(task.get_session()) + "\n"
        with open(settings.path_data, "a") as saveFile:  # recreate new file
            saveFile.write(write)  # puts massive string in file
        settings.last_save = int(time.time())

    def import_tasks(self):
        with open(settings.path_data) as file:  # load tasks
            for line in file:
                split_line = line.rstrip().split("_")
                try:
                    self.append_task(Task(split_line[0], int(split_line[1]), int(split_line[2])))
                except IndexError:
                    # this is triggered then the save file is in the old format and then the new file is updates
                    self.append_task(Task(split_line[0], int(split_line[1]), 0))


# ----------------------------------------------------------------------------------------------------------- Task class
class Task:
    def __init__(self, name, total=0, session=0):

        self.name = name
        self.total = total
        self.session = session
        self.ongoing = False
        self.start = 0  # the time.time() when a task is started

    def __repr__(self):
        return str(self.name)

    def get_name(self) -> str:
        return self.name

    def get_total(self) -> int:
        return self.total

    def get_session(self) -> int:
        return self.session

    def get_start(self) -> int:
        return self.start

    def set_name(self, name: str):
        self.name = name

    def set_total(self, total: int):
        self.total = int(total)

    def is_ongoing(self) -> bool:
        return self.ongoing

    def new_session(self):
        self.session = 0

    def start_task(self):
        """
        Records the start time of a task in self.start
        :return: None
        """
        self.start = int(time.time())
        self.ongoing = True

    def stop_task(self):
        """
        Adds the spent time of an ongoing task to total and session
        :return: None
        """
        self.total += int(time.time() - self.start)
        self.session += int(time.time() - self.start)
        self.ongoing = False
        self.start = 0

    def displaytext(self) -> str:
        """
        Returns string in format for the listbox in app0 using magic
        :return: str in format name + ' ... ' + time
        """
        space = settings.space  # the number of spaces in a row in app0
        divide_character = settings.divide_character  # this is the empty character between the task name and the time
        if self.is_ongoing():  # makes sure the self.total is accurate
            self.stop_task()
            self.start_task()
        time_seconds = self.format_time(self.total)
        if settings.session:
            time_seconds = self.format_time(self.session)
        if (len(self.name) + len(time_seconds)) >= space:  # if the string is too long, only one space is used
            divide = divide_character
        else:
            # subtracts the length of the string from the number of spaces
            divide = divide_character * (space - (len(self.name) + len(time_seconds)))
        return self.name + divide + time_seconds

    @staticmethod
    def format_time(time_seconds: int) -> str:
        """
        formats seconds to XXh XXm format
        :param time_seconds: int time in seconds
        :return: str in the XXh XXm format
        """
        days = str(int(time_seconds / 86400))
        hours = str(int((time_seconds % 86400) / 3600))
        minutes = str(int((time_seconds % 3600) / 60))
        if time_seconds >= 3600:
            if time_seconds >= 86400:
                return days + "D " + hours + "H " + minutes + "M"
            else:
                return hours + "H " + minutes + "M"
        else:
            return minutes + "M"


# ------------------------------------------------------------------------------------------------------- Settings class
class Settings:
    def __init__(self):
        """
        Initialises all settings variables and paths
        """
        # ------------- editable in App1
        self.show_error_messages = True
        self.ongoing_rows = 4
        self.paused_rows = 12
        self.session = False
        self.last_save = 0
        self.key = 'key'
        self.theme = 'Default'
        # ------------- dynamic non editable
        self.windows = platform.system() == 'Windows'
        self.space = 26 if self.windows else 29
        self.font_size = 12 if self.windows else 16
        self.settings_load_error = False  # if True it triggers a popup box when app0 is launched
        # ------------- Static non editable
        self.info = []
        self.path_data = ""
        self.path_settings = ""
        self.path_info = ""
        self.path_icon = ""
        self.path = ""
        # ------------- init methods
        self.set_filepaths()
        self.load_info()
        self.load_settings()
        # ------------- hard-coded non editable
        self.divide_character = u"\u00A0"  # other options: '·'   MAC:' '   '-'   '—'   '…'   '_' win:u"\u00A0"
        self.app_font = ('Courier New', self.font_size)

    def __repr__(self):
        """
        Prints all settings
        :return: str, list of all settings
        """
        string_settings = self.to_string().split('\n')
        names = [attr for attr in vars(self) if not attr.startswith('__')]
        return str(string_settings[index] + ' : ' + names[index] for index in range(len(string_settings)))

    def set_ongoing(self, rows: int):
        """
        Sets the number of rows in the 'ongoing' listbox in app0
        :param rows: int number of rows
        :return: None
        """
        self.ongoing_rows = rows

    def set_paused(self, rows: int):
        """
        Sets the number of rows in the 'paused' listbox in app0
        :param rows: int number of rows
        :return: None
        """
        self.paused_rows = rows

    def to_string(self) -> str:
        """ 
        :return: str of all the settings
        """""
        return ('show-error-messages_' + str(self.show_error_messages) + '\nongoing-rows_' +
                str(self.ongoing_rows) + '\npaused-rows_' + str(self.paused_rows) + '\nlast-save_' +
                str(self.last_save) + '\ntheme_' + str(self.theme) + '\nsession_' + str(self.session) +
                '\nKey_' + str(self.key))

    def default_settings(self):
        """
        Sets the settings back to default, however does not update their values in app0
        :return: None
        """
        self.show_error_messages = True
        self.session = True
        self.ongoing_rows = 4
        self.paused_rows = 12
        self.last_save = 0
        self.windows = platform.system() == 'Windows'
        self.space = 26 if self.windows else 29
        self.font_size = 12 if self.windows else 16
        self.divide_character = u"\u00A0"  # alternatives '·'   MAC:' '   '-'   '—'   '…'   '_' win:u"\u00A0"
        self.app_font = ('Courier New', self.font_size)
        self.key = self.key  # should not change
        self.theme = 'Default'

    def set_filepaths(self):
        """
        Sets all filepaths to variables in the settings class while accounting for what os the user is using
        :return: None
        """
        if getattr(sys, 'frozen', False):  # frozen
            dir_ = os.path.dirname(sys.executable)
            self.path = dir_
        else:  # unfrozen
            dir_ = os.path.dirname(os.path.realpath(__file__))
            self.path = dir_
        if self.windows:  # windows or mac
            self.path_data = os.path.join(os.path.dirname(dir_), "worktimes\\data.txt")
            self.path_settings = os.path.join(os.path.dirname(dir_), "worktimes\\settings.rfe")
            self.path_info = os.path.join(os.path.dirname(dir_), "worktimes\\info.txt")
            self.path_icon = os.path.join(os.path.dirname(dir_), "worktimes\\icon.ico")
        else:
            self.path_data = os.path.join(os.path.dirname(dir_), "worktimes/data.txt")
            self.path_settings = os.path.join(os.path.dirname(dir_), "worktimes/settings.rfe")
            self.path_info = os.path.join(os.path.dirname(dir_), "worktimes/info.txt")
            self.path_icon = os.path.join(os.path.dirname(dir_), "worktimes/icon.ico")

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

    def load_settings(self):
        """
        Loads the settings from the settings.rfe file. This is hardcoded since the settings.rfe is just string
        :return: None
        """
        try:
            load = []
            with open(self.path_settings, 'r') as infofile:
                for line in infofile:
                    load.append(line.rstrip('\n').split("_"))
            self.show_error_messages = load[0][1] != "False"  # != False so that if file is corrupt it returns True
            self.ongoing_rows = int(load[1][1])
            self.paused_rows = int(load[2][1])
            self.last_save = int(load[3][1])
            self.theme = load[4][1]
            self.session = load[5][1] != "False"  # != False so that if file is corrupt it returns True
            self.key = load[6][1]
        except (FileNotFoundError, UnicodeDecodeError, ValueError, IndexError):
            self.default_settings()
            self.settings_load_error = True

    def save_settings(self):
        """
        saves settings to the settings.rfe file.
        :return: None
        """
        open(self.path_settings, 'w').close()  # deleted old file
        write = settings.to_string()  # massive string of all settings
        with open(self.path_settings, "a") as settings_save_file:
            settings_save_file.write(write)  # writes massive string to settings.rfe file

    def full_version(self, entry_key='key') -> bool:
        """
        Compares the hash of the key to a master hash, but if the key is already activated, returns true
        :return: bool whether the key matches any of the license hashes or if key is already activated
        """
        hashed_keys = ['8d15e1733fbf3129a9e201c2b7af6024e5c6b1d11fa9893aafc32536e147aec6',
                       'e811be7e5d5cdcad2ce1161b1260c5aa2aae78952626dd206d0b2697a3b7a9de',
                       '394ac5ddcf9dbef4a3456e70d5c3939ff86cae0e08824ba8ed31b6128d7c1a06',
                       '16c47f535cd231bd9d24cfdd1e7342c4dd4f6bc04987988177db4203cb7fccd5',
                       '56df2216dc5a879dca41ad1b0a01b3e0850ea30e7793154ce244133f14a9a350',
                       '3aabbcdb1634ac0324429a92f7613e11c154440b150cf5cfd0e7935669cabe15',
                       'f316a30401ee64677f3cc430134df275590965a4a67569f0809c4040eeecb430',
                       'a42bafae289799bb79ab2f2d71c5e2d8d7e26efc356ffa89166adb658c323f27',
                       'b62a1c6c56ad2367706fe8239bea6a6a7cb0786fa49e7cfa66620f93d8fec471',
                       '9563003439ca0b3f0c0f335a7a50e8f7a96165f63a96081572eab12becedde0a',
                       '8d88650c1058556f6340fc2afd8cdc27e65e41520038e79465efeead2eb4c09d',
                       '638cbbc0f342b002c2a78e65f27b8ead1786bbdb87fc338d5bb1fb52610fb21f']
        settings_match = hashlib.sha256(self.key.encode()).hexdigest() in hashed_keys
        entry_match = hashlib.sha256(entry_key.encode()).hexdigest() in hashed_keys
        return settings_match or entry_match


# ---------------------------------------------------------------------------------------------------------- Theme Class
class Theme:
    def __init__(self, theme_name='default'):
        """
        Imports the theme from a text file. Text-file is chosen based on theme_name.
        If import is failed default theme is set from hardcoded values.
        :param theme_name: str of the name of the theme
        """
        self.available_themes = ['Default', 'Red', 'Green', 'Pink', 'Black', 'White', 'Grey', 'Custom']
        if theme_name not in self.available_themes:  # list of themes
            theme_name = 'Default'
        self.theme_name = theme_name
        if settings.windows:  # windows or mac
            self.path_theme = os.path.join(os.path.dirname(settings.path), "worktimes\\themes\\"+theme_name+".txt")
        else:
            self.path_theme = os.path.join(os.path.dirname(settings.path), "worktimes/themes/"+theme_name+".txt")
        theme = []  # the string from the file
        try:
            with open(self.path_theme, 'r') as theme_file:
                for line in theme_file:
                    theme.append(line.rstrip().split("_"))
            self.fg = theme[0][1]
            self.bg = theme[1][1]
            self.bg2 = theme[2][1]
            self.red = theme[3][1]

            colours = [self.fg, self.bg, self.bg2, self.red]
            for colour in colours:
                if len(colour) != 7 or colour[0] != '#':
                    raise ValueError  # checking if all colours are hexadecimal #ff0011
                if any([character not in "1234567890abcdef" for character in colour[1:]]):
                    raise ValueError

        except (FileNotFoundError, UnicodeDecodeError, ValueError, IndexError):  # if error then default theme
            self.theme_default()

    def theme_default(self):
        """
        sets default theme from hardcoded values
        :return: None but changes the class options
        """
        self.fg = '#ffffff'
        self.bg = '#007fc2'
        self.bg2 = '#006cb2'
        self.red = '#c21234'


# ------------------------------------------------------------------------------------------------------- Work Times app
class App0:
    def __init__(self, master):
        self.sorted = 'random'
        self.saved = True
        self.worktasks = TaskList()
        # -------------- Themes
        self.theme = Theme(settings.theme)
        app_font = settings.app_font
        ongoing_rows = settings.ongoing_rows
        paused_rows = settings.paused_rows
        fg = self.theme.fg
        bg = self.theme.bg
        bg2 = self.theme.bg2
        # -------------- Appearance using too many dictionaries
        self.options_button = {"bg": bg2, "fg": fg, "borderwidth": 1, "relief": "flat",
                               "activebackground": fg, "activeforeground": bg, "pady": 0, "padx": 2}
        self.options_listbox = {"bg": bg, "fg": fg, "borderwidth": 1, "relief": "sunken",
                                "selectbackground": fg, "selectforeground": bg}
        self.options_frame = {"bg": bg, "borderwidth": 2, "relief": "flat"}
        self.options_entry = {"bg": bg, "fg": fg, "borderwidth": 1, "relief": "sunken", "width": 21,
                              "insertbackground": fg, "selectbackground": fg, "selectforeground": bg}
        self.options_label = {"bg": bg, "fg": fg, "borderwidth": 1, "relief": "flat"}
        self.options_label_frame = {"bg": bg, "fg": fg, "borderwidth": 0, "relief": "flat"}
        #  -------------- Master configuration
        self.master = master
        self.master.iconbitmap(settings.path_icon)
        self.master.title('Work Times')
        self.master.tk_setPalette(background=bg, foreground=bg)
        #  -------------- Main Frame
        self.frame = Frame(master)
        self.frame.pack(fill=BOTH, expand=1, padx=0, pady=0)
        #  -------------- Top Menu
        self.save_button = Button(self.frame, text="Save", command=self.save)
        self.save_button.grid(row=0, column=0)
        self.sort_abc_button = Button(self.frame, text="Sort Abc", command=self.sort_abc)
        self.sort_abc_button.grid(row=0, column=1)
        self.sort_time_button = Button(self.frame, text="Sort Time", command=self.sort_time)
        self.sort_time_button.grid(row=0, column=2)
        self.start_stop_button = Button(self.frame, text="Start|Stop", command=self.start_stop)
        self.start_stop_button.grid(row=0, column=3)
        self.refresh_button = Button(self.frame, text="⚙", command=self.open_settings)
        self.refresh_button.grid(row=0, column=5)
        self.entry_label = Label(self.frame, text="New Task:")
        self.entry_label.grid(row=1, column=0)
        self.entry_task_name = Entry(self.frame)
        self.entry_task_name.grid(row=1, column=1, columnspan=4, sticky=E + W)
        self.entry_task_name.bind('<Return>', self.add)  # this causes the task to be added when you press enter
        self.add_button = Button(self.frame, text="Add", command=self.add)
        self.add_button.grid(row=1, column=5)
        #  -------------- The Two Listboxes
        self.ongoing_label_frame = LabelFrame(self.frame, text="Ongoing")
        self.ongoing_label_frame.grid(columnspan=6, sticky=E + W + S + N)
        self.ongoing_label_frame.columnconfigure(0, weight=1)
        self.ongoing = Listbox(self.ongoing_label_frame, height=ongoing_rows, font=app_font)
        self.ongoing.grid(sticky=E + W + S + N)
        self.paused_label_frame = LabelFrame(self.frame, text="Paused")
        self.paused_label_frame.grid(columnspan=6, sticky=E + W + S + N)
        self.paused_label_frame.columnconfigure(0, weight=1)
        self.paused = Listbox(self.paused_label_frame, height=paused_rows, font=app_font)
        self.paused.grid(sticky=E + W + S + N)
        #  -------------- Collection of all widget parts
        self.all_button = [self.save_button, self.start_stop_button, self.sort_time_button, self.refresh_button,
                           self.add_button, self.sort_abc_button]
        self.all_frame = [self.frame]
        self.all_entry = [self.entry_task_name]
        self.all_label = [self.entry_label]
        self.all_listbox = [self.ongoing, self.paused]
        self.all_label_frame = [self.paused_label_frame, self.ongoing_label_frame]

        # --------------- Startup Methods
        self.startup()
        self.clock()

    def startup(self):
        """
        This function is only here so i can minimize it in PyCharm. This is the ugliest method in the file.
        :return: None or raises errors
        """
        # You're not meant to look at it, simply acknowledge that it works, and don't question how.
        for widget in self.all_button:  # apparently you can make a class Button instead but now its too late
            widget.configure(self.options_button)
        for widget in self.all_listbox:
            widget.configure(self.options_listbox)
        for widget in self.all_frame:
            widget.configure(self.options_frame)
        for widget in self.all_entry:
            widget.configure(self.options_entry)
        for widget in self.all_label:
            widget.configure(self.options_label)
        for widget in self.all_label_frame:
            widget.configure(self.options_label_frame)
        self.is_saved()
        self.update()
        # ------------------------------------------------------------------------------------ Failed to import settings
        if settings.settings_load_error:  # settings need to be loaded before this point
            self.master.update()
            messagebox.showerror("Settings file corrupt",
                                 "The settings file could not be read due to unexpected character or format\n"
                                 "The default settings will be used.\n"
                                 "If this error is persistent please restore to default under in the settings window.",
                                 parent=self.master)
        # ------------------------------------------------------------------------------------------------- Import Tasks
        try:  # this method needs to be in app0 because the Task List is a attribute of app0
            self.worktasks.import_tasks()
            return
        except FileNotFoundError:
            create_new_savefile = messagebox.askyesno("Save data not found",
                                                      "The data file was not found, do you wish to make a new one?\n"
                                                      "This will cause any previous data to be lost.")
        except (UnicodeDecodeError, ValueError, IndexError):
            # when fails to load tasks, program closes in order to make sure that the previous data isn't lost.
            create_new_savefile = messagebox.askyesno("Save file corrupt",
                                                      "Could not read save file due to unexpected character "
                                                      "or formatting.\n" +
                                                      "do you wish to make a new one?\n"
                                                      "This will cause all previous data to be lost.")
        if create_new_savefile:
            self.worktasks.save()
            return
        else:
            messagebox.showerror("Please review save file",
                                 "Please review the data.txt file in order to prevent data loss.\n\n"
                                 "Program will exit.")
        quit()
        # -------------------------------------------------------------------------------------------- First time prompt
        if len(self.worktasks) + settings.last_save == 0:  # if no tasks and have never been saved generate greeting
            self.master.update()
            new_user = messagebox.askyesno("Welcome!",
                                           "Thank you for using Work Times!\nIs this your first time using this App?",
                                           parent=self.master)
            if new_user:
                self.show_info()
            self.worktasks.save()

    # ------------------- App0 class functions
    @staticmethod
    def to_task_name(selection):
        """
        reformat ListBox format to only the taskname
        :param selection: A selection object from the listbox
        :return: str returns name of the selected task.
        """
        return selection.split(settings.divide_character)[0]

    def clock(self):
        """
        Calls self.update every cycle_time ms
        :return: None
        """
        cycle_time = 55000  # milliseconds (divide by 1000 to get seconds)
        self.update()
        self.master.after(cycle_time, self.clock)  # remember this needs to be self.clock and NOT self.clock()

    def update(self):
        """
        Updates app0, by deleting all elements from the 2 ListBoxes and appending them again with the updated time.
        :return:None
        """
        self.paused.delete(0, END)  # empties both lists
        self.ongoing.delete(0, END)
        paused_bg1, paused_bg2 = self.theme.bg, self.theme.bg2  # alternating colours and lines
        ongoing_bg1, ongoing_bg2 = self.theme.bg, self.theme.bg2
        for task in self.worktasks.get_list():  # adds tasks back into lists
            if task.is_ongoing():
                self.ongoing.insert(END, task.displaytext())
                self.ongoing.itemconfig(END, {'bg': ongoing_bg1})
                ongoing_bg1, ongoing_bg2 = ongoing_bg2, ongoing_bg1
            else:
                self.paused.insert(END, task.displaytext())
                self.paused.itemconfig(END, {'bg': paused_bg1})
                paused_bg1, paused_bg2 = paused_bg2, paused_bg1
        self.is_saved()

    # noinspection PyAttributeOutsideInit, PyAttributeOutsideInit
    def open_settings(self):
        """
        Opens the settings window using Toplevel
        :return: None
        """
        self.settings_window = Toplevel(self.master)  # must be defined outside __init__ else it will appear on startup
        self.app1 = App1(self.settings_window)
        self.settings_window.protocol("WM_DELETE_WINDOW", self.app1.ask_save)  # prompt when window is closed
        self.settings_window.resizable(0, 0)

    def save(self):
        """
        Saves the worktasks
        :return: None
        """
        if self.worktasks.is_ongoing():
            if settings.show_error_messages:
                messagebox.showerror("Save error", "Cannot save if one or more tasks are ongoing.", parent=self.master)
        self.worktasks.save()
        self.saved = True
        self.update()
        self.is_saved()

    def is_saved(self) -> bool:
        """
        returns whether project is saved AND changes button colour
        :return: bool if project is saved
        """
        if self.saved and not self.worktasks.is_ongoing():
            self.save_button.configure(bg=self.theme.bg2)
        else:
            self.save_button.configure(bg=self.theme.red)

        self.saved = self.saved and not self.worktasks.is_ongoing()
        return self.saved

    def ask_save(self):
        """
        should i save?
        :return: None, put triggers a popup
        """
        if self.is_saved():
            root.destroy()
            return
        self.save_button.flash()
        question = messagebox.askyesnocancel("Save", "Do you want to save before you exit?")
        if question is True:
            self.worktasks.save()
            self.master.destroy()
            return
        if question is False:
            self.master.destroy()
            return

    def sort_abc(self):
        self.worktasks.sort_alphabetically(self.sorted == "abc")
        self.sorted = 'cba' if self.sorted == 'abc' else 'abc'
        self.update()

    def sort_time(self):
        self.worktasks.sort_time(self.sorted != "123")
        self.sorted = '321' if self.sorted == '123' else '123'
        self.update()

    # noinspection PyUnusedLocal
    def add(self, argument=0):
        """
        Adds task to TaskList and ListBox, while checking for: valid entry, name collusion, full version
        :param argument: does Nothing, the argument is only there so that the bind for the entry to work
        with 2 arguments.
        :return: None but appends new task to paused ListBox
        """
        task_name = self.entry_task_name.get()
        if len(task_name) == 0:  # Checks if entry field is empty
            return False
        if self.worktasks.in_task_list(task_name):  # Checks for duplicates
            messagebox.showerror("New Task error", "There is already a task with the name: \n '" + task_name + "'",
                                 parent=self.master)
            return False
        if any(character in task_name for character in ["#", "_", "%", "&", "'", '"']):  # checks for illegal characters
            messagebox.showerror("New Task error",
                                 "Do not use any of the following characters in the task name:\n# _ % & ' " + '"',
                                 parent=self.master)
            return False
        if len(self.worktasks) >= 5 and not settings.full_version():  # checks full version
            messagebox.showerror("Full Version required",
                                 "Please activate the full version in the settings window, or reach out to:\n"
                                 "kjell@nyberg.dev\n"
                                 "To obtain a key.",
                                 parent=self.master)
            return False
        task = Task(task_name)  # Creates new task
        self.worktasks.append_task(task)  # adds new task to TaskList class
        self.entry_task_name.delete(0, 'end')  # Deletes entry-field
        self.saved = False
        self.update()  # this update should also append the task to the app0 ListBox

    def start_stop(self):
        """
        This method moves selected task from paused to ongoing and vise versa, while recording the time and adds it
        to a value stored in the Task list for the selected task
        :return: None
        """
        selection = self.ongoing.curselection()  # checks which listbox that the selected task is in
        if len(selection) == 0:
            selection = self.paused.curselection()
            if len(selection) == 0:  # if no task is selected in either box the it will notify user if open is on
                if settings.show_error_messages:
                    messagebox.showerror("No task selected", "To start or stop a task it needs to be selected.",
                                         parent=self.master)
                return self.is_saved()  # returns with no changes

            task_name = self.to_task_name(self.paused.get(selection[0]))  # gets taskname from listbox format
            task = self.worktasks.get_task(task_name)  # gets task object from tasklist using taskname
            task.start_task()
            self.saved = False
            self.update()
            return self.is_saved()
        task_name = self.to_task_name(self.ongoing.get(selection[0]))
        task = self.worktasks.get_task(task_name)
        task.stop_task()
        self.saved = False
        self.update()
        self.is_saved()

    def remove_task(self):
        """
        Deletes task that is currently selected in paused listbox
        :return: None
        """
        selection = self.paused.curselection()
        if len(selection) == 0:  # if no task is selected in either box the it will notify user if open is on
            if settings.show_error_messages:
                messagebox.showerror("No task selected", "Only paused tasks can be removed.", parent=self.master)
                return
        task_name = self.to_task_name(self.paused.get(selection[0]))  # gets taskname from listbox format
        task = self.worktasks.get_task(task_name)  # gets task object from tasklist using taskname
        result = messagebox.askyesno("Remove task?", "Are you sure you want to remove:\n" + task_name +
                                     "\n\nThis cannot be undone.", icon="question")
        if result:
            self.worktasks.remove_task(task)
            self.saved = False
            self.update()

    # noinspection PyAttributeOutsideInit, PyAttributeOutsideInit
    def show_info(self):
        self.info_window = Toplevel(self.master)   # must be defined outside __init__ else it will appear on startup
        self.app2 = App2(self.info_window)
        self.info_window.resizable(0, 0)


# --------------------------------------------------------------------------------------------------------- Settings app
class App1:
    def __init__(self, master):
        """
        It gets uglier the more you look at it
        :param master: the master that is passed through from app0
        """
        self.master = master
        self.frame = Frame(master, borderwidth=1)
        self.frame.grid()
        self.master.iconbitmap(settings.path_icon)
        self.master.title("Settings")
        self.saved = True

        self.theme = app0.theme
        text_warning_button = "Turn off warning dialogs" if settings.ongoing_rows else "Turn on warning dialogs"
        text_session = "Show total" if settings.session else "Show this session"
        options = self.theme.available_themes
        self.variable_colour = StringVar(master)
        self.variable_colour.set(settings.theme)

        fg = self.theme.fg
        bg = self.theme.bg
        bg2 = self.theme.bg2
        self.options_button = {"bg": bg2, "fg": fg, "borderwidth": 1, "relief": "raised", "activebackground": fg,
                               "activeforeground": bg, "pady": 0, "padx": 2, "width": 20}
        self.options_entry = {"bg": bg, "fg": fg, "borderwidth": 1, "relief": "sunken", "width": 25,
                              "insertbackground": fg, "selectbackground": fg, "selectforeground": bg}
        self.options_label_frame = {"bg": bg, "fg": fg, "borderwidth": 0, "relief": "flat"}

        self.label_show_session = LabelFrame(self.frame, text="Sessions:", bg=bg, fg=fg)
        self.label_show_session.grid(row=0, column=0, columnspan=2)
        self.button_show_session = Button(self.label_show_session, text=text_session, command=self.show_session)
        self.button_show_session.grid(row=1, column=0, ipadx=3)
        self.button_new_session = Button(self.label_show_session, text="Start new session", command=self.new_session)
        self.button_new_session.grid(row=1, column=1, ipadx=3)

        self.label_app_and_use = LabelFrame(self.frame, text="Appearance and usage:")
        self.label_app_and_use.grid(row=2, column=0, columnspan=1)
        self.button_apply_theme = Button(self.label_app_and_use, text="Apply theme", command=self.apply_theme)
        self.button_apply_theme.grid(row=3, column=0)
        self.option_menu_theme = OptionMenu(self.label_app_and_use, self.variable_colour, *options)
        self.option_menu_theme.grid(row=3, column=1)
        self.option_menu_theme['menu'].config(bg=fg, fg=bg)
        self.button_ongoing_rows = Button(self.label_app_and_use, text="Set ongoing eows", command=self.set_ongoing_row)
        self.button_ongoing_rows.grid(row=4, column=0)
        self.entry_ongoing_rows = Entry(self.label_app_and_use)
        self.entry_ongoing_rows.grid(row=4, column=1, columnspan=2)
        self.entry_ongoing_rows.bind('<Return>', self.set_ongoing_row)  # bind enter key
        self.button_paused_rows = Button(self.label_app_and_use, text="Set paused rows", command=self.set_paused_rows)
        self.button_paused_rows.grid(row=5, column=0)
        self.entry_paused_rows = Entry(self.label_app_and_use)
        self.entry_paused_rows.grid(row=5, column=1, columnspan=2)
        self.entry_paused_rows.bind('<Return>', self.set_paused_rows)  # bind enter key
        self.button_warning = Button(self.label_app_and_use, text=text_warning_button, command=self.warning_dialog)
        self.button_warning.grid(row=6, column=0)

        self.label_license = LabelFrame(self.frame, text="License:")
        self.label_license.grid(row=10, column=0)
        self.button_add_key = Button(self.label_license, text="Enter key:", command=self.add_key)
        self.button_add_key.grid(row=11, column=0)
        self.entry_key = Entry(self.label_license)
        self.entry_key.grid(row=11, column=1)
        self.entry_key.bind('<Return>', self.add_key)

        self.label_info_save = LabelFrame(self.frame, text="Info, Save, Remove task and Restore Settings:")
        self.label_info_save.grid(row=12, column=0,  columnspan=2)
        self.button_settings_save = Button(self.label_info_save, text="Save settings", command=self.save_settings)
        self.button_settings_save.grid(row=13, column=0, ipadx=3)
        self.button_restore_setting = Button(self.label_info_save, text="Reset settings", command=self.restore)
        self.button_restore_setting.grid(row=13, column=1, ipadx=3)
        self.button_show_info = Button(self.label_info_save, text="Show Info help and license", command=self.show_info)
        self.button_show_info.grid(row=14, column=0, ipadx=3)
        self.button_remove_task = Button(self.label_info_save, text="Remove selected task", command=self.remove_task)
        self.button_remove_task.grid(row=14, column=1, ipadx=3)

        self.all_button = [self.button_settings_save, self.button_add_key, self.button_new_session,
                           self.button_ongoing_rows, self.button_paused_rows, self.button_remove_task,
                           self.button_restore_setting, self.button_show_info, self.button_show_session,
                           self.option_menu_theme, self.button_warning, self.button_apply_theme]
        self.all_entry = [self.entry_key, self.entry_ongoing_rows,
                          self.entry_paused_rows]
        self.all_label_frame = [self.label_license, self.label_show_session, self.label_app_and_use,
                                self.label_info_save]
        self.full_update()

    # --------------------------------------------------------------------------------------------- App1 class functions
    def full_update(self):
        for widget in self.all_button:
            widget.propagate(0)
            widget.configure(self.options_button)
        for widget in self.all_label_frame:
            widget.configure(self.options_label_frame)
        for widget in self.all_entry:
            widget.configure(self.options_entry)
        self.is_saved()

    @staticmethod
    def remove_task():
        """
        chained methods
        :return: None
        """
        app0.remove_task()

    @staticmethod
    def show_info():
        """
        chained method
        :return: None
        """
        app0.show_info()

    def save_settings(self):
        """
        Saved settings and changes button colour
        :return: None
        """
        settings.save_settings()
        self.saved = True
        self.is_saved()

    def show_session(self):
        """
        Changes whether app0 shows total time or session time, also changes settings button
        :return: None
        """
        if not app0.is_saved():
            messagebox.showerror("Save before new session", "You must save before you can show session.")
            return
        if not settings.session:
            if settings.show_error_messages:
                messagebox.showerror("Display Update", "Showing current session.", icon="info")
            settings.session = True
            self.button_show_session.configure(text="Show total time")
        else:
            if settings.show_error_messages:
                messagebox.showerror("Display Update", "Showing total work time.", icon="info")
            settings.session = False
            self.button_show_session.configure(text="Show session time")
        self.saved = False
        self.is_saved()
        app0.update()

    @staticmethod
    def new_session():
        """
        Starts new session AND updates app0
        :return: None
        """
        if settings.session:
            app0.worktasks.new_session()
            messagebox.showerror("Session Update", "A new session has been started.", icon="info")
            app0.saved = False
            app0.is_saved()
            app0.update()
            return
        messagebox.showerror("Session Update", "Show current session before starting a new one.", icon="info")

    def apply_theme(self):
        """
        This changes the settings.theme variable so a different theme is loaded next startup.
        :return: None
        """
        settings.theme = self.variable_colour.get()
        self.saved = False
        self.is_saved()
        messagebox.showinfo("Theme Update", "Theme has been changed, a restart is required to see full effect.\n\n"
                                            "Remember to save changes.", parent=self.master)

    # noinspection PyUnusedLocal
    def set_ongoing_row(self, argument=0):
        """
        Changed the number of rows in the ongoing ListBox
        :param argument: Not used, ony there so method can take 2 parameters
        :return: None
        """
        try:
            settings.ongoing_rows = int(self.entry_ongoing_rows.get())
            app0.ongoing.configure(height=settings.ongoing_rows)
        except ValueError:
            messagebox.showerror("Change Number of rows", "Input must be a number", parent=self.master)
        self.saved = False
        self.is_saved()

    # noinspection PyUnusedLocal
    def set_paused_rows(self, argument=0):
        """
        changes the number of rows in the paused ListBox
        :param argument: Not used, ony there so method can take 2 parameters
        :return: None
        """
        try:
            settings.paused_rows = int(self.entry_paused_rows.get())
            app0.paused.configure(height=settings.paused_rows)
        except ValueError:
            messagebox.showerror("Change Number of rows", "Input must be a number", parent=self.master)
        self.saved = False
        self.is_saved()

    def warning_dialog(self):
        """changes whether warning dialogs appear, also changes the text of the button"""
        if settings.show_error_messages:
            settings.show_error_messages = False
            self.button_warning.configure(text="Turn on warning dialogs")
            messagebox.showinfo("Warning dialogs", "Dialogs like this one will no longer be displayed unless necessary",
                                parent=self.master)
        elif not settings.show_error_messages:
            settings.show_error_messages = True
            self.button_warning.configure(text="Turn off warning dialogs")
            messagebox.showinfo("Warning dialogs", "Dialogs like this one will now always be displayed",
                                parent=self.master)
        self.saved = False
        self.is_saved()

    @staticmethod
    def restore():
        """ Restores the settings to default and restarts the app"""
        result = messagebox.askyesno("Restore settings", "Are you sure you want to restore your settings to default?",
                                     icon="question")
        if not result:
            return
        settings.default_settings()
        settings.save_settings()
        result = messagebox.askyesno("Restore settings", "Settings have been restored to their default value "
                                                         "the app needs to be restarted for this to take full effect.\n"
                                                         "Do you wish to restart now?", icon="question")
        if result:
            quit()

    def is_saved(self) -> bool:
        """
        returns whether settings are saved AND changes button colour
        :return: bool if settings are saved
        """
        if self.saved:
            self.button_settings_save.configure(bg=self.theme.bg2, fg=self.theme.fg)
        else:
            self.button_settings_save.configure(bg=self.theme.red, fg=self.theme.fg)
        return self.saved

    def ask_save(self):
        """should i save settings?"""
        if self.is_saved():
            self.master.destroy()
            return
        self.button_settings_save.flash()
        question = messagebox.askyesnocancel("Save", "Do you want to save the settings before you close the window?")
        if question is True:
            self.save_settings()
            self.master.destroy()
            return
        if question is False:
            self.master.destroy()
            return

    # noinspection PyUnusedLocal
    def add_key(self, argument=0) -> bool:
        """
        Compares the key from the entry field with the valid ones using the comparision of hashes.
        :param argument: Not used, ony there so method can take 2 parameters
        :return: bool if key was successfully added
        """
        if len(self.entry_key.get()) == 0:  # if field it empty do nothing
            return False

        entry = self.entry_key.get()  # Get entry

        if settings.full_version(entry):  # return true if key is valid
            settings.key = entry  # Updates the key in the settings
            self.save_settings()  # saves the settings
            messagebox.showinfo("Valid Key", "The key you entered is valid.\n"
                                             "The full version of the app is now accessible", parent=self.master)
            return True

        messagebox.showinfo("Invalid Key", "The key you entered does not match any valid key. \n\n"
                                           "If you believe this is an error reach out to:\nkjell@nyberg.dev",
                            parent=self.master)
        return False


# ------------------------------------------------------------------------------------------------------------- Info app
class App2:
    """
    this is just a text window that displays the text from the info file
    """
    def __init__(self, master):
        self.theme = app0.theme
        textbox = Text(master, height=28, width=40, bg=self.theme.bg, fg=self.theme.fg)  # define widget
        textbox.pack()
        for line in settings.info[:-1]:  # settings.info is a list of string that i want to display
            textbox.insert(END, line + '\n')  # adds each element from the settings.info list to the widget
        textbox.insert(END, settings.info[-1])  # this is here so that there is no "\n" on the last line


# ----------------------------------------------------------------------------------------------------- Global variables
if __name__ == "__main__":
    settings = Settings()  # global variable because it is used globally
    root = Tk()
    app0 = App0(root)  # Main window
    root.protocol("WM_DELETE_WINDOW", app0.ask_save)  # defined what happens when app is quit with the window 'x'
    root.resizable(0, 0)  # prevents app from being scaled up
    root.mainloop()

# ------------------------------------------------------------------------------------------------------------------TODO
# TODO: when restoring settings the session button does not change.
# TODO: make text display differently when in total vs session mode.
# TODO: exiting settings app without saving and then reopening will cause the save button to appear saved
# TODO: fix the thing with the invalid number of arguments when you press <Return> in the entry fields


sys.exit()
