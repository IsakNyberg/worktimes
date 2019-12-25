#!/usr/bin/env python3


import wx
import customWX as CWX
import Task

TASKS = Task.TaskList()
TASKS.import_tasks()


class App(wx.Dialog):
    def __init__(self, *args, **kwargs):
        kwargs["style"] = kwargs.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetTitle("WorkTimes")

        self.button_1 = CWX.Button(self, wx.ID_ANY, "Start | Stop")
        self.button_1.Bind(wx.EVT_BUTTON, self.start_stop_task)
        self.entry_1 = CWX.TextCtrl(self, wx.ID_ANY, "")
        self.button_3 = CWX.Button(self, wx.ID_ANY, "Add")
        self.button_3.Bind(wx.EVT_BUTTON, self.add_task)
        self.button_4 = CWX.Button(self, wx.ID_ANY, "Settings")
        self.ongoing_list = CWX.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.paused_list = CWX.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.__do_layout()

        self.paused_list.Bind(wx.EVT_LIST_COL_CLICK, self.sort)
        self.ongoing_list.Bind(wx.EVT_LIST_COL_CLICK, self.sort)

        self.timer = CWX.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.update()
        self.timer.Start(20000)

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.button_1, 0, 0, 0)
        sizer_2.Add(self.entry_1, 0, 0, 0)
        sizer_2.Add(self.button_3, 0, 0, 0)
        sizer_2.Add(self.button_4, 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add(self.ongoing_list, 1, wx.EXPAND, 0)
        sizer_1.Add(self.paused_list, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def update(self, event=None):
        TASKS.update()
        self.paused_list.update(TASKS.get_paused())
        self.ongoing_list.update(TASKS.get_ongoing())
        return event

    def start_stop_task(self, event):
        tasknames = []
        tasknames += self.ongoing_list.get_selected_tasks()
        tasknames += self.paused_list.get_selected_tasks()
        for taskname in tasknames:
            task = TASKS.get_task(taskname)
            if task.ongoing:
                task.stop_task()
            else:
                task.start_task()
        self.update(event)
        return event

    def add_task(self, event):
        taskname = self.entry_1.GetValue()
        self.entry_1.SetValue("")
        TASKS.append_new_task(taskname)
        self.update(event)
        return event

    def sort(self, event):
        column = event.GetColumn()
        if column == 0:
            TASKS.sort_alphabetically()
        else:
            TASKS.sort_time(column == 1)
        self.update(event)
        return event


class MyApp(wx.App):
    def OnInit(self):
        self.dialog = App(None, wx.ID_ANY, "")
        self.SetTopWindow(self.dialog)
        self.dialog.ShowModal()
        self.dialog.Destroy()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()


# TODO add popup error window
