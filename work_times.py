import os
import time
import platform
from tkinter import *
from tkinter import messagebox
from tkinter import font
from datetime import datetime, timedelta


# ----------------------------------------------------------------------------------------------------- Global functions
def save(save_list):
    """
    This saves the TaskList into the data.txt file in the fromat
    taskname_session_totaltime
    TaskList:param save_list:
    None:return: void
    """
    open(settings.path_data, 'w').close()  # delete old file
    write = ""
    for task in save_list.get_list():  # makes one massive string following the save format
        write += task.get_name() + "_" + str(task.get_total()) + "_" + str(task.get_session()) + "\n"
    with open(settings.path_data, "a") as saveFile:  # recreate new file
        saveFile.write(write)  # puts massive string in file
    settings.last_save = time.time()

def ask_save():
    """should i save?"""
    if app0.is_saved():
        root0.destroy()
        return
    question = messagebox.askyesnocancel("Save", "Do you want to save before you exit?")
    if question is True:
        save(app0.worktasks)
        root0.destroy()
        return
    if question is False:
        root0.destroy()
        return

def format_time(time):  # formats seconds to 33h 33m format
    days = str(int(time / 86400))
    hours = str(int((time % 86400) / 3600))
    minutes = str(int((time % 3600) / 60))
    if time >= 3600:
        if time >= 86400:
            return days + "D " + hours + "H " + minutes + "M"
        else:
            return hours + "H " + minutes + "M"
    else:
        return minutes + "M"


# ------------------------------------------------------------------------------------------------------ Task List Class
class TaskList:
    def __init__(self):
        self.allTasks = []

    def __len__(self):
        return len(self.allTasks)

    def __repr__(self):
        return string(self.allTasks)

    def get_list(self):
        return self.allTasks

    def append_task(self, task):
        self.allTasks.append(task)

    def remove_task(self, task):
        self.allTasks.remove(task)

    def sort_alphabetically(self, reverse):
        self.allTasks.sort(key=lambda task: task.get_name(), reverse=reverse)

    def sort_time(self, reverse):
        self.allTasks.sort(key=lambda task: task.get_total(), reverse=reverse)

    def is_ongoing(self):
        return any(task.is_ongoing() for task in self.allTasks)

    def in_task_list(self, task_name):
        return any(task.get_name() == task_name for task in self.allTasks)

    def get_task(self, task_name):  # Returns Task object with name == task_name
        for task in self.allTasks:
            if task.get_name() == task_name:
                return task
        return None

    def get_total(self):
        return sum([task.get_total for task in self.allTasks])

    def new_session(self):
        for task in self.allTasks:
            task.new_session()


# ----------------------------------------------------------------------------------------------------------- Task class
class Task:
    def __init__(self, name, total=0, session=0):
        self.name = name
        self.total = total
        self.session = session
        self.ongoing = False
        self.start = 0

    def __repr__(self):
        return str(self.name)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_total(self):
        return self.total

    def get_session(self):
        return self.session

    def set_total(self, total):
        self.total = int(total)

    def get_start(self):
        return self.start

    def is_ongoing(self):
        return self.ongoing

    def new_session(self):
        self.session = 0

    def start_task(self):
        self.start = int(time.time())
        self.ongoing = True

    def stop_task(self):
        self.total += int(time.time() - self.start)
        self.session += int(time.time() - self.start)
        self.ongoing = False
        self.start = 0

    def displaytext(self):
        """Returns string in format for  the listbox in app0"""
        space = settings.space
        divide_character = settings.divide_character
        if self.is_ongoing():
            self.stop_task()
            self.start_task()
        time = format_time(self.total)
        if settings.session:
            time = format_time(self.session)
        if (len(self.name) + len(time)) >= space:
            divide = divide_character
        else:
            divide = divide_character * (space - (len(self.name) + len(time)))
        return self.name + divide + time


