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

    def append_task(self, task) -> None:
        self.allTasks.append(task)

    def remove_task(self, task) -> None:
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

    def in_task_list(self, task_name) -> bool:
        """
        works the same as in for lists
        :param task_name: String, name of a task
        :return: boolean whether there is a task with that name in the TaskList
        """
        return any(task.get_name() == task_name for task in self.allTasks)

    def get_task(self, task_name):
        """
        Returns Task object with name == task_name
        :param task_name: str name of task
        :return: Task with the name task_name
        """
        for task in self.allTasks:
            if task.get_name() == task_name:
                return task
        return None

    def get_total(self):
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

    def get_name(self):
        return self.name

    def get_total(self):
        return self.total

    def get_session(self):
        return self.session

    def get_start(self):
        return self.start

    def set_name(self, name: str):
        self.name = name

    def set_total(self, total: int):
        self.total = int(total)

    def is_ongoing(self):
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

    def displaytext(self):
        """
        Returns string in format for the listbox in app0 using magic
        :return: str in format name + '   ' + time
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
    def format_time(time_seconds):
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
        self.bg_colour = '#007fc2'  # hexadecimal
        self.bg2_colour = '#006cb2'
        self.fg_colour = '#ffffff'
        self.show_error_messages = True
        self.ongoing_rows = 4
        self.paused_rows = 12
        self.session = False
        self.last_save = 0
        self.key = 'key'
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

    def set_bg(self, colour: str):
        """
        Sets the primary background colour of the app
        :param colour: str hexadecimal
        :return: None
        """
        self.bg_colour = colour

    def set_bg2(self, colour: str):
        """
        Sets the secondary background colour of the app
        :param colour: str hexadecimal
        :return: None
        """
        self.bg2_colour = colour

    def change_fg(self, colour: str):
        """
        Sets the foreground (text) colour of the app
        :param colour: str hexadecimal
        :return: None
        """
        self.fg_colour = colour

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

    def to_string(self):
        """ 
        :return: str of all the settings
        """""
        return ('bg-colour_' + str(self.bg_colour) + '\nbg2-colour_' + str(self.bg2_colour) + '\nfg-colour_' +
                str(self.fg_colour) + '\nshow-error-messages_' + str(self.show_error_messages) + '\nongoing-rows_' +
                str(self.ongoing_rows) + '\npaused-rows_' + str(self.paused_rows) + '\nlast-save_' +
                str(self.last_save) + '\nfont-size_' + str(self.font_size) + '\nsession_' + str(self.session) +
                '\nKey_' + str(self.key))

    def default_settings(self):
        """
        Sets the settings back to default, however does not update their values in app0
        :return: None
        """
        self.bg_colour = '#007fc2'  # hexadecimal
        self.bg2_colour = '#006cb2'
        self.fg_colour = '#ffffff'
        self.show_error_messages = True
        self.session = False
        self.ongoing_rows = 4
        self.paused_rows = 12
        self.last_save = 0
        self.windows = platform.system() == 'Windows'
        self.space = 26 if self.windows else 28
        self.font_size = 12 if self.windows else 16
        self.divide_character = u"\u00A0"  # setting '·'   MAC:' '   '-'   '—'   '…'   '_' win:u"\u00A0"
        self.app_font = ('Courier New', self.font_size)
        self.key = self.key  # should change

    def set_filepaths(self):
        """
        Sets all filepaths to variables in the settings class while accounting for what os the user is using
        :return: None
        """
        if getattr(sys, 'frozen', False):  # frozen
            dir_ = os.path.dirname(sys.executable)
        else:  # unfrozen
            dir_ = os.path.dirname(os.path.realpath(__file__))
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
            self.bg_colour = load[0][1]
            self.bg2_colour = load[1][1]
            self.fg_colour = load[2][1]
            self.show_error_messages = load[3][1] != "False"  # != False so that if file is corrupt it returns True
            self.ongoing_rows = int(load[4][1])
            self.paused_rows = int(load[5][1])
            self.last_save = int(load[6][1])
            # self.font_size = int(load[7][1]) DON'T USE This was a stupid option to change, should be based on platform
            self.session = load[8][1] == "True"  # == True so that if file is corrupt it returns False
            self.key = load[9][1]

            colours = [self.bg_colour, self.bg2_colour, self.fg_colour]
            if any((len(colour) != 7 or colour[0] != '#') for colour in colours):
                raise ValueError  # checking if all colours are hexadecimal #ff0011

        except (FileNotFoundError, UnicodeDecodeError, ValueError):
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

    def full_version(self, entry_key=''):
        """
        compares the hash of the key to a master hash
        :return: bool whether the key matches any of the license hashes
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


