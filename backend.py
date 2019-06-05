#!/usr/bin/env python3
import pickle
import time


class TaskList(list):
    """
    Imports tasks from the pickeled file, sets error flag accordingly.
    """
    def __init__(self, given_tasks=[]):
        self.import_error = False
        self += given_tasks
        if not given_tasks:
            try:
                with open("data.p", "rb") as f:
                    self += pickle.load(f)
            except:
                self.import_error = True

    def sort_alphabetically(self, reverse: bool):
        """
        sorts TaskList alphabetically a-z or z-a
        :param reverse: boolean whether a-z or z-a
        :return: None
        """
        self.sort(key=lambda task: task.get_name(), reverse=reverse)

    def sort_time(self, reverse: bool, session=True):
        """
        sorts TaskList by the recorded time ascending or descending
        :param reverse: boolean whether ascending or descending
        :param session: boolean whether to sort by sesstion or total
        :return:
        """
        self.sort(key=lambda task: task.total, reverse=reverse)
        if session:
            self.sort(key=lambda task: task.session, reverse=reverse)

    def is_ongoing(self) -> bool:
        """
        :return: boolean if there is at least 1 task that is ongoing.
        """
        return any(task.is_ongoing() for task in self)

    def in_task_list(self, task_name: str) -> bool:
        """
        Works the same as 'in' for lists BUT uses str instead of the object.
        :param task_name: String, name of a task
        :return: boolean whether there is a task with that name in the TaskList
        """
        return any(task.get_name() == task_name for task in self)

    def get_task(self, task_name: str):
        """
        Returns Task object with name == task_name
        :param task_name: str name of task
        :return: Task with the name task_name, none if not found
        """
        for task in self:
            if task.get_name() == task_name:
                return task
        return None

    def get_total(self) -> int:
        """
        gets sum of the total time of all tasks
        :return: int total time
        """
        return sum([task.get_total for task in self])

    def new_session(self):
        """
        Sets the session time of all tasks to 0 Does NOT update the app0
        :return: None
        """
        for task in self:
            task.new_session()

    def save(self):
        """
        This saves the TaskList into the data.txt file in the format:
        name_session_total
        :return: None
        """
        with open("data.p", "wb") as f:
            pickle.dump(self, f)


class Task:
    """
    A task object is an object consisting of 5 variables that are used to monitor time. Each task appears in the app0
    list with the name and the time displayed.
    """
    def __init__(self, name, total=0, session=0):
        self.name = name  # Name of task
        self.total = total  # Total Time spent on task. Default = 0
        self.session = session  # Time spend on session. Default = 0
        self.ongoing = False  # private bool, true if task is ongoing otherwise false.
        self.start = 0  # the time.time() when a task is started

    def __repr__(self):
        return str(self.name) + " " + str(self.total) + " " + str(self.session)

    def is_ongoing(self) -> bool:
        return self.ongoing

    def new_session(self):
        """
        sets session time to 0, while total remains the same
        :return: None
        """
        self.session = 0

    def start(self):
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
