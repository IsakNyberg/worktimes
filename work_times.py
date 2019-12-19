#!/usr/bin/env python3


import wx
import customWX as CWX
import Task

tasks = Task.TaskList()
tasks.import_tasks()


class App(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle("WorkTimes")

        self.button_1 = CWX.Button(self, wx.ID_ANY, "Start")
        self.button_2 = CWX.Button(self, wx.ID_ANY, "Stop")
        self.entry_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_3 = CWX.Button(self, wx.ID_ANY, "Add")
        self.button_4 = CWX.Button(self, wx.ID_ANY, "Settings")
        self.ongoing_list = CWX.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.paused_list = CWX.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.__do_layout()

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.button_1, 0, 0, 0)
        sizer_2.Add(self.button_2, 0, 0, 0)
        sizer_2.Add(self.entry_1, 0, 0, 0)
        sizer_2.Add(self.button_3, 0, 0, 0)
        sizer_2.Add(self.button_4, 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add(self.ongoing_list, 1, wx.EXPAND, 0)
        sizer_1.Add(self.paused_list, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()


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
