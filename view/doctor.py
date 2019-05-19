# -*- coding: utf-8 -*-
"""
desc: 医生页面
last modified: 2019.5.19
"""

import wx

toolist = ['search', 'add']


class DoctorFrame(wx.Frame):

    def __init__(self, parent, title):
        super(DoctorFrame, self).__init__(
            parent, title=title, size=(800, 500))

        self.InitUI()
        self.Centre()
        self.SetMinSize((800, 500))
        self.SetMaxSize((800, 500))
        self.Show()

    def InitUI(self):

        panel = self.panel = wx.Panel(self)

        sizer = wx.GridBagSizer(0, 30)

        # sizer.Add(RegisterBtn, pos=(3, 2), span=(1, 2), flag=wx.ALL, border=5)

        # ------
        # 工具栏
        # ------

        toolbar = self.CreateToolBar()

        # ----------
        # 查找人员信息
        # ----------

        SearchTool = toolbar.AddTool(
            wx.ID_ANY, 'Search', wx.Bitmap('img/search.png'))

        self.Bind(wx.EVT_TOOL, self.OnSearch, SearchTool)

        # --------------
        # 所有人员信息 列表
        # --------------

        AllTool = toolbar.AddTool(
            wx.ID_ANY, 'All People', wx.Bitmap('img/all.png'))

        self.Bind(wx.EVT_TOOL, self.OnAll, AllTool)

        # ----------
        # 添加人员信息
        # ----------

        AddTool = toolbar.AddTool(
            wx.ID_ANY, 'Add', wx.Bitmap('img/add.png'))

        self.Bind(wx.EVT_TOOL, self.OnAdd, AddTool)

        # ----------
        # 删除人员信息
        # ----------

        DeleteTool = toolbar.AddTool(
            wx.ID_ANY, 'Delete', wx.Bitmap('img/delete.png'))

        self.Bind(wx.EVT_TOOL, self.OnDelete, DeleteTool)

        # ----------
        # 体温信息
        # ----------

        TemperatureTool = toolbar.AddTool(
            wx.ID_ANY, 'Temperature', wx.Bitmap('img/temperature.png'))

        self.Bind(wx.EVT_TOOL, self.OnTemperature, TemperatureTool)

        # ----------
        # 脉搏信息
        # ----------

        PulseTool = toolbar.AddTool(
            wx.ID_ANY, 'Pulse', wx.Bitmap('img/pulse.png'))

        self.Bind(wx.EVT_TOOL, self.OnPulse, PulseTool)

        # ----------
        # 心电信息
        # ----------

        HeartTool = toolbar.AddTool(
            wx.ID_ANY, 'Heart', wx.Bitmap('img/heart.png'))

        self.Bind(wx.EVT_TOOL, self.OnHeart, HeartTool)

        # ----------
        # 报警信息
        # ----------

        AlarmTool = toolbar.AddTool(
            5, 'Alarm', wx.Bitmap('img/alarm.png'))

        self.Bind(wx.EVT_TOOL, self.OnAlarm, AlarmTool)

        # -------
        # 退出工具
        # -------

        QuitTool = toolbar.AddTool(
            wx.ID_ANY, 'Quit', wx.Bitmap('img/quit.png'))

        self.Bind(wx.EVT_TOOL, self.OnQuit, QuitTool)

        # ------
        # 初始化
        # -------
        toolbar.Realize()

        UserNameLabel = wx.StaticText(panel, label="用户名:")
        sizer.Add(UserNameLabel, pos=(0, 0), flag=wx.ALL, border=5)

        # !设置此panel的sizer
        panel.SetSizerAndFit(sizer)

    def OnSearch(self, e):
        print(self.UserNameTextCtrl.GetValue())

    def OnAll(self, e):
        print(self.UserNameTextCtrl.GetValue())

    def OnAdd(self, e):
        print(self.UserNameTextCtrl.GetValue())

    def OnDelete(self, e):
        print(self.UserNameTextCtrl.GetValue())

    def OnTemperature(self, e):
        print(self.UserNameTextCtrl.GetValue())

    def OnPulse(self, e):
        print(self.UserNameTextCtrl.GetValue())

    def OnHeart(self, e):
        print(self.UserNameTextCtrl.GetValue())

    # 警报
    def OnAlarm(self, e):
        self.HidePanel(e.GetId())

    # 如果行为是切换其他panel，隐藏当前panel
    def HidePanel(self, num):
        print(self.panel.GetId())
        self.panel.Destroy()
        self.panel = wx.Panel(self, -1)
        print(num)

    # 创建 警报 页面
    def CreateAlarmPanel():
        pass

    def OnQuit(self, e):
        self.Close()


def main():
    app = wx.App()
    DoctorFrame(None, title='医生平台')
    app.MainLoop()


if __name__ == '__main__':
    main()
