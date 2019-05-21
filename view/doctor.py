# -*- coding: utf-8 -*-
"""
desc: 医生页面
last modified: 2019.5.19
"""

import wx
import wx.grid as table
import wx.lib.scrolledpanel as scrolled
import numpy
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

toolist = ['search', 'all', 'add', 'delete',
           'temperature', 'pulse', 'heart', 'alarm']


players = [('Tendulkar', '15000', '100'), ('Dravid', '14000', '1'),
           ('Kumble', '1000', '700'), ('KapilDev', '5000', '400'),
           ('Ganguly', '8000', '50')]


# 个人信息，患者信息（保存状态）
userdata = {}


class DoctorFrame(wx.Frame):

    def __init__(self, parent, title):
        super(DoctorFrame, self).__init__(
            parent, title=title, size=(800, 400))

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

        SearchTool = toolbar.AddTool(1, 'Search', wx.Bitmap(
            'img/search.png'), shortHelp="查找人员信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, SearchTool)

        # --------------
        # 所有人员信息 列表
        # --------------

        AllTool = toolbar.AddTool(2, 'All People', wx.Bitmap(
            'img/all.png'), shortHelp="所有人员信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, AllTool)

        # ----------
        # 添加人员信息
        # ----------

        AddTool = toolbar.AddTool(3, 'Add', wx.Bitmap(
            'img/add.png'), shortHelp="添加人员信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, AddTool)

        # ----------
        # 删除人员信息
        # ----------

        # DeleteTool = toolbar.AddTool(4, 'Delete', wx.Bitmap('img/delete.png'))

        # self.Bind(wx.EVT_TOOL, self.OnSelectTool, DeleteTool)

        # ----------
        # 体温信息
        # ----------

        TemperatureTool = toolbar.AddTool(
            5, 'Temperature', wx.Bitmap('img/temperature.png'), shortHelp="体温信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, TemperatureTool)

        # ----------
        # 脉搏信息
        # ----------

        PulseTool = toolbar.AddTool(6, 'Pulse', wx.Bitmap(
            'img/pulse.png'), shortHelp="脉搏信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, PulseTool)

        # ----------
        # 心电信息
        # ----------

        HeartTool = toolbar.AddTool(7, 'Heart', wx.Bitmap(
            'img/heart.png'), shortHelp="心电信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, HeartTool)

        # ----------
        # 报警信息
        # ----------

        # AlarmTool = toolbar.AddTool(8, 'Alarm', wx.Bitmap(
        #     'img/alarm.png'), shortHelp="修改报警信息")

        # self.Bind(wx.EVT_TOOL, self.OnSelectTool, AlarmTool)

        # -------
        # 退出工具
        # -------

        QuitTool = toolbar.AddTool(
            wx.ID_ANY, 'Quit', wx.Bitmap('img/quit.png'), shortHelp="退出系统")

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
                self.CreateAllPanel()
            elif n == 3:
                self.CreateAddPanel()
            elif n == 4:
                self.CreateDeletePanel()
            elif n == 5:
                self.CreateTemperaturePanel()
            elif n == 6:
                self.CreatePulsePanel()
            elif n == 7:
                self.CreateHeartPanel()
            elif n == 8:
                self.CreateAlarmPanel()

    # 创建 搜索 页面
    def CreateSearchPanel(self):
        # 只有一个panel，动态删除添加（效率较低
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
        LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
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
        self.SetTitle("医生 - 搜索个人信息")

    # !创建 所有人员列表 页面
    def CreateAllPanel(self):

        self.panel.Destroy()
        self.panel = panel = scrolled.ScrolledPanel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        grid = table.Grid(panel, -1)

        grid.CreateGrid(15, 8)

        # grid.SetRowSize(0, 00)
        grid.SetColSize(0, 100)
        grid.SetColSize(5, 100)
        grid.SetColSize(6, 100)
        grid.SetColSize(7, 100)

        grid.SetColLabelValue(0, '病历编号')
        grid.SetColLabelValue(1, '姓名')
        grid.SetColLabelValue(2, '性别')
        grid.SetColLabelValue(3, '年龄')
        grid.SetColLabelValue(4, '职业')
        grid.SetColLabelValue(5, '联系方式')
        grid.SetColLabelValue(6, '过敏史')
        grid.SetColLabelValue(7, '家族病史')


        # 病患数据填充数组（抽离？
        data = [['0908721','老毕','男','45','混子','17864534243','无','神经病']]
        for i in range(1):
            for j in range(8):
                grid.SetCellValue(i, j, data[i][j])

        # grid.ShowScrollbars(wx.SHOW_SB, wx.SHOW_SB_DEFAULT)


        nm = wx.StaticBox(panel, -1, '')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        nmbox = wx.BoxSizer(wx.HORIZONTAL)


        upBtn = wx.Button(panel, -1, label="上一页")
        # LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        nmbox.Add(upBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)

        downBtn = wx.Button(panel, -1, label="下一页")
        # LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        nmbox.Add(downBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)

        submitBtn = wx.Button(panel, -1, label="提交修改")
        # LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        nmbox.Add(submitBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)

        deleteBtn = wx.Button(panel, -1, label="删除对象")
        # LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        nmbox.Add(deleteBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)


        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 5)


        vbox.Add(grid, 0, wx.ALL |wx.CENTER)
        vbox.Add(nmSizer, 0, wx.ALL | wx.EXPAND | wx.CENTER)

        # vbox.Add(sizer, 0, wx.ALL | wx.CENTER, 5)
        # vbox.Add(nmSizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizerAndFit(vbox)
        self.Show()
        self.SetTitle("医生 - 查看所有患者信息")
        # self.panel.Fit()


    # 创建 添加人员 页面
    def CreateAddPanel(self):

       # 只有一个panel，动态删除添加（效率较低
        self.panel.Destroy()
        self.panel = panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        nm = wx.StaticBox(panel, -1, '')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        nmbox = wx.BoxSizer(wx.HORIZONTAL)


        LoginBtn = wx.Button(panel, label="添加")
        LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        nmbox.Add(LoginBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)


        ClearBtn = wx.Button(panel, label="清空")
        ClearBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        nmbox.Add(ClearBtn, 0, wx.ALL | wx.CENTER, 5)

        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 5)

        # ------------------------------------------
        sizer = wx.GridBagSizer(10, 30)

        MedicalHistoryLabel = wx.StaticText(panel, label="病历编号:")
        sizer.Add(MedicalHistoryLabel, pos=(1, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(1, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="用户名:")
        sizer.Add(UserNameLabel, pos=(2, 0), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(2, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第二行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="性别:")
        sizer.Add(MedicalHistoryLabel, pos=(2, 4),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(2, 5),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

   

        # ---------------------------第三行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="联系方式:")
        sizer.Add(MedicalHistoryLabel, pos=(2, 8),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(2, 9),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="职业:")
        sizer.Add(UserNameLabel, pos=(3, 0), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(3, 1), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第四行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="家族病史:")
        sizer.Add(MedicalHistoryLabel, pos=(5, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(5, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="过敏史:")
        sizer.Add(UserNameLabel, pos=(5, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(5, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        MedicalHistoryLabel = wx.StaticText(panel, label="个人病史:")
        sizer.Add(MedicalHistoryLabel, pos=(5, 8),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(5, 9),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        # UserNameLabel = wx.StaticText(panel, label="体检记录:")
        # sizer.Add(UserNameLabel, pos=(4, 4), flag=wx.ALL | wx.EXPAND, border=5)

        # self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        # sizer.Add(UserNameTextCtrl, pos=(4, 5), span=(1, 3),
        #           flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第6行-------------------------------
        MedicalHistoryLabel = wx.StaticText(panel, label="家庭住址:")
        sizer.Add(MedicalHistoryLabel, pos=(7, 0), flag=wx.ALL, border=5)

        self.MedicalHistoryTextCtrl = MedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalHistoryTextCtrl, pos=(7, 1),
                  span=(1, 7), flag=wx.ALL | wx.EXPAND, border=5)

        # --------------------------------------------
        
        vbox.Add(sizer, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(nmSizer, 0, wx.ALL | wx.EXPAND | wx.CENTER)
        panel.SetSizerAndFit(vbox)
        # self.Centre()
        self.Show()
        self.SetTitle("医生 - 添加个人信息")


    # 创建 体温 页面
    def CreateTemperaturePanel(self):
        self.panel.Destroy()

        self.panel =panel= wx.Panel(self, -1)

        YearChoices = [u"2018年", u"2019年"]
        YearChoiceBox = wx.Choice(panel, wx.ID_ANY, pos=(682, 150), choices=YearChoices)
        YearChoiceBox.SetSelection(0)

        MonthChoices = [u"4月", u"5月"]
        MonthChoiceBox = wx.Choice(panel, wx.ID_ANY, pos=(682, 200), choices=MonthChoices)
        MonthChoiceBox.SetSelection(0)

        DayChoices = [u"18日", u"19日", u"20日"]
        DayChoiceBox = wx.Choice(panel, wx.ID_ANY, pos=(682, 250), choices=DayChoices)
        DayChoiceBox.SetSelection(0)

        NumberLabel = wx.StaticText(panel,  wx.ID_ANY, pos=(682, 80), label="病历号:")
       
        self.NumberTextCtrl = NumberTextCtrl = wx.TextCtrl(
            panel, wx.ID_ANY, pos=(682, 100),)

        SubmitBtn = wx.Button(panel, label="确定",pos=(682,300))

        # 临时数据，点击重新渲染
        scores = [36, 36.5, 37.5, 38, 37, 37.5, 37, 37.5, 37.5, 37.5]
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
        self.axes_score.set_xlabel('time')
        self.axes_score.set_ylabel('temperature')
        FigureCanvas(self.panel, -1, self.figure_score)
        self.panel.Fit()
        self.SetTitle("医生 - 查看患者体温信息")

        # RegisterBtn.Bind(wx.EVT_BUTTON, self.OnRegister)


    # 创建 脉搏 页面
    def CreatePulsePanel(self):
        # print('alarm')
        # 只有一个panel，动态删除添加（效率较低
        self.panel.Destroy()
        self.panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer(0, 30)

        UserNameLabel = wx.StaticText(self.panel, label="Pulse")
        sizer.Add(UserNameLabel, pos=(0, 0), flag=wx.ALL, border=5)

        self.panel.SetSizerAndFit(sizer)
        self.SetTitle('医生 — 查看患者脉搏信息')

    # 创建 心电 页面
    def CreateHeartPanel(self):
        # print('alarm')
        # 只有一个panel，动态删除添加（效率较低
        self.panel.Destroy()
        self.panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer(0, 30)

        UserNameLabel = wx.StaticText(self.panel, label="Heart")
        sizer.Add(UserNameLabel, pos=(0, 0), flag=wx.ALL, border=5)

        self.panel.SetSizerAndFit(sizer)
        self.SetTitle('医生 — 查看患者心电信息')

    # 创建 警报 页面
    def CreateAlarmPanel(self):
        # print('alarm')
        # 只有一个panel，动态删除添加（效率较低
        self.panel.Destroy()
        self.panel = panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        wx.BoxSizer(wx.HORIZONTAL)

        sizer = wx.GridBagSizer(0, 30)

        SendLabel = wx.StaticText(panel, label="发送信息：")
        SendTextCtrl = wx.TextCtrl(panel, size=(300, 70), style=wx.TE_MULTILINE)

        RecvLabel = wx.StaticText(self.panel, label="回馈信息：")
        RecvTextCtrl = wx.TextCtrl(
            panel, size=(300, 70), style=wx.TE_MULTILINE)

        NoteLabel = wx.StaticText(self.panel, label="备注信息：")
        NoteTextCtrl = wx.TextCtrl(panel, size=(300, 70), style=wx.TE_MULTILINE)
        
        SaveBtn = wx.Button(panel, label="保存")
        # SaveBtn.Bind(wx.EVT_BUTTON, self.OnRegister)


        sizer.Add(SendLabel, pos=(1, 4), flag=wx.ALL | wx.CENTER, border=5)
        sizer.Add(SendTextCtrl, pos=(1, 5),flag=wx.ALL | wx.CENTER, border=5)

        sizer.Add(RecvLabel, pos=(2, 4), flag=wx.ALL, border=5)
        sizer.Add(RecvTextCtrl, pos=(2, 5), flag=wx.ALL | wx.CENTER, border=5)

        sizer.Add(NoteLabel, pos=(3, 4), flag=wx.ALL, border=5)
        sizer.Add(NoteTextCtrl, pos=(3, 5), flag=wx.ALL | wx.CENTER, border=5)

        sizer.Add(SaveBtn, pos=(4, 6), flag=wx.EXPAND | wx.LEFT, border=5)

        panel.SetSizerAndFit(sizer)
        self.SetTitle('医生 — 警报信息更改')
        self.Show()

    def OnLogin(self):
        pass

    # 退出程序
    def OnQuit(self, e):
        wx.MessageBox("已退出登录！")
        self.Close()


def main():
    app = wx.App()
    DoctorFrame(None, title='医生 - 搜索个人信息')
    app.MainLoop()


if __name__ == '__main__':
    main()