# ------------------------------------------------------------------------------------------------------- Work Times app
class App0:
    def __init__(self, master):
        self.sorted = 'random'
        self.saved = True
        self.worktasks = TaskList()

        fg = settings.fg_colour
        bg = settings.bg_colour
        bg2 = settings.bg2_colour
        app_font = settings.app_font
        ongoing_rows = settings.ongoing_rows
        paused_rows = settings.paused_rows
        self.options_button = {"bg": bg2, "fg": fg, "pady": 0, "padx": 2, "borderwidth": 1, "relief": 'flat',
                               "activebackground": fg, "activeforeground": bg}
        self.options_listbox = {"bg": bg, "fg": fg, "borderwidth": 1, "relief": 'sunken',
                                "selectbackground": fg, "selectforeground": bg}
        self.options_frame = {"bg": bg, "fg": fg, "borderwidth": 0, "relief": 'flat'}
        self.options_entry = {"bg": bg, "fg": fg, "borderwidth": 1, "relief": 'sunken'}

        self.master = master
        self.frame = Frame(master)
        self.frame.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.master.iconbitmap(settings.path_icon)
        self.master.title('Work Times')
        self.master.tk_setPalette(background=bg, fg=fg)

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
        self.add_button = Button(self.frame, text="Add", command=self.add)
        self.add_button.grid(row=1, column=5)
        self.entry_label = Label(self.frame, text="New Task:", bg=bg, fg=fg)
        self.entry_label.grid(row=1, column=0)
        self.entry = Entry(self.frame)
        self.entry.grid(row=1, column=1, columnspan=4, sticky=E + W)

        self.ongoing_frame = LabelFrame(self.frame, text="Ongoing", bg=bg, fg=fg)
        self.ongoing_frame.grid(columnspan=6, sticky=E + W + S + N)
        self.ongoing_frame.columnconfigure(0, weight=1)
        self.ongoing = Listbox(self.ongoing_frame, bg=bg, fg=fg, height=ongoing_rows, font=app_font)
        self.ongoing.grid(sticky=E + W + S + N)

        self.paused_frame = LabelFrame(self.frame, text="Paused", bg=bg, fg=fg)
        self.paused_frame.grid(columnspan=6, sticky=E + W + S + N)
        self.paused_frame.columnconfigure(0, weight=1)
        self.paused = Listbox(self.paused_frame, bg=bg, fg=fg, height=paused_rows, font=app_font)
        self.paused.grid(sticky=E + W + S + N)

        self.all_button = [self.save_button, self.start_stop_button, self.sort_time_button,
                           self.refresh_button, self.add_button, self.sort_abc_button]
        self.all_frame = [self.ongoing_frame, self.paused_frame]
        self.all_entry = [self.entry]
        self.all_label = [self.entry_label]
        self.all_listbox = [self.ongoing, self.paused]

        # ------------------------------------------------------------------------------------ Failed to import settings
        if settings.settings_load_error:
            self.master.update()
            messagebox.showerror("Settings file corrupt",
                                 "The settings file could not be read due to unexpected character or format\n"
                                 "The default settings will be used.\n"
                                 "If this error is persistent please restore to default under in the settings window.",
                                 parent=self.master)

        # ------------------------------------------------------------------------------------------------- Import Tasks
        try:
            with open(settings.path_data) as file:  # load tasks
                for line in file:
                    split_line = line.rstrip().split("_")
                    try:
                        self.worktasks.append_task(Task(split_line[0], int(split_line[1]), int(split_line[2])))
                    except IndexError:
                        # this is triggered then the save file is in the old format and then the new file is updates
                        self.worktasks.append_task(Task(split_line[0], int(split_line[1]), 0))

        except FileNotFoundError:

            create_new_savefile = messagebox.askyesno("Save data not found",
                                                      "The data file was not found, do you wish to make a new one?\n"
                                                      "This will cause any previous data to be lost.",
                                                      parent=self.master)
            if create_new_savefile:
                self.worktasks.save()
            else:
                messagebox.showerror("Please review save file",
                                     "Please review the data.txt in order to prevent data loss.\n"
                                     "Program will exit.",
                                     parent=self.master)
            quit()

        except:  # when fails to load tasks, program closes in order to make sure that the previous data isn't lost.
            create_new_savefile = messagebox.askyesno("Save file corrupt",
                                                      "Could not read save file due to unexpected character "
                                                      "or formatting.\n" +
                                                      "do you wish to make a new one?\n"
                                                      "This will cause all previous data to be lost.")
            self.update()
            if create_new_savefile:
                self.worktasks.save()

            else:
                messagebox.showerror("Please review save file",
                                     "Please review the data.txt file in order to prevent data loss.\n\n"
                                     "Program will exit.")
            quit()
        # ------------------------------------------------------------------------------------------------- Starts clock

        self.clock()

        # -------------------------------------------------------------------------------------------- First time prompt
        if len(self.worktasks) + settings.last_save == 0:  # if no tasks and have never been saved generate greeting
            self.master.update()
            new_user = messagebox.askyesno("Welcome!",
                                           "Thank you for using Work Times!\nIs this your first time using this App?",
                                           parent=self.master)
            if new_user:
                self.show_info()
            self.worktasks.save()

    # --------------------------------------------------------------------------------------------- App0 class functions
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
        paused_bg1, paused_bg2 = settings.bg_colour, settings.bg2_colour  # alternating colours and lines
        ongoing_bg1, ongoing_bg2 = settings.bg_colour, settings.bg2_colour
        for task in self.worktasks.get_list():  # adds tasks back into lists
            if task.is_ongoing():
                self.ongoing.insert(END, task.displaytext())
                self.ongoing.itemconfig(END, {'bg': ongoing_bg1})
                ongoing_bg1, ongoing_bg2 = ongoing_bg2, ongoing_bg1
            else:
                self.paused.insert(END, task.displaytext())
                self.paused.itemconfig(END, {'bg': paused_bg1})
                paused_bg1, paused_bg2 = paused_bg2, paused_bg1

        self.master.tk_setPalette(background=settings.bg_colour, fg=settings.fg_colour)
        for widget in self.all_button:
            widget.configure(self.options_button)
        for widget in self.all_listbox:
            widget.configure(self.options_listbox)
        for widget in self.all_frame:
            widget.configure(self.options_frame)
        for widget in self.all_entry:
            widget.configure(self.options_entry)
        self.is_saved()

    def open_settings(self):
        """
        Opens the settings window using Toplevel
        :return: None
        """
        self.settings_window = Toplevel(self.master)
        self.app1 = App1(self.settings_window)
        self.settings_window.protocol("WM_DELETE_WINDOW", self.app1.ask_save)  # prompt when window is closed

    def save(self):
        """
        Saves the worktasks
        :return: None
        """
        if self.worktasks.is_ongoing():
            if settings.show_error_messages:
                messagebox.showerror("Save error", "Cannot save if one or more tasks are ongoing.", parent=self.master)
        self.update()
        self.worktasks.save()
        self.saved = True
        self.is_saved()

    def is_saved(self):
        """
        returns whether project is saved AND changes button colour
        :return: bool if project is saved
        """
        if self.saved and not self.worktasks.is_ongoing():
            self.save_button.configure(self.options_button)
        else:
            self.save_button.configure(bg='#c21234', fg=settings.fg_colour)

        self.saved = self.saved and not self.worktasks.is_ongoing()
        return self.saved

    def ask_save(self):
        """
        should i save?
        :return: None, put triggers a popup
        """
        if self.is_saved():
            root0.destroy()
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

    def add(self):
        """
        Adds task to TaskList and ListBox, while checking for: valid entry, name collusion, full version
        :return: None but appends new task to paused ListBox
        """
        task_name = self.entry.get()
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
        self.entry.delete(0, 'end')  # Deletes entry-field
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

    def show_info(self):
        self.info_window = Toplevel(self.master)
        self.app2 = App2(self.info_window)


