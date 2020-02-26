import wx

THEME_BLUE = [(0xff, 0xff, 0xff), (0x00, 0x7f, 0xc2), (0x00, 0x6c, 0xb2)]


class Timer(wx.Timer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, size=(200, -1))


class Button(wx.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Frame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)


class Panel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT)  # important to include style=wx.LC_REPORT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self, 1, wx.EXPAND)
        self.SetSizer(sizer)


class SaveMessageDialog(wx.MessageDialog):
    def __init__(self, parent):
        message = "Do you want to save the unsaved changes?"
        caption = "Unsaved changes"
        super().__init__(parent, message, caption, wx.YES_NO)
        self.SetYesNoLabels('Save', 'Don\'t save')


class ListCtrl(wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AppendColumn('Name', wx.LIST_FORMAT_LEFT, 200)
        self.AppendColumn('Session', wx.LIST_FORMAT_RIGHT, 50)
        self.AppendColumn('Total', wx.LIST_FORMAT_RIGHT, 50)
        self.SetColumnWidth(0, 200)
        self.SetColumnWidth(1, 75)
        self.SetColumnWidth(2, 75)

    def add_task_list(self, tasklist):  # the tasklist can either be a list of task or a tasklist object
        for task in tasklist:
            self.add_task(task)

    def add_task(self, task):
        task_info = task.get_info()
        row = self.InsertItem(0, task_info[0])
        self.SetItem(row, 1, task_info[1])
        self.SetItem(row, 2, task_info[2])

    def get_selected_tasks(self):
        select_count = self.GetSelectedItemCount()
        index = self.GetFirstSelected()
        selected_tasks = []
        for item in range(select_count):
            selected_tasks.append(self.GetItem(itemIdx=index, col=0).GetText())
            index = self.GetNextSelected(index)
        self.deselect_all()
        return selected_tasks

    def hide_session(self):
        self.SetColumnWidth(1, 0)

    def deselect_all(self):
        for row in range(self.GetItemCount()):
            if self.IsSelected(row):
                self.Select(row, 0)

    def get_tasknames(self):
        tasknames = []
        for row in range(self.GetItemCount()):
            tasknames.append(self.GetItem(itemIdx=row, col=0).GetText())
        return tasknames

    def apply_theme(self, theme):
        # TODO
        text = wx.Colour(*theme[0])
        background = wx.Colour(*theme[1])
        self.SetTextColour(text)
        self.SetBackgroundColour(background)

        # im not sure why the lines below don't work
        # self.SetHeaderAttr(wx.ItemAttr(text, background))
        # self.SetAlternateRowColour(wx.Colour(*theme[2]))
        # self.EnableAlternateRowColours()

    def update(self, tasklist):
        # Makes the two lists equal length
        len_dif = self.GetItemCount() - len(tasklist)
        if len_dif > 0:
            for index in range(len_dif):
                self.DeleteItem(0)
        elif len_dif < 0:
            for index in range(-len_dif):
                self.add_task(tasklist[index])

        # populate the table
        row = 0
        for task in tasklist:
            task_info = task.get_info()
            self.SetItem(row, 0, task_info[0])
            self.SetItem(row, 1, task_info[1])
            self.SetItem(row, 2, task_info[2])
            row += 1