# ------------------------------------------------------------------------------------------------------- Settings class
class Settings:
    def __init__(self):
        # ------------- editable
        self.bg_colour = (0, 127, 194)  # Editable stored as hex decimal
        self.bg2_colour = (0, 108, 178)  # Editable stored as hex decimal
        self.fg_colour = (255, 255, 255)  # Editable stored as hex decimal
        self.show_error_messages = True
        self.ongoing_rows = 4
        self.paused_rows = 12
        self.session = False
        self.last_save = 0
        # ------------- dynamic non editable
        self.windows = platform.system() != 'Darwin'
        self.space = 26 if self.windows else 28
        self.font_size = 12 if self.windows else 16
        self.settings_load_error = False
        # ------------- Static non editable
        self.info = []
        self.path_data = ""
        self.path_settings = ""
        self.path_info = ""
        self.path_icon = ""
        # ------------- init methods
        self.fix_colour()
        self.set_filepaths()
        self.load_info()
        self.load_settings()
        # ------------- hard-coded non editable
        self.divide_character = u"\u00A0"  # setting '·'   MAC:' '   '-'   '—'   '…'   '_' win:u"\u00A0"
        self.app_font = ('Courier New', self.font_size)

    def __repr__(self):
        string_settings = self.to_string().split('\n')
        names = [attr for attr in vars(self) if not attr.startswith('__')]
        return str(string_settings[index] + ' : ' + names[index] for index in range(len(string_settings)))

    def set_bg(self, colour):
        self.bg_colour = colour
        self.fix_colour()

    def set_bg2(self, colour):
        self.bg2_colour = colour
        self.fix_colour()

    def change_fg(self, colour):
        self.fg_colour = colour
        self.fix_colour()

    def fix_colour(self):
        self.bg_colour = '#%02x%02x%02x' % self.bg_colour
        self.bg2_colour = '#%02x%02x%02x' % self.bg2_colour
        self.fg_colour = '#%02x%02x%02x' % self.fg_colour

    def set_ongoing(self, rows):
        self.ongoing_rows = rows

    def set_paused(self, rows):
        self.paused_rows = rows

    def to_string(self):
        return ('bg-colour_' + str(self.bg_colour) + '\nbg2-colour_' + str(self.bg2_colour) + '\nfg-colour_' +
                str(self.fg_colour) + '\nshow-error-messages_' + str(self.show_error_messages) + '\nongoing-rows_' +
                str(self.ongoing_rows) + '\npaused-rows_' + str(self.paused_rows) + '\nlast-save_' +
                str(self.last_save) + '\nfont-size_' + str(self.font_size) + '\nsession_' + str(self.session))

    def default_settings(self):
        self.bg_colour = (0, 127, 194)
        self.bg2_colour = (0, 108, 178)
        self.fg_colour = (255, 255, 255)
        self.show_error_messages = True
        self.session = False
        self.ongoing_rows = 4
        self.paused_rows = 12
        self.last_save = 0
        self.windows = platform.system() != 'Darwin'
        self.space = 26 if self.windows else 26
        self.font_size = 12 if self.windows else 16
        self.divide_character = u"\u00A0"  # setting '·'   MAC:' '   '-'   '—'   '…'   '_' win:u"\u00A0"
        self.app_font = ('Courier New', self.font_size)
        self.fix_colour()

    def set_filepaths(self):
        if getattr(sys, 'frozen', False):  # frozen
            dir_ = os.path.dirname(sys.executable)
        else:  # unfrozen
            dir_ = os.path.dirname(os.path.realpath(__file__))
        if platform.system() == 'Darwin':  # windows or mac
            self.path_data = os.path.join(os.path.dirname(dir_), "worktimes/data.txt")
            self.path_settings = os.path.join(os.path.dirname(dir_), "worktimes/settings.rfe")
            self.path_info = os.path.join(os.path.dirname(dir_), "worktimes/info.txt")
            self.path_icon = os.path.join(os.path.dirname(dir_), "worktimes/icon.ico")
        else:
            self.path_data = os.path.join(os.path.dirname(dir_), "worktimes\\data.txt")
            self.path_settings = os.path.join(os.path.dirname(dir_), "worktimes\\settings.rfe")
            self.path_info = os.path.join(os.path.dirname(dir_), "worktimes\\info.txt")
            self.path_icon = os.path.join(os.path.dirname(dir_), "worktimes\\icon.ico")

    def load_info(self):
        try:
            with open(self.path_info, 'r') as infofile:
                for line in infofile:
                    self.info.append(line.rstrip())
        except (FileNotFoundError, UnicodeDecodeError, ValueError):
            self.info = ['Info file could not be read.']

    def load_settings(self):
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
            # self.font_size = int(load[7][1]) This was a stupid option to change, should be based on platform
            self.session = load[8][1] == "True"  # == False so that if file is corrupt it returns False

            colours = [self.bg_colour, self.bg2_colour, self.fg_colour]
            if any((len(colour) != 7 or colour[0] != '#') for colour in colours):
                raise Exception('Colour error')  # checking if all colours are hexadeimal #ff0011

        except (FileNotFoundError, UnicodeDecodeError, ValueError):
            print("Failed to import settings")
            self.default_settings()
            self.settings_load_error = True

    def save_settings(self):
        open(self.path_settings, 'w').close()
        write = settings.to_string()
        with open(self.path_settings, "a") as settings_save_file:
            settings_save_file.write(write)