# --------------------------------------------------------------------------------------------------------- Settings app
class App1:
    def __init__(self, master):

        self.master = master
        self.frame = Frame(master)
        self.frame.grid()
        self.master.iconbitmap(settings.path_icon)
        self.master.title("Settings")
        self.saved = True
        fg = settings.fg_colour
        bg = settings.bg_colour
        '''bg2 = settings.bg2_colour  # not used but may be at some point
        app_font = settings.app_font
        ongoing_rows = settings.ongoing_rows
        paused_rows = settings.paused_rows
        divide_character = settings.divide_character  # not used but may be at some point'''
        session = settings.session  # this is a static variable, it is not a mistake
        m = {True: "Turn off warning dialogs", False: "Turn on warning dialogs"}
        n = {True: "Show total", False: "Show this session"}

        self.label_show_session = LabelFrame(self.frame, text="Sessions:", bg=bg, fg=fg)
        self.label_show_session.grid(row=0, column=0, columnspan=2)
        self.button_show_session = Button(self.label_show_session, text=n[session], command=self.show_session, width=20, bg=fg, fg=bg)
        self.button_show_session.grid(row=1, column=0, pady=3, padx=1)
        self.button_new_session = Button(self.label_show_session, text="Start new session", command=self.new_session, width=20, bg=fg, fg=bg)
        self.button_new_session.grid(row=1, column=1, pady=3, padx=1)

        self.label_appearance_and_usage = LabelFrame(self.frame, text="Appearance and usage:", bg=bg, fg=fg)
        self.label_appearance_and_usage.grid(row=2, column=0,  columnspan=2)
        # self.label_value = Label(self.label_appearance_and_usage, text="Value", bg=bg, fg=fg)
        # self.label_value.grid(row=2, column=1)
        self.button_text_colour = Button(self.label_appearance_and_usage, text="Change text colour", command=self.fg_colour, width=20, bg=fg, fg=bg)
        self.button_text_colour.grid(row=3, column=0, pady=3, padx=1)
        self.entry_fg = Entry(self.label_appearance_and_usage)
        self.entry_fg.grid(row=3, column=1, columnspan=2)
        self.button_app_colour = Button(self.label_appearance_and_usage, text="Change app colour", command=self.bg_colour, width=20, bg=fg, fg=bg)
        self.button_app_colour.grid(row=4, column=0, pady=3, padx=1)
        self.entry_bg = Entry(self.label_appearance_and_usage)
        self.entry_bg.grid(row=4, column=1, columnspan=2)
        self.button_app2_colour = Button(self.label_appearance_and_usage, text="Change app 2nd colour", command=self.bg2_colour, width=20, bg=fg, fg=bg)
        self.button_app2_colour.grid(row=5, column=0, pady=3, padx=1)
        self.entry_bg2 = Entry(self.label_appearance_and_usage)
        self.entry_bg2.grid(row=5, column=1, columnspan=2)
        self.button_ongoing_rows = Button(self.label_appearance_and_usage, text="Change Ongoing tasks rows", command=self.set_ongoing_rows, width=20, bg=fg, fg=bg)
        self.button_ongoing_rows.grid(row=6, column=0, pady=3, padx=1)
        self.entry_ongoing_rows = Entry(self.label_appearance_and_usage)
        self.entry_ongoing_rows.grid(row=6, column=1, columnspan=2)
        self.button_paused_rows = Button(self.label_appearance_and_usage, text="Change Paused tasks rows", command=self.set_paused_rows, width=20, bg=fg, fg=bg)
        self.button_paused_rows.grid(row=7, column=0, pady=3, padx=1)
        self.entry_paused_rows = Entry(self.label_appearance_and_usage)
        self.entry_paused_rows.grid(row=7, column=1, columnspan=2)
        self.button_warning = Button(self.label_appearance_and_usage, text=m[settings.show_error_messages], command=self.warning_dialog, width=20, bg=fg, fg=bg)
        self.button_warning.grid(row=9, column=0, pady=3, padx=1)

        self.label_info_save = LabelFrame(self.frame, text="Info, Save, Remove task and Restore Settings:", bg=bg, fg=fg)
        self.label_info_save.grid(row=10, column=0,  columnspan=2)
        self.button_settings_save = Button(self.label_info_save, text="Save settings", command=self.save_settings, bg=fg, width=20, fg=bg)
        self.button_settings_save.grid(row=11, column=0, pady=3, padx=1)
        self.button_restore_setting = Button(self.label_info_save, text="Restore default settings", command=self.restore, width=20, bg=fg, fg=bg)
        self.button_restore_setting.grid(row=11, column=1, pady=3, padx=1)
        self.button_show_info = Button(self.label_info_save, text="Show Info help and license", command=self.show_info, width=20, bg=fg, fg=bg)
        self.button_show_info.grid(row=12, column=0, pady=3, padx=1)
        self.button_remove_task = Button(self.label_info_save, text="Remove selected task", command=self.remove_task, width=20, bg=fg, fg=bg)
        self.button_remove_task.grid(row=12, column=1, pady=3, padx=1)

        self.label_license = LabelFrame(self.frame, text="License:", bg=bg, fg=fg)
        self.label_license.grid(row=13, column=0)
        # self.label_key = Label(self.frame, text="Key", bg=bg, fg=fg)
        # self.label_key.grid(row=13, column=1)
        self.button_add_key = Button(self.label_license, text="Enter Key:", command=self.add_key, bg=fg, width=20, fg=bg)
        self.button_add_key.grid(row=14, column=0, pady=3, padx=1)
        self.entry_key = Entry(self.label_license)
        self.entry_key.grid(row=14, column=1)

    # --------------------------------------------------------------------------------------------- App1 class functions

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
        self.button_settings_save.configure(bg=settings.fg_colour, fg=settings.bg_colour)
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

    def set_ongoing_rows(self):
        """
        changed the number of rows in the ongoing ListBox
        :return: None
        """
        try:
            settings.ongoing_rows = int(self.entry_ongoing_rows.get())
            app0.ongoing.configure(height=settings.ongoing_rows)
        except ValueError:
            messagebox.showerror("Change Number of rows", "Input must be a number", parent=self.master)
        self.saved = False
        self.is_saved()

    def set_paused_rows(self):
        """
        changes the number of rows in the paused ListBox
        :return: None
        """
        try:
            settings.paused_rows = int(self.entry_paused_rows.get())
            app0.paused.configure(height=settings.paused_rows)
        except ValueError:
            messagebox.showerror("Change Number of rows", "Input must be a number", parent=self.master)
        self.saved = False
        self.is_saved()

    def bg_colour(self):
        """
        changes the first background colour it takes input from the rgb field and only takes inputs in the format
        '(255,255,255)'
        :return: None
        """
        try:
            colour_tuple = tuple(map(int, self.entry_bg.get()[1:-1].split(",")))
            if any(i > 255 or i < 0 for i in colour_tuple):
                raise ValueError
            bg = '#%02x%02x%02x' % colour_tuple
            settings.bg_colour = bg
            root0.tk_setPalette(background=bg, fg=settings.fg_colour)
        except (TypeError, ValueError):
            messagebox.showerror("Change bg colour", "Colour must be in (R,G,B) format", parent=self.master)
        self.saved = False
        self.is_saved()
        app0.update()

    def bg2_colour(self):
        """
        changes the 2nd background colour it takes input from the rgb field and only takes inputs in the format
        '(255,255,255)'
        :return: None
        """
        try:
            colour_tuple = tuple(map(int, self.entry_bg2.get()[1:-1].split(",")))
            if any(i > 255 or i < 0 for i in colour_tuple):
                raise ValueError
            bg2 = '#%02x%02x%02x' % colour_tuple
            settings.bg2_colour = bg2
        except (TypeError, ValueError):
            messagebox.showerror("Change bg colour", "Colour must be in (R,G,B) format", parent=self.master)
        self.saved = False
        self.is_saved()
        app0.update()

    def fg_colour(self):
        """
        changes the foreground colour (text colour) it takes input from the rgb field and only takes inputs in
        the format '(255,255,255)'
        :return: None
        """
        try:
            colour_tuple = tuple(map(int, self.entry_fg.get()[1:-1].split(",")))
            if any(i > 255 or i < 0 for i in colour_tuple):
                raise ValueError
            fg = '#%02x%02x%02x' % colour_tuple
            settings.fg_colour = fg
            root0.tk_setPalette(background=settings.bg_colour, fg=fg)
            messagebox.showerror("Change fg colour", "Colour has been changed a restart may be required to see full "
                                                     "effect.", parent=self.master)
        except (TypeError, ValueError):
            messagebox.showerror("Change fg colour", "Colour must be in (R,G,B) format", parent=self.master)
        self.saved = False
        self.is_saved()
        app0.update()

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
        result = messagebox.askyesno("Restore settings", "Dettings have been restored to their default value "
                                                         "the app needs to be restarted for this to take full effect.\n"
                                                         "Do you wish to restart now?", icon="question")
        if result:
            quit()

    def is_saved(self):
        """returns whether settings are saved AND changes button colour"""
        if self.saved:
            self.button_settings_save.configure(bg=settings.fg_colour, fg=settings.bg_colour)
        else:
            self.button_settings_save.configure(bg="red", fg=settings.fg_colour)
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

    def add_key(self) -> bool:
        """
        Compares the key from the entry field with the valid ones using the comparision of hashes.
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
        textbox = Text(master, height=28, width=40)
        textbox.pack()
        for line in settings.info[:-1]:
            textbox.insert(END, line + '\n')
        textbox.insert(END, settings.info[-1])  # this is here so that there is no "\n" on the last line


# ----------------------------------------------------------------------------------------------------- Global variables
if __name__ == "__main__":
    settings = Settings()
    root0 = Tk()
    app0 = App0(root0)
    root0.protocol("WM_DELETE_WINDOW", app0.ask_save)
    root0.resizable(0, 0)
    root0.mainloop()

# ------------------------------------------------------------------------------------------------------------------TODO
# TODO: when restoring settings the session button does not change
# TODO: settings.first_time_opened
# TODO: make the settings windows not resizable
# TODO: app0.update vs app0.theme_update
# TODO: Themes
# TODO: app1 appearance update

sys.exit()
