# -*- coding: utf-8 -*-
"""
desc: 病人页面
last modified: 2019.5.20
"""

import wx
import wx.grid as table
import wx.lib.scrolledpanel as scrolled
import numpy
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import os

# 保存全局状态，基本信息，图表信息，不再继续请求
userdata = {}


class PatientFrame(wx.Frame):

    def __init__(self, parent, title, user):
        super(PatientFrame, self).__init__(
            parent, title=title, size=(800, 400))
        global userdata
        userdata = user
        # 用户 全局状态
        print(userdata)
        self.InitUI()
        self.Centre()

        #! self.SetMinSize((800, 500))

        # self.SetMaxSize((800, 500))
        # self.Show()

        self.current = 1

    def InitUI(self):

        self.panel = panel = wx.Panel(self, -1)
        self.SetBackgroundColour('white')
        self.CreateSearchPanel()
        # self.CreateAddPanel()
        # ------
        # 工具栏
        # ------

        toolbar = self.CreateToolBar()

        # ----------
        # 查找人员信息
        # ----------

        SearchTool = toolbar.AddTool(1, 'Search', wx.Bitmap(os.path.join(
            os.path.dirname(__file__), 'img/search.png')), shortHelp="查找人员信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, SearchTool)

        # ----------
        # 体温信息
        # ----------

        TemperatureTool = toolbar.AddTool(
            2, 'Temperature', wx.Bitmap(os.path.join(os.path.dirname(
                __file__), 'img/temperature.png')), shortHelp="体温信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, TemperatureTool)

        # ----------
        # 脉搏信息
        # ----------

        PulseTool = toolbar.AddTool(3, 'Pulse', wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'img/pulse.png')), shortHelp="脉搏信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, PulseTool)

        # ----------
        # 心电信息
        # ----------

        HeartTool = toolbar.AddTool(4, 'Heart', wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'img/heart.png')), shortHelp="心电信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, HeartTool)

        # -------
        # 退出工具
        # -------

        QuitTool = toolbar.AddTool(
            wx.ID_ANY, 'Quit', wx.Bitmap(os.path.join(
                os.path.dirname(__file__), 'img/quit.png')), shortHelp="退出系统")

        self.Bind(wx.EVT_TOOL, self.OnQuit, QuitTool)

        # ------
        # 初始化
        # -------
        toolbar.Realize()

    def OnSelectTool(self, e):
        # self.SetSize((800, 500))
        self.HidePanel(e.GetId())

    # 如果行为是切换其他panel，隐藏当前panel
    def HidePanel(self, num):
        # 转一下整型
        n = int(num)
        if n != self.current:
            self.current = n
            # print('我换到了', n)
            if n == 1:
                self.CreateSearchPanel()
            elif n == 2:
                self.CreateTemperaturePanel()
            elif n == 3:
                self.CreatePulsePanel()
            elif n == 4:
                self.CreateHeartPanel()

    # 创建 搜索 页面
    def CreateSearchPanel(self):
        self.panel.Destroy()
        self.panel = panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        nm = wx.StaticBox(panel, -1, '用户查找条件')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        nmbox = wx.BoxSizer(wx.HORIZONTAL)

        fn = wx.StaticText(panel, -1, "按病历编号查找：")
        nmbox.Add(fn, 0, wx.ALL | wx.CENTER, 5)

        nm1 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm1, 0, wx.ALL | wx.CENTER, 5)

        ln = wx.StaticText(panel, -1, "按姓名查找：")
        nmbox.Add(ln, 0, wx.ALL | wx.CENTER, 5)

        nm2 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm2, 0, wx.ALL | wx.CENTER, 5)

        ln1 = wx.StaticText(panel, -1, "按联系方式查找：")
        nmbox.Add(ln1, 0, wx.ALL | wx.CENTER, 5)

        nm3 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm3, 0, wx.ALL | wx.CENTER, 5)

        LoginBtn = wx.Button(panel, label="查找")
        # LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        nmbox.Add(LoginBtn, 0, wx.ALL | wx.CENTER, 5)

        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 5)

        # ------------------------------------------
        sizer = wx.GridBagSizer(10, 30)

        MedicalHistoryLabel = wx.StaticText(panel, label="病历编号:")
        sizer.Add(MedicalHistoryLabel, pos=(0, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(0, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="用户名:")
        sizer.Add(UserNameLabel, pos=(0, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(0, 5),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第二行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="性别:")
        sizer.Add(MedicalHistoryLabel, pos=(1, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(1, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="年龄:")
        sizer.Add(UserNameLabel, pos=(1, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(1, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第三行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="职业:")
        sizer.Add(MedicalHistoryLabel, pos=(2, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(2, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="联系方式:")
        sizer.Add(UserNameLabel, pos=(2, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(2, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第四行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="过敏史:")
        sizer.Add(MedicalHistoryLabel, pos=(3, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(3, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="家族病史:")
        sizer.Add(UserNameLabel, pos=(3, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(3, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第五行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="个人病史:")
        sizer.Add(MedicalHistoryLabel, pos=(4, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(4, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="体检记录:")
        sizer.Add(UserNameLabel, pos=(4, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(4, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第6行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="家庭住址:")
        sizer.Add(MedicalHistoryLabel, pos=(5, 0), flag=wx.ALL, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(5, 1),
                  span=(1, 7), flag=wx.ALL | wx.EXPAND, border=5)

        # --------------------------------------------
        vbox.Add(nmSizer, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(sizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizerAndFit(vbox)
        # self.Centre()
        self.Show()
        self.SetTitle("患者 - 搜索个人信息")

    # 创建 体温 页面

    def CreateTemperaturePanel(self):
        self.panel.Destroy()

        self.panel = panel = wx.Panel(self, -1)

        YearChoices = [u"2018年", u"2019年"]
        YearChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 150), choices=YearChoices)
        YearChoiceBox.SetSelection(0)

        MonthChoices = [u"1月", u"2月", u"3月", u"4月", u"5月", u"6月",
         u"7月", u"8月",u"9月",u"10月",u"11月",u"12月"]
        MonthChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 200), choices=MonthChoices)
        MonthChoiceBox.SetSelection(0)

        DayChoices = [
            u"1日", u"2日", u"3日", u"4日",u"5日", 
            u"6日", u"7日", u"8日", u"9日", u"10日", 
            u"11日", u"12日",u"13日", u"14日", u"15日",
            u"16日", u"17日", u"18日", u"19日",u"20日", 
            u"21日", u"22日", u"23日", u"24日", u"25日", 
            u"26日", u"27日", u"28日", u"29日", u"30日", u"31日"]
        DayChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 250), choices=DayChoices)
        DayChoiceBox.SetSelection(0)

        NumberLabel = wx.StaticText(
            panel,  wx.ID_ANY, pos=(682, 80), label="病历号:")

        self.NumberTextCtrl = NumberTextCtrl = wx.TextCtrl(
            panel, wx.ID_ANY, pos=(682, 100),)

        SubmitBtn = wx.Button(panel, label="确定", pos=(682, 300))
        SubmitBtn.Bind(
            wx.EVT_BUTTON, lambda event: self.CallRenderGraph(
                event, [30, 36.5, 37.5, 38, 37, 37.5, 37, 37.5, 37.5, 37.5]))
        # 临时数据，点击重新渲染=
        self.ChangeData([36, 36.5, 37.5, 38, 37, 37.5, 37, 37.5, 37.5, 37.5])

        self.SetTitle("患者 - 查看患者体温信息")

    def CallRenderGraph(self, e, data):
        self.ChangeData(data)

    def ChangeData(self, data):
        # !请求数据
        scores = data
        sum = 0
        for s in scores:
            sum += s
        average = sum / len(scores)

        t_score = numpy.arange(1, len(scores) + 1, 1)
        s_score = numpy.array(scores)

        self.figure_score = Figure()
        self.figure_score.set_figheight(3.8)
        self.figure_score.set_figwidth(6.8)
        self.axes_score = self.figure_score.add_subplot(111)

        self.axes_score.plot(t_score, s_score, 'ro', t_score, s_score, 'k')
        self.axes_score.axhline(y=average, color='r')
        self.axes_score.set_title(u'Temperature')
        self.axes_score.grid(True)
        self.axes_score.set_xlabel('t')
        self.axes_score.set_ylabel('temperature')
        FigureCanvas(self.panel, -1, self.figure_score)
        self.panel.Fit()

    # 创建 脉搏 页面
    def CreatePulsePanel(self):

        self.panel.Destroy()
        self.panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer(0, 30)

        UserNameLabel = wx.StaticText(self.panel, label="Pulse")
        sizer.Add(UserNameLabel, pos=(0, 0), flag=wx.ALL, border=5)

        self.panel.SetSizerAndFit(sizer)
        self.SetTitle('患者 — 查看患者脉搏信息')

    # 创建 心电 页面
    def CreateHeartPanel(self):

        self.panel.Destroy()
        self.panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer(0, 30)

        UserNameLabel = wx.StaticText(self.panel, label="Heart")
        sizer.Add(UserNameLabel, pos=(0, 0), flag=wx.ALL, border=5)

        self.panel.SetSizerAndFit(sizer)
        self.SetTitle('患者 — 查看患者心电信息')

    # 退出程序
    def OnQuit(self, e):
        wx.MessageBox("已退出登录！")
        self.Close()


def main():
    app = wx.App()
    PatientFrame(None, title='患者 - 搜索个人信息', user='')
    app.MainLoop()


if __name__ == '__main__':
    main()
