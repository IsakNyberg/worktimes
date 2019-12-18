#!/usr/bin/env python3

# -------------------------------------------------------------------------------------------------------------- imports


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
        if settings.windows:
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
        This function is only here so i can minimize it in PyCharm.
        This is the ugliest method in the file, you are not meant to look at.
        :return: None or raises errors
        """
        if settings.windows:
            # You're not meant to look at it, simply acknowledge that it works, and don't question how.
            for widget in self.all_button:  # apparently you can make a class Button instead of this, but now its too late
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
            create_new_savefile = messagebox.askyesno("Save file corrupted",
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
            self.master.update()  # this is sometimes needed before messageboxes
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
        Reformat ListBox format to only the taskname
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
        """
        Sorts the tasks in the ListBoxes alphabetically
        :return: None
        """
        self.worktasks.sort_alphabetically(self.sorted == "abc")
        # This sorts the task in the TaskList, ascending or descending is determines by how it was previously sorted
        self.sorted = 'cba' if self.sorted == 'abc' else 'abc'
        # This variable stores which direction the TaskList is stored in so that it can be reversed
        self.update()
        # The update part is the part that actually sorts the ListBox

    def sort_time(self):
        """
        Sorts the tasks in the ListBoxes by time spent
        :return: None
        """
        self.worktasks.sort_time(self.sorted != "123")
        # This sorts the task in the TaskList, ascending or descending is determines by how it was previously sorted
        self.sorted = '321' if self.sorted == '123' else '123'
        # This variable stores which direction the TaskList is stored in so that it can be reversed
        self.update()
        # The update part is the part that actually sorts the ListBox

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
        """
        Shows an info widow using Toplevel
        :return: None
        """
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
        if settings.windows:
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
