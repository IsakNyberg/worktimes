import wx


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


class ListCtrl(wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # important to include style=wx.LC_REPORT

        self.AppendColumn('Name', wx.LIST_FORMAT_LEFT, 200)
        self.AppendColumn('Session', wx.LIST_FORMAT_RIGHT, 50)
        self.AppendColumn('Total', wx.LIST_FORMAT_RIGHT, 50)

    def add_task_list(self, tasklist):
        for task in tasklist:
            self.add_task(task)

    def add_task(self, task):
        task_info = task.get_info()
        pos = self.InsertItem(0, task_info[0])
        self.SetItem(pos, 1, task_info[1])
        self.SetItem(pos, 2, task_info[2])

    def get_selected_tasks(self):
        select_count = self.GetSelectedItemCount()
        selected_tasks = []
        for item in range(select_count):
            choice = self.GetFirstSelected()
            selected_tasks.append(self.GetItem(itemIdx=choice, col=0))
        return selected_tasks
