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

        self.button_1 = CWX.Button(self, wx.ID_ANY, "Start | Stop", style=wx.BU_EXACTFIT)
        self.button_1.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU))
        self.button_1.Bind(wx.EVT_BUTTON, self.start_stop_task)

        self.entry_1 = CWX.TextCtrl(self, wx.ID_ANY, "")

        self.button_3 = CWX.Button(self, wx.ID_ANY, "", style=wx.BU_EXACTFIT)
        self.button_3.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_MENU))
        self.button_3.Bind(wx.EVT_BUTTON, self.add_task)

        self.button_4 = CWX.Button(self, wx.ID_ANY, "", style=wx.BU_EXACTFIT)
        self.button_4.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_MENU))
        self.button_4.Bind(wx.EVT_BUTTON, self.remove)

        self.button_5 = CWX.Button(self, wx.ID_ANY, "", style=wx.BU_EXACTFIT)
        self.button_5.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_MENU))
        self.button_5.Bind(wx.EVT_BUTTON, self.save)

        self.button_6 = CWX.Button(self, wx.ID_ANY, "", style=wx.BU_EXACTFIT)
        self.button_6.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MENU))

        self.ongoing_list = CWX.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.ongoing_list.Bind(wx.EVT_LIST_COL_CLICK, self.sort)
        self.ongoing_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.deselect_other)

        self.paused_list = CWX.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.paused_list.Bind(wx.EVT_LIST_COL_CLICK, self.sort)
        self.paused_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.deselect_other)

        self.__do_layout()

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
        sizer_2.Add(self.button_5, 0, 0, 0)
        sizer_2.Add(self.button_6, 0, 0, 0)
        sizer_1.Add(sizer_2, 0, 1, 0)
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
            TASKS.start_stop(taskname)
        self.update(event)
        return event

    def save(self, event):
        TASKS.save()
        self.update(event)
        return event

    def remove(self, event):
        tasknames = []
        tasknames += self.ongoing_list.get_selected_tasks()
        tasknames += self.paused_list.get_selected_tasks()
        for taskname in tasknames:
            TASKS.remove_task(taskname)
        self.update(event)
        return event

    def add_task(self, event):
        taskname = self.entry_1.GetValue()
        if taskname == "":
            return event
        self.entry_1.SetValue("")
        TASKS.append_new_task(taskname)
        self.update(event)
        return event

    def sort(self, event):
        self.ongoing_list.deselect_all()
        self.paused_list.deselect_all()
        column = event.GetColumn()
        if column == 0:
            TASKS.sort_alphabetically()
        else:
            TASKS.sort_time(column == 1)
        self.update(event)
        return event

    def deselect_other(self, event):
        """
        This function is here so that an item from both list cannot be selected at the same time
        :param event:
        :return:
        """
        if event.GetEventObject() is self.paused_list:
            self.ongoing_list.deselect_all()
            self.button_1.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU))
        elif event.GetEventObject() is self.ongoing_list:
            self.paused_list.deselect_all()
            self.button_1.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_MENU))
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
    if not TASKS.saved:
        pass


# TODO add popup error window