# -------------------------------------------------------------------------------------------------------- Worktimes app
class App0:
    def __init__(self, master):
        self.sorted = 'random'
        self.saved = True
        self.worktasks = TaskList()
        fg = settings.fg_colour
        bg = settings.bg_colour
        bg2 = settings.bg2_colour  # not used but may be at some point
        app_font = settings.app_font
        ongoing_rows = settings.ongoing_rows
        paused_rows = settings.paused_rows
        divide_character = settings.divide_character  # not used but may be at some point
        session = settings.session  # to do

        self.master = master
        self.frame = Frame(master)
        self.frame.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.master.iconbitmap(settings.path_icon)
        self.master.title('Work Times')
        self.master.tk_setPalette(background=bg, fg=fg)

        App0.saveButton = Button(self.frame, text="Save", command=self.save, bg=fg, fg=bg)
        App0.saveButton.grid(row=0, column=0)
        App0.sortabcButton = Button(self.frame, text="Sort Abc", command=self.sort_abc, bg=fg, fg=bg)
        App0.sortabcButton.grid(row=0, column=1)
        App0.sorttimeButton = Button(self.frame, text="Sort Time", command=self.sort_time, bg=fg, fg=bg)
        App0.sorttimeButton.grid(row=0, column=2)
        App0.startstopButton = Button(self.frame, text="Start|Stop", command=self.start_stop, bg=fg, fg=bg)
        App0.startstopButton.grid(row=0, column=3)
        App0.refreshButton = Button(self.frame, text="⚙", command=self.open_settings, bg=fg, fg=bg)
        App0.refreshButton.grid(row=0, column=5)
        App0.addButton = Button(self.frame, text="Add", command=self.add, bg=fg, fg=bg)
        App0.addButton.grid(row=1, column=5)
        App0.label = Label(self.frame, text="New Task:", bg=bg, fg=fg)
        App0.label.grid(row=1, column=0)
        App0.entry = Entry(self.frame)
        App0.entry.grid(row=1, column=1, columnspan=4, sticky=E + W)

        App0.ongoingFrame = LabelFrame(self.frame, text="Ongoing", bg=bg, fg=fg)
        App0.ongoingFrame.grid(columnspan=6, sticky=E + W + S + N)
        App0.ongoingFrame.columnconfigure(0, weight=1)
        App0.ongoing = Listbox(App0.ongoingFrame, bg=bg, fg=fg, height=ongoing_rows, font=app_font)
        App0.ongoing.grid(sticky=E + W + S + N)

        App0.pausedFrame = LabelFrame(self.frame, text="Paused", bg=bg, fg=fg)
        App0.pausedFrame.grid(columnspan=6, sticky=E + W + S + N)
        App0.pausedFrame.columnconfigure(0, weight=1)
        App0.paused = Listbox(App0.pausedFrame, bg=bg, fg=fg, height=paused_rows, font=app_font)
        App0.paused.grid(sticky=E + W + S + N)

        self.front = [self.saveButton, self.sortabcButton, self.startstopButton, self.sorttimeButton,
                      self.refreshButton, self.addButton]
        self.back = [self.entry, self.ongoing, self.paused, self.ongoingFrame, self.pausedFrame, self.label]

        # ------------------------------------------------------------------------------------ Failed to import settings
        if settings.settings_load_error:
            root0.update()
            messagebox.showerror("Settings file corrupt",
                                 "The settings file could not be read due to unexpected character or format\n"
                                 "The default settings will be used.\n"
                                 "If this error is persistent please restore to default under in the settings window",
                                 parent=root0)

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
            print(FileNotFoundError)

            create_new_savefile = messagebox.askyesno("Save not found",
                                                      "The data file was not found, do you wish to make a new one?\n"
                                                      "This will cause any previous data to be lost",
                                                      parent=None)
            if create_new_savefile:
                save(self.worktasks)
            else:
                messagebox.showerror("Please review save file",
                                     "Please review the data.txt in order to prevent data loss.\n"
                                     "Program will exit.",
                                     parent=None)
            quit()

        except:  # when fails to load tasks, program closes in order to make sure that the previous data isn't lost.
            create_new_savefile = messagebox.askyesno("Save file corrupt",
                                                      "Could not read save file due to unexpected character "
                                                      "or formatting.\n" +
                                                      "do you wish to make a new one?\n"
                                                      "This will cause any previous data to be lost",
                                                      parent=None)
            self.update()
            if create_new_savefile:
                save(self.worktasks)

            else:
                messagebox.showerror("Please review save file",
                                     "Please review the data.txt in order to prevent data loss.\n"
                                     "Program will exit.",
                                     parent=None)
            quit()

        self.clock()

        # -------------------------------------------------------------------------------------------- First time prompt
        if len(self.worktasks) + settings.last_save == 0:  # if no tasks and have never been saved generate greeting
            root0.update()
            new_user = messagebox.askyesno("Welcome!",
                                           "Thank you for using Work Times!\nIs this your first time using this App?",
                                           parent=root0)
            if new_user:
                root3 = Tk()
                textbox = Text(root3, height=28, width=40)
                textbox.pack()
                for line in settings.info:
                    textbox.insert(END, line + "\n")
                root3.mainloop()
            save(self.worktasks)

    # --------------------------------------------------------------------------------------------- App0 class functions
    @staticmethod
    def to_task_name(selection):
        """reformats listboxformat to only the taskname"""
        return selection.split(settings.divide_character)[0]

    def clock(self):
        """Calls self.update every cycle_time ms"""
        cycle_time = 55000  # milliseconds (divide by 1000 to get seconds)
        self.update()
        self.master.after(cycle_time, self.clock)

    def update(self):
        bg = settings.bg_colour
        bg2 = settings.bg2_colour
        fg = settings.fg_colour
        self.paused.delete(0, END)  # empties both lists
        self.ongoing.delete(0, END)
        pausedBG1, pausedBG2 = bg, bg2  # alternating colours and lines
        ongoingBG1, ongoingBG2 = bg, bg2
        for task in self.worktasks.get_list():  # adds tasks back into lists
            if task.is_ongoing():
                self.ongoing.insert(END, task.displaytext())
                self.ongoing.itemconfig(END, {'bg': ongoingBG1})
                ongoingBG1, ongoingBG2 = ongoingBG2, ongoingBG1
            else:
                self.paused.insert(END, task.displaytext())
                self.paused.itemconfig(END, {'bg': pausedBG1})
                pausedBG1, pausedBG2 = pausedBG2, pausedBG1

        self.master.tk_setPalette(background=bg, fg=fg)
        for widget in self.front:
            widget.configure(bg=fg, fg=bg)
        self.is_saved()

    def open_settings(self):
        self.settings_window = Toplevel(self.master)
        self.app = App1(self.settings_window)

    def save(self):
        if self.worktasks.is_ongoing():
            if settings.show_error_messages:
                messagebox.showerror("Save error", "Cannot save when one or more tasks are ongoing", parent=root0)
                return
        save(self.worktasks)
        self.saved = True
        self.update()

    def is_saved(self):
        """returns whether project is saved AND changes button colour"""
        if self.saved:
            App0.saveButton.configure(bg=settings.fg_colour, fg=settings.bg_colour)
        else:
            App0.saveButton.configure(bg="red", fg=settings.fg_colour)

        return self.saved

    def sort_abc(self):
        self.worktasks.sort_alphabetically(self.sorted == "abc")
        self.sorted = 'cba' if self.sorted == 'abc' else 'abc'
        self.update()

    def sort_time(self):
        self.worktasks.sort_time(self.sorted != "123")
        self.sorted = '321' if self.sorted == '123' else '123'
        self.update()

    def add(self):
        task_name = self.entry.get()
        if len(task_name) == 0:
            return
        if self.worktasks.in_task_list(task_name):
            messagebox.showerror("New Task error", "There is already a task with the name: \n '" + task_name + "'",
                                 parent=root0)
            return
        if any(character in task_name for character in ["#", "_", "%", "&", "'", '"']):
            messagebox.showerror("New Task error",
                                 "Do not use any of the following characters in the task name:\n# _ % & ' " + '"',
                                 parent=root0)
            return

        task = Task(task_name)  # Creates new task
        self.worktasks.append_task(task)  # adds new task to TaskList class
        self.paused.insert(END, task.displaytext())  # adds new task to App0 list
        self.entry.delete(0, 'end')  # Deletes entry-field
        self.saved = False
        self.update()

    def start_stop(self):
        """ This method moves selected task from paused to ongoing and vise versa, while recording the time and adds it
        to a value stored in the Task list for the selected task"""
        selection = self.ongoing.curselection()  # checks which listbox that the selected task is in
        if len(selection) == 0:
            selection = self.paused.curselection()
            if len(selection) == 0:  # if no task is selected in either box the it will notify user if open is on
                if settings.show_error_messages:
                    messagebox.showerror("No task selected", "To start or stop a task it needs to be selected.",
                                         parent=root0)
                return self.is_saved()  # returns with no changes

            task_name = self.to_task_name(self.paused.get(selection[0]))  # gets taskname from listbox format
            task = self.worktasks.get_task(task_name)  # gets task object from tasklist using taskname
            task.start_task()
            self.paused.delete(selection[0])  # removes task from paused and adds to ongoing
            self.ongoing.insert(END, task.displaytext())
            self.saved = False
            self.update()
            return
        task_name = self.to_task_name(self.ongoing.get(selection[0]))
        task = self.worktasks.get_task(task_name)
        task.stop_task()
        self.ongoing.delete(selection[0])
        self.paused.insert(END, task.displaytext())
        self.saved = False
        self.update()

    def remove_task(self):
        """ Deletes task that is currently selected in paused listbox """
        selection = self.paused.curselection()
        if len(selection) == 0:  # if no task is selected in either box the it will notify user if open is on
            if settings.show_error_messages:
                messagebox.showerror("No task selected", "Only paused tasks can be removed.",
                                     parent=root0)
        task_name = self.to_task_name(self.paused.get(selection[0]))  # gets taskname from listbox format
        task = self.worktasks.get_task(task_name)  # gets task object from tasklist using taskname
        result = messagebox.askyesno("Remove task?", "Are you sure you want to remove:\n" + task_name +
                                     "\nThis cannot be undone", icon="question")
        if result:
            self.worktasks.remove_task(task)
            self.paused.delete(selection[0])  # removes task from paused
            self.saved = False
            self.update()


