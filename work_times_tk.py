#!/usr/bin/env python3

# -------------------------------------------------------------------------------------------------------------- imports
import settings
from backend import Task
from backend import TaskList


# ------------------------------------------------------------------------------------------------------- Work Times app
class Main_Window:
    def __init__(self):
        self.worktasks = TaskList()
        self.saved = True
        self.sort = 'Random'
        self.theme = 'Default'
        pass
        """
        needs buttons: 
            save
            sort time/abc
            Start | stop
            add
            open settings
        needs fields:
            entry field
            ongoing tasks field
            paused tasks field
        """

    def clock(self):
        """
        Function that calls update evry couple seconds, you may no need it
        """
        pass

    def update(self):
        """
        updates the app including the times inside of the fields
        the time shown on the list should be dependent on either session or not session
        """
        for task in self.worktasks:
            if task.is_ongoing():
                """append task to the ongoing list"""
            else:
                """append task to the paused list"""
        if self.saved:
            """save button neutral colour"""
        else:
            """save button red"""
        pass

    def open_settings(self):
        """
        opens the settings window
        """
        pass

    def save(self):
        """
        Saves the worktasks
        :return: None
        """
        self.worktasks.save()
        self.saved = True
        self.update()
        pass

    def ask_save(self):
        """
        App asks if the user wants to save on quit
        """
        pass

    def sort_abc(self):
        """
        Sorts the tasks in the ListBoxes alphabetically
        :return: None
        """
        self.worktasks.sort_alphabetically(self.sorted == "abc")
        """This sorts the task in the TaskList, ascending or descending is determines by how it was previously sorted"""
        self.sort = 'reversed-abc' if self.sorted == 'abc' else 'abc'
        """This variable stores which direction the TaskList is stored in so that it can be reversed"""
        self.update()
        """The update part is the part that actually sorts the ListBox"""
        pass

    def sort_time(self):
        """
        Sorts the tasks in the ListBoxes by time spent
        :return: None
        """
        self.worktasks.sort_time(self.sorted != "123")
        """This sorts the task in the TaskList, ascending or descending is determines by how it was previously sorted"""
        self.sort = 'reversed-time' if self.sorted == '123' else '123'
        """This variable stores which direction the TaskList is stored in so that it can be reversed"""
        self.update()
        """The update part is the part that actually sorts the ListBox"""
        pass

    def add(self, task_name):
        """
        creates a new task object with the name from task_name and adds it to the task list
        """
        task = Task(task_name)
        self.worktasks.append(task)

        self.saved = False
        self.update()
        pass

    def get_selected_task(self):
        """
        returns the selected task from the menu
        """
        pass

    def start_stop(self):
        """
        starts the selected task
        """
        task = self.get_selected_task()
        if task.is_ongoing():
            task.start()  # backend function
        else:
            task.stop()

        self.saved = False
        self.update()

    def remove_task(self):
        """
        Deletes task that is currently selected in paused listbox
        :return: None
        """
        task = self.get_selected_task()
        self.worktasks.remove(task)

        self.saved = False
        self.update()

    def show_info(self):
        """
        shows the info window
        """
        pass


class Settings_Window:
    def __init__(self, master):
        """
        should have buttons:
            show/hide session
            start new session

            change theme
            change number of rows in both boxes
            disable dialog boxes

            show info button
            add license key (not too important)

            save settings button
            restore settings button
            remove task (or we move this to the main window)
        """
        self.saved = True

    def update(self):
        """
        update the button with dynamic text hide/show, enable/disable and save button turning red
        """

    def remove_task(somethings):
        """
        this task is written as is was in main wndow
        """
        main_window.remove_task()

    def show_info():
        """
        shows the info window
        """

    def save_settings(self):
        """
        Saved settings and changes button colour
        :return: None
        """
        settings.save()
        self.saved = True
        self.update()

    def show_session(self):
        """
        changes the show session value
        """
        settings.session = True
        self.saved = False
        self.update()
        main_window.update()

    @staticmethod
    def new_session():
        """creates a new session
        should only work is the current session is true"""
        main_window.worktasks.new_session()
        main_window.update()
        main_window.saved = False

    def set_ongoing_row(self, rows):
        """
        changes number of ongoing rows
        """
        self.saved = False
        self.is_saved()

    def set_paused_rows(self, rows):
        """
        changes number of paused rows
        """
        self.saved = False

    def warning_dialog(self):
        """changes whether warning dialogs appear, also changes the text of the button"""
        self.saved = False

    def restore(self):
        """ Restores the settings to default"""
        settings.retstore()
        self.saved = False

    def ask_save(self):
        """if not self.saved ask if the user wants to save on exit"""
        pass

    def add_key(self):
        """"""
        pass


# ------------------------------------------------------------------------------------------------------------- Info app
class Info_Window:
    """
    this is just a text window that displays the text from the info file
    """
    def __init__(self):
        """make a nice textbox"""


# ----------------------------------------------------------------------------------------------------- Global variables
if __name__ == "__main__":
    pass
