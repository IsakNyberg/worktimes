import time


# ------------------------------------------------------------------------------------------------------ Task List Class
class TaskList(list):
    """
    List of Task objects
    """
    def __init__(self):
        self.session = True
        self.data_path = 'data.txt'
        self.saved = True
        self.last_save = time.time()

        self.sorted = False

    def __len__(self) -> int:
        return len(self)

    def __repr__(self) -> str:
        return str([task for task in self])

    def get_ongoing(self):
        return [task for task in self if task.ongoing]

    def get_paused(self):
        return [task for task in self if not task.ongoing]

    def update(self):
        for task in self.get_ongoing():
            task.update()

    def rename_task(self, old_name, new_name):
        if self.in_task_list(new_name):
            raise ValueError("Rename error. Already task with name {0}".format(new_name))

        self.get_task(old_name).name = new_name
        self.saved = False

    def append_new_task(self, name):
        if self.get_task(name):
            raise ValueError("Already task with name {0}".format(name))
        self.append(Task(name))
        self.saved = False

    def append_task(self, task):
        self.append(task)
        self.saved = False

    def start_stop(self, taskname):
        task = self.get_task(taskname)
        if task.ongoing:
            task.stop_task()
        else:
            task.start_task()
        self.saved = False

    def remove_task(self, taskname):
        task = self.get_task(taskname)
        if task.ongoing:
            raise ValueError("An ongoing task cannot be removed")
        self.remove(task)
        self.saved = False

    def sort_alphabetically(self):
        """
        sorts TaskList alphabetically a-z or z-a
        :return: None
        """
        self.sort(key=lambda task: task.name, reverse=self.sorted)
        self.sorted = not self.sorted

    def sort_time(self, session=False):
        """
        sorts TaskList by the recorded time ascending or descending
        highest task is at the top.
        :param session: boolean whether session or total
        :return:
        """
        self.sort(key=lambda task: task.total, reverse=self.sorted)
        if session:
            self.sort(key=lambda task: task.session, reverse=self.sorted)
        self.sorted = not self.sorted

    def is_ongoing(self) -> bool:
        """
        :return: boolean if there is at least 1 task that is ongoing.
        """
        return any(task.is_ongoing() for task in self.tasks)

    def in_task_list(self, task_name: str) -> bool:
        """
        Works the same as 'in' for lists
        :param task_name: String, name of a task
        :return: boolean whether there is a task with that name in the TaskList
        """
        return any(task.get_name() == task_name for task in self.tasks)

    def get_task(self, task_name: str):
        """
        Returns Task object with name == task_name
        :param task_name: str name of task
        :return: Task with the name task_name, none if not found
        """
        for task in self:
            if task.name == task_name:
                return task
        return None

    def get_total(self) -> int:
        """
        gets sum of the total time of all tasks
        :return: int total time
        """
        return sum([task.get_total for task in self.tasks])

    def new_session(self):
        """
        Sets the session time of all tasks to 0 Does NOT update the app0
        :return: None
        """
        self.saved = False
        for task in self.tasks:
            task.new_session()

    def save(self):
        """
        This saves the TaskList into the data.txt file in the format:
        name_session_total
        :return: None
        """
        open(self.data_path, 'w').close()  # delete old file
        write = ""
        for task in self:  # makes one massive string following the save format
            write += "{0}_{1}_{2}\n".format(task.name, task.total, task.session)
        with open(self.data_path, "a") as saveFile:  # recreate new file
            saveFile.write(write)  # puts massive string in file
        self.last_save = time.time()

    def import_tasks(self):
        with open(self.data_path) as file:  # load tasks
            for line in file:
                split_line = line.rstrip().split("_")
                try:
                    self.append_task(Task(split_line[0], int(split_line[1]), int(split_line[2])))
                except IndexError:
                    # this is triggered then the save file is in the old format and then the new file is updates
                    self.append_task(Task(split_line[0], int(split_line[1]), 0))


# ----------------------------------------------------------------------------------------------------------- Task class
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
        return str(self.name)

    def get_info(self):
        return [self.name, self.format_time(self.session), self.format_time(self.total)]

    def new_session(self):
        self.session = 0

    def update(self):
        if self.ongoing:
            self.stop_task()
            self.start_task()

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

    def displaytext(self, session) -> str:
        """
        Returns the information of the task in string format.
        For non string format use get_info(self).
        :return: str in format name + ' ' + time
        """
        if self.ongoing:  # makes sure the self.total is accurate
            self.stop()
            self.start()

        formatted_time = self.format_time(self.total)
        if session:
            formatted_time = self.format_time(self.session)

        return "{0} {1}".format(self.name, formatted_time)

    @staticmethod
    def format_time(time_seconds: int) -> str:
        """
        Formats seconds to XXh XXm format
        A day is 24 hours not 12 hours
        :param time_seconds: int time in seconds
        :return: str in the XXh XXm format
        """
        days = int(time_seconds / 86400)  # day is 24 hours not 12 hours
        hours = int((time_seconds % 86400) / 3600)
        minutes = int((time_seconds % 3600) / 60)
        if time_seconds >= 3600:
            if time_seconds >= 86400:
                return "{0}d {1}h {2}m".format(days, hours, minutes)
            else:
                return "{0}h {1}m".format(hours, minutes)
        else:
            return "{0}m".format(minutes)