# --------------------------------------------------------------------------------------------------------- Settings app
class App1:
    def __init__(self, master):

        self.master = master
        self.frame = Frame(master)
        self.frame.grid()
        self.master.iconbitmap(settings.path_icon)
        self.master.title("Settings")
        fg = settings.fg_colour
        bg = settings.bg_colour
        bg2 = settings.bg2_colour  # not used but may be at some point
        app_font = settings.app_font
        ongoing_rows = settings.ongoing_rows
        paused_rows = settings.paused_rows
        divide_character = settings.divide_character  # not used but may be at some point
        session = settings.session
        m = {True: "Turn off warning dialogs", False: "Turn on warning dialogs"}
        n = {True: "Show total", False: "Show this session"}

        label = Label(self.frame, text="Sessions:", justify=LEFT, bg=bg, fg=fg)
        label.grid(row=0, column=0)
        self.session_button = Button(self.frame, text=n[session], command=self.show_session, width=20, bg=fg, fg=bg)
        self.session_button.grid(row=1, column=0, pady=3, padx=1)
        self.new_session_button = Button(self.frame, text="Start new session", command=self.new_session, width=20, bg=fg,
                                         fg=bg)
        self.new_session_button.grid(row=1, column=1, pady=3, padx=1)
        label = Label(self.frame, text="Appearance and usage:", bg=bg, fg=fg)
        label.grid(row=2, column=0)
        label = Label(self.frame, text="Value", bg=bg, fg=fg)
        label.grid(row=2, column=1)
        self.text_colour = Button(self.frame, text="Change text colour", command=self.fgcolour, width=20, bg=fg, fg=bg)
        self.text_colour.grid(row=3, column=0, pady=3, padx=1)
        self.fg_entry = Entry(self.frame)
        self.fg_entry.grid(row=3, column=1, columnspan=2)
        self.app_colour = Button(self.frame, text="Change app colour", command=self.bgcolour, width=20, bg=fg, fg=bg)
        self.app_colour.grid(row=4, column=0, pady=3, padx=1)
        self.bg_entry = Entry(self.frame)
        self.bg_entry.grid(row=4, column=1, columnspan=2)
        self.app2_colour = Button(self.frame, text="Change app 2nd colour", command=self.bg2colour, width=20, bg=fg,
                                  fg=bg)
        self.app2_colour.grid(row=5, column=0, pady=3, padx=1)
        self.bg2_entry = Entry(self.frame)
        self.bg2_entry.grid(row=5, column=1, columnspan=2)
        self.ongoing_rows = Button(self.frame, text="Change Ongoing tasks rows", command=self.ongoingrowchange,
                                   width=20, bg=fg, fg=bg)
        self.ongoing_rows.grid(row=6, column=0, pady=3, padx=1)
        self.ongoing_rows_entry = Entry(self.frame)
        self.ongoing_rows_entry.grid(row=6, column=1, columnspan=2)
        self.paused_rows = Button(self.frame, text="Change Paused tasks rows", command=self.pausedrowchange, width=20,
                                  bg=fg, fg=bg)
        self.paused_rows.grid(row=7, column=0, pady=3, padx=1)
        self.paused_rows_entry = Entry(self.frame)
        self.paused_rows_entry.grid(row=7, column=1, columnspan=2)
        self.warning = Button(self.frame, text=m[settings.show_error_messages], command=self.warning_dialog, width=20,
                              bg=fg, fg=bg)
        self.warning.grid(row=9, column=0, pady=3, padx=1)
        Label(self.frame, text="Info, Save, Remove task and Restore Settings:", bg=bg, fg=fg).grid(row=10, column=0,
                                                                                                   columnspan=2)
        self.settings_save = Button(self.frame, text="Save settings", command=self.save_settings, bg=fg, width=20,
                                    fg=bg)
        self.settings_save.grid(row=11, column=0, pady=3, padx=1)
        self.restore_setting = Button(self.frame, text="Restore default settings", command=self.restore, width=20,
                                      bg=fg, fg=bg)
        self.restore_setting.grid(row=11, column=1, pady=3, padx=1)
        self.show_info_button = Button(self.frame, text="Show Info help and license", command=self.show_info, width=20,
                                       bg=fg, fg=bg)
        self.show_info_button.grid(row=12, column=0, pady=3, padx=1)
        self.remove_task = Button(self.frame, text="Remove selected task", command=self.remove_task, width=20, bg=fg,
                                  fg=bg)
        self.remove_task.grid(row=12, column=1, pady=3, padx=1)

    # --------------------------------------------------------------------------------------------- App1 class functions
    @staticmethod
    def remove_task():
        app0.remove_task()

    def show_info(self):
        self.settings_window = Toplevel(self.master)
        self.app = App2(self.settings_window)

    def save_settings(self):
        settings.save_settings()
        self.settings_save.configure(bg=settings.fg_colour, fg=settings.bg_colour)

    def show_session(self):
        """Changes whether app0 shows total time or session time, also changes settings button"""
        if not app0.is_saved():
            messagebox.showerror("Save before new session", "You must save before you can start show session")
            return
        if settings.show_error_messages:
            if not settings.session:
                messagebox.showerror("Display Update", "Showing current session", icon="info")
                settings.session = True
                self.session_button.configure(text="Show total time")
            else:
                messagebox.showerror("Display Update", "Showing total work time", icon="info")
                settings.session = False
                self.session_button.configure(text="Show session time")
        app0.update()

    @staticmethod
    def new_session():
        if settings.session:
            app0.worktasks.new_session()
            messagebox.showerror("Session Update", "A new session has been started", icon="info")
        messagebox.showerror("Session Update", "Show current session before starting a new one", icon="info")

    def ongoingrowchange(self):
        global ongoing_rows
        try:
            ongoing_rows = int(self.ongoing_rowsentry.get())
            setting[4][1] = self.ongoing_rowsentry.get()
            App0.completed.configure(height=ongoing_rows)
            self.settingssave.configure(bg="red", fg="white")
        except:
            messagebox.showerror("Change Number of rows", "Input must be a number", parent=self)

    def pausedrowchange(self):
        global paused_rows
        try:
            paused_rows = int(self.paused_rowsentry.get())
            setting[5][1] = self.paused_rowsentry.get()
            App0.tasks.configure(height=paused_rows)
            self.settingssave.configure(bg="red", fg="white")
        except:
            messagebox.showerror("Change Number of rows", "Input must be a number", parent=self)

    def bgcolour(self):
        try:
            bg = '#%02x%02x%02x' % tuple(map(int, self.bg_entry.get()[1:-1].split(",")))
            settings.bg_colour = bg
            root0.tk_setPalette(background=bg, fg=settings.fg_colour)
            self.settings_save.configure(bg="red", fg="white")
        except (TypeError, ValueError):
            messagebox.showerror("Change bg colour", "Colour must be in (R,G,B) format", parent=self)
        app0.update()

    def bg2colour(self):
        """ changes the background colour it takes input from the rgb field and only takes inputs in
                the format '(255,255,255)' """
        try:
            bg2 = '#%02x%02x%02x' % tuple(map(int, self.bg2_entry.get()[1:-1].split(",")))
            settings.bg2_colour = bg2
            self.settings_save.configure(bg="red", fg="white")
        except (TypeError, ValueError):
            messagebox.showerror("Change bg colour", "Colour must be in (R,G,B) format", parent=self)
        app0.update()

    def fgcolour(self):
        """ changes the foreground colour (text colour) it takes input from the rgb field and only takes inputs in
        the format '(255,255,255)' """
        try:
            fg = '#%02x%02x%02x' % tuple(map(int, self.fg_entry.get()[1:-1].split(",")))  # don't touch: one line magic
            settings.fg_colour = fg
            root0.tk_setPalette(background=settings.bg_colour, fg=fg)
            self.settings_save.configure(bg="red", fg="blue")
            messagebox.showerror("Change fg colour", "Colour has been changed\n"
                                                     "a restart may be required to see full effect.",
                                 parent=self.master)
        except (TypeError, ValueError):
            messagebox.showerror("Change fg colour", "Colour must be in (R,G,B) format", parent=self.master)
        app0.update()

    def warning_dialog(self):
        """ changes wheter warning dialogs appear, also changes the text of the button"""
        if settings.show_error_messages:
            settings.show_error_messages = False
            self.warning.configure(text="Turn on warning dialogs")
            messagebox.showerror("Warning dialogs", "Dialogs like this one will no longer be displayed unless necessary"
                                 , icon="info", parent=self)
        elif not settings.show_error_messages:
            settings.show_error_messages = True
            self.warning.configure(text="Turn off warning dialogs")
            messagebox.showerror("Warning dialogs", "Dialogs like this one will now always be displayed", icon="info",
                                 parent=self)
        self.settingssave.configure(bg="red", fg=bg)  # turns the save settings buttnon red

    def restore(self):
        """ Restores the settings to default and restarts the app"""
        result = messagebox.askyesno("Restore settings", "Are you sure you want to restore your settings to default?",
                                     icon="question")
        if result:
            settings.default_settings()
            savesettings(self, setting)
        result = messagebox.askyesno("Restore settings", "settings have been restored to their default value\n"
                                                         "the app needs to be restarted for this to take full effect\n"
                                                         "do you wish to restart now?", icon="question")
        if result:
            quit()


# ------------------------------------------------------------------------------------------------------------- Info app
class App2:
    """ this is just a text window that displays the text from the info file"""

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
    root0.resizable(0, 0)
    root0.protocol("WM_DELETE_WINDOW", ask_save)
    app0 = App0(root0)
    root0.mainloop()
# --------------------------------------------------------------------------------------------------------- save changes

sys.exit()

# ---------------------------------------------------------------------------------------------------------------- TO DO
# :)
