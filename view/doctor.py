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
import os
import re
import json
import pika
from parse import hl72json

# 保存全局状态
userdata = {}


class DoctorFrame(wx.Frame):

    def __init__(self, parent, title, user):
        super(DoctorFrame, self).__init__(
            parent, title=title, size=(800, 400))
        global userdata
        userdata = user
        userdata['temperature'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        userdata['pulse'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        userdata['heart'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        userdata['year'] = 0
        userdata['month'] = 0
        userdata['day'] = 0

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

        SearchTool = toolbar.AddTool(1, 'Search', wx.Bitmap(os.path.join(os.path.dirname(__file__), 'img/search.png')), shortHelp="查找人员信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, SearchTool)

        # --------------
        # 所有人员信息 列表
        # --------------

        AllTool = toolbar.AddTool(2, 'All People', wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'img/all.png')), shortHelp="所有人员信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, AllTool)

        # ----------
        # 添加人员信息
        # ----------

        AddTool = toolbar.AddTool(3, 'Add', wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'img/add.png')), shortHelp="添加人员信息")

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
            5, 'Temperature', wx.Bitmap(os.path.join(os.path.dirname(
                __file__), 'img/temperature.png')), shortHelp="体温信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, TemperatureTool)

        # ----------
        # 脉搏信息
        # ----------

        PulseTool = toolbar.AddTool(6, 'Pulse', wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'img/pulse.png')), shortHelp="脉搏信息")

        self.Bind(wx.EVT_TOOL, self.OnSelectTool, PulseTool)

        # ----------
        # 心电信息
        # ----------

        HeartTool = toolbar.AddTool(7, 'Heart', wx.Bitmap(
            os.path.join(os.path.dirname(__file__), 'img/heart.png')), shortHelp="心电信息")

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

        self.number = nm1 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm1, 0, wx.ALL | wx.CENTER, 5)

        ln = wx.StaticText(panel, -1, "按姓名查找：")
        nmbox.Add(ln, 0, wx.ALL | wx.CENTER, 5)

        self.name = nm2 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm2, 0, wx.ALL | wx.CENTER, 5)

        ln1 = wx.StaticText(panel, -1, "按联系方式查找：")
        nmbox.Add(ln1, 0, wx.ALL | wx.CENTER, 5)

        self.phone = nm3 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm3, 0, wx.ALL | wx.CENTER, 5)

        FindBtn = wx.Button(panel, label="查找")
        FindBtn.Bind(wx.EVT_BUTTON, self.OnFind)
        nmbox.Add(FindBtn, 0, wx.ALL | wx.CENTER, 5)

        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 5)

        # ------------------------------------------
        sizer = wx.GridBagSizer(10, 30)

        MedicalNumberLabel = wx.StaticText(panel, label="病历编号:")
        sizer.Add(MedicalNumberLabel, pos=(0, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalNumberTextCtrl = MedicalNumberTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(MedicalNumberTextCtrl, pos=(0, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="用户名:")
        sizer.Add(UserNameLabel, pos=(0, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(0, 5),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第二行-------------------------------
        GenderLabel = wx.StaticText(panel, label="性别:")
        sizer.Add(GenderLabel, pos=(1, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.GenderTextCtrl = GenderTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(GenderTextCtrl, pos=(1, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        YearOldLabel = wx.StaticText(panel, label="年龄:")
        sizer.Add(YearOldLabel, pos=(1, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.YearOldTextCtrl = YearOldTextCtrl = wx.TextCtrl(panel)
        sizer.Add(YearOldTextCtrl, pos=(1, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第三行-------------------------------
        JobLabel = wx.StaticText(panel, label="职业:")
        sizer.Add(JobLabel, pos=(2, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.JobTextCtrl = JobTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(JobTextCtrl, pos=(2, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        PhoneLabel = wx.StaticText(panel, label="联系方式:")
        sizer.Add(PhoneLabel, pos=(2, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.PhoneTextCtrl = PhoneTextCtrl = wx.TextCtrl(panel)
        sizer.Add(PhoneTextCtrl, pos=(2, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第四行-------------------------------
        AllergyLabel = wx.StaticText(panel, label="过敏史:")
        sizer.Add(AllergyLabel, pos=(3, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.AllergyTextCtrl = AllergyTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(AllergyTextCtrl, pos=(3, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        FamilyMedicalHistoryLabel = wx.StaticText(panel, label="家族病史:")
        sizer.Add(FamilyMedicalHistoryLabel, pos=(
            3, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.FamilyMedicalHistoryTextCtrl = FamilyMedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(FamilyMedicalHistoryTextCtrl, pos=(3, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第五行-------------------------------
        PersonalMedicalHistoryLabel = wx.StaticText(panel, label="个人病史:")
        sizer.Add(PersonalMedicalHistoryLabel, pos=(4, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.PersonalMedicalHistoryTextCtrl = PersonalMedicalHistoryTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(PersonalMedicalHistoryTextCtrl, pos=(4, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        CheckRecordLabel = wx.StaticText(panel, label="体检记录:")
        sizer.Add(CheckRecordLabel, pos=(4, 4),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.CheckRecordTextCtrl = CheckRecordTextCtrl = wx.TextCtrl(panel)
        sizer.Add(CheckRecordTextCtrl, pos=(4, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第6行-------------------------------
        HomeLabel = wx.StaticText(panel, label="家庭住址:")
        sizer.Add(HomeLabel, pos=(5, 0), flag=wx.ALL, border=5)

        self.HomeTextCtrl = HomeTextCtrl = wx.TextCtrl(
            panel)
        sizer.Add(HomeTextCtrl, pos=(5, 1),
                  span=(1, 7), flag=wx.ALL | wx.EXPAND, border=5)
        # --------------------------------------------
        vbox.Add(nmSizer, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(sizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizerAndFit(vbox)
        # self.Centre()
        self.Show()
        self.SetTitle("医生 - 搜索个人信息")

    def trim(self, origin):
        return origin[0][0].replace(' ', '').replace('\"', '').replace(',', '').replace(':', '').replace('}', '').replace('CDA.3', '').replace('ZCS.4', '')

    def toHL7file(self, patient):
        with open('patient.txt', 'w', encoding='utf-8') as f:
            f.write(patient)

    def OnFind(self,e):
        global res
        res = '-1'
        cs = ClientSend('getdata', 'unumber=' + self.number.GetValue())
        del cs
        cv = ClientRecv()
        del cv
        if res != '-1':
            filejson = hl72json.hl72json(self,'patient.txt')
            after = filejson.replace('\n','')
            # 姓名
            names = re.findall(".*PID.2.6\"(.*)\"(PID.2.8).*", after)
            name = self.trim(names)
            # self.nm2.SetValue(name)
            self.UserNameTextCtrl.SetValue(name)
            # 编号
            unumbers = re.findall(".*PID.2.4\"(.*)\"(PID.2.6).*", after)
            unumber = self.trim(unumbers)
            # self.nm1.SetValue(unumber)
            self.MedicalNumberTextCtrl.SetValue(unumber)
            # 联系方式
            phones = re.findall(".*PID.2.14\"(.*)\"(PID.2.15).*", after)
            phone = self.trim(phones)
            # self.nm3.SetValue(phone)
            self.PhoneTextCtrl.SetValue(phone)
            # 地址
            homes = re.findall(".*PID.2.12\"(.*)\"(PID.2.14).*", after)
            home = self.trim(homes)
            self.HomeTextCtrl.SetValue(home)
            # 性别
            genders = re.findall(".*PID.2.9\"(.*)\"(PID.2.12).*", after)
            gender = self.trim(genders)
            if gender == 'F':
                self.GenderTextCtrl.SetValue('男')
            else:
                self.GenderTextCtrl.SetValue('女')
            # 年龄
            yos = re.findall(".*PID.2.8\"(.*)\"(PID.2.9).*", after)
            yo = self.trim(yos)
            self.YearOldTextCtrl.SetValue(yo)
            # 工作
            jobs = re.findall(".*PID.2.15\"(.+?)\"(CDA.3).*", after)
            job = self.trim(jobs)
            self.JobTextCtrl.SetValue(job)
            # 家族病史
            familys = re.findall(".*CDA.3.6\"(.*)\"(CDA.3.7).*", after)
            family = self.trim(familys)
            self.FamilyMedicalHistoryTextCtrl.SetValue(family)
            # 过敏史
            allergys = re.findall(".*CDA.3.4\"(.*)\"(CDA.3.6).*", after)
            allergy = self.trim(allergys)
            self.AllergyTextCtrl.SetValue(allergy)
            # 个人病史
            personals = re.findall(".*CDA.3.7\"(.*)\"(CDA.3.9).*", after)
            personal = self.trim(personals)
            self.PersonalMedicalHistoryTextCtrl.SetValue(personal)
            # 体检记录
            checks = re.findall(".*CDA.3.9\"(.+?)\"(ZCS.4).*", after)
            check = self.trim(checks)
            self.CheckRecordTextCtrl.SetValue(check)
        else:
            wx.MessageBox('查无此人！')
            # name
            self.UserNameTextCtrl.SetValue('')
            # 编号
            self.MedicalNumberTextCtrl.SetValue('')
            # 联系方式
            self.PhoneTextCtrl.SetValue('')
            # 地址
            self.HomeTextCtrl.SetValue('')
            # 性别
            self.GenderTextCtrl.SetValue('')
            # 年龄
            self.YearOldTextCtrl.SetValue('')
            # 工作
            self.JobTextCtrl.SetValue('')
            # 家族病史
            self.FamilyMedicalHistoryTextCtrl.SetValue('')
            # 过敏史
            self.AllergyTextCtrl.SetValue('')
            # 个人病史
            self.PersonalMedicalHistoryTextCtrl.SetValue('')
            # 体检记录
            self.CheckRecordTextCtrl.SetValue('')


    # !创建 所有人员列表 页面
    def CreateAllPanel(self):

        self.panel.Destroy()
        self.panel = panel = scrolled.ScrolledPanel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.grid = grid = table.Grid(panel, -1)

        grid.CreateGrid(15, 12)

        for i in range(15):
            grid.SetReadOnly(i, 0, True)
            grid.SetReadOnly(i, 1, True)

        # grid.SetRowSize(0, 00)
        grid.SetColSize(0, 100)
        grid.SetColSize(5, 100)
        grid.SetColSize(6, 100)
        grid.SetColSize(7, 100)

        grid.SetColLabelValue(0, '病历编号')
        grid.SetColLabelValue(1, '主治医师编号')
        grid.SetColLabelValue(2, '姓名')
        grid.SetColLabelValue(3, '性别')
        grid.SetColLabelValue(4, '年龄')
        grid.SetColLabelValue(5, '联系方式')
        grid.SetColLabelValue(6, '家庭住址')
        grid.SetColLabelValue(7, '职业')
        grid.SetColLabelValue(8, '过敏史')
        grid.SetColLabelValue(9, '家族病史')
        grid.SetColLabelValue(10, '个人病史')
        grid.SetColLabelValue(11, '体检记录')
        # grid.ShowScrollbars(wx.SHOW_SB, wx.SHOW_SB_DEFAULT)

        global res
        global userdata
        res = '-1'
        cs = ClientSend('all', 'unumber=' + userdata['unumber'])
        del cs
        cv = ClientRecv()
        del cv
        if res != '-1':
            data = []
            origin = res.strip('[(').strip(')]').replace(')','').replace('(','').replace("'","").replace(" ","").split(',')
 
            # data = [['0908721','老毕','男','45','混子','17864534243','无','神经病']]
            # print(origin,data)

            origindata = numpy.array(origin)  # x是一维数组
            data = origindata.reshape((int(len(origin)/12), 12))
  
            for i in range(int(len(origin)/12)):
                for j in range(12):
                    self.grid.SetCellValue(i, j, data[i][j])


        nm = wx.StaticBox(panel, -1, '')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        nmbox = wx.BoxSizer(wx.HORIZONTAL)


        # upBtn = wx.Button(panel, -1, label="上一页")
        # LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        # nmbox.Add(upBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)

        # downBtn = wx.Button(panel, -1, label="下一页")
        # LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
        # nmbox.Add(downBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)

        ChangeBtn = wx.Button(panel, -1, label="提交修改")
        ChangeBtn.Bind(wx.EVT_BUTTON, self.OnChange)
        nmbox.Add(ChangeBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)

        DeleteBtn = wx.Button(panel, -1, label="删除对象")
        DeleteBtn.Bind(wx.EVT_BUTTON, self.OnDelete)
        nmbox.Add(DeleteBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)


        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 5)

        grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnSelectRow)
        
        vbox.Add(grid, 0, wx.ALL |wx.CENTER)
        vbox.Add(nmSizer, 0, wx.ALL | wx.EXPAND | wx.CENTER)

        # vbox.Add(sizer, 0, wx.ALL | wx.CENTER, 5)
        # vbox.Add(nmSizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizerAndFit(vbox)
        self.Show()
        self.SetTitle("医生 - 查看所有患者信息")
        # self.panel.Fit()

    def OnSelectRow(self,e):
        global row
        self.grid.SelectRow(e.GetRow())
        row = e.GetRow()

    # 删除
    def OnDelete(self,e):
        global row
        global res

        res = '-1'
        cs = ClientSend('delete', 'unumber=' + self.grid.GetCellValue(row, 0) )
        del cs
        cv = ClientRecv()
        del cv
        if res != '-1':
            wx.MessageBox('删除成功！')
        else:
            wx.MessageBox('删除失败！')

    # !the last 修改
    def OnChange(self,e):
        global row
        global res
        res = '-1'
        cs = ClientSend('update', 'unumber=' + self.grid.GetCellValue(row,0) + '&name=' + self.grid.GetCellValue(row, 2) + '&gender=' + self.grid.GetCellValue(row, 3) +'&yearold=' + self.grid.GetCellValue(row, 4) +'&job=' + self.grid.GetCellValue(row, 7) +'&phone=' + self.grid.GetCellValue(row, 5) +'&allergy=' + self.grid.GetCellValue(row, 8) +'&family=' + self.grid.GetCellValue(row, 9))
        del cs
        cv = ClientRecv()
        del cv
        if res != '-1':
            wx.MessageBox('修改成功！')
        else:
            wx.MessageBox('修改失败！')

    # 创建 添加人员 页面
    def CreateAddPanel(self):

        # 只有一个panel，动态删除添加（效率较低
        self.panel.Destroy()
        self.panel = panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        nm = wx.StaticBox(panel, -1, '')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        nmbox = wx.BoxSizer(wx.HORIZONTAL)


        AddBtn = wx.Button(panel, label="添加")
        AddBtn.Bind(wx.EVT_BUTTON, self.OnAdd)
        nmbox.Add(AddBtn, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)


        ClearBtn = wx.Button(panel, label="清空")
        ClearBtn.Bind(wx.EVT_BUTTON, self.OnClear)
        nmbox.Add(ClearBtn, 0, wx.ALL | wx.CENTER, 5)

        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 5)

        # ------------------------------------------
        sizer = wx.GridBagSizer(10, 30)

        MedicalNumberLabel = wx.StaticText(panel, label="病历编号:")
        sizer.Add(MedicalNumberLabel, pos=(1, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.MedicalNumberTextCtrl1 = MedicalNumberTextCtrl1 = wx.TextCtrl(
            panel)
        sizer.Add(MedicalNumberTextCtrl1, pos=(1, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        UserNameLabel = wx.StaticText(panel, label="用户名:")
        sizer.Add(UserNameLabel, pos=(2, 0), flag=wx.ALL | wx.EXPAND, border=5)

        self.UserNameTextCtrl1 = UserNameTextCtrl1 = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl1, pos=(2, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第二行-------------------------------
        GenderLabel = wx.StaticText(panel, label="性别:")
        sizer.Add(GenderLabel, pos=(2, 4),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.GenderTextCtrl1 = GenderTextCtrl1 = wx.TextCtrl(
            panel)
        sizer.Add(GenderTextCtrl1, pos=(2, 5),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第三行-------------------------------
        PhoneLabel = wx.StaticText(panel, label="联系方式:")
        sizer.Add(PhoneLabel, pos=(2, 8),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.PhoneTextCtrl1 = PhoneTextCtrl1 = wx.TextCtrl(
            panel)
        sizer.Add(PhoneTextCtrl1, pos=(2, 9),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        JobLabel = wx.StaticText(panel, label="职业:")
        sizer.Add(JobLabel, pos=(3, 0), flag=wx.ALL | wx.EXPAND, border=5)

        self.JobTextCtrl1 = JobTextCtrl1 = wx.TextCtrl(panel)
        sizer.Add(JobTextCtrl1, pos=(3, 1), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        YearOldLabel = wx.StaticText(panel, label="年龄:")
        sizer.Add(YearOldLabel, pos=(3, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.YearOldTextCtrl1 = YearOldTextCtrl1 = wx.TextCtrl(panel)
        sizer.Add(YearOldTextCtrl1, pos=(3, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)
        # ---------------------------第四行-------------------------------
        FamilyMedicalHistoryLabel = wx.StaticText(panel, label="家族病史:")
        sizer.Add(FamilyMedicalHistoryLabel, pos=(5, 0),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.FamilyMedicalHistoryTextCtrl1 = FamilyMedicalHistoryTextCtrl1 = wx.TextCtrl(
            panel)
        sizer.Add(FamilyMedicalHistoryTextCtrl1, pos=(5, 1),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        AllergyLabel = wx.StaticText(panel, label="过敏史:")
        sizer.Add(AllergyLabel, pos=(5, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.AllergyTextCtrl1 = AllergyTextCtrl1 = wx.TextCtrl(panel)
        sizer.Add(AllergyTextCtrl1, pos=(5, 5), span=(1, 3),
                  flag=wx.ALL | wx.EXPAND, border=5)

        PersonalMedicalHistoryLabel = wx.StaticText(panel, label="个人病史:")
        sizer.Add(PersonalMedicalHistoryLabel, pos=(5, 8),
                  flag=wx.ALL | wx.EXPAND, border=5)

        self.PersonalMedicalHistoryTextCtrl1 = PersonalMedicalHistoryTextCtrl1 = wx.TextCtrl(
            panel)
        sizer.Add(PersonalMedicalHistoryTextCtrl1, pos=(5, 9),
                  span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        # ---------------------------第6行-------------------------------
        HomeLabel = wx.StaticText(panel, label="家庭住址:")
        sizer.Add(HomeLabel, pos=(7, 0), flag=wx.ALL, border=5)

        self.HomeTextCtrl1 = HomeTextCtrl1 = wx.TextCtrl(
            panel)
        sizer.Add(HomeTextCtrl1, pos=(7, 1),
                  span=(1, 7), flag=wx.ALL | wx.EXPAND, border=5)

        # --------------------------------------------

        vbox.Add(sizer, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(nmSizer, 0, wx.ALL | wx.EXPAND | wx.CENTER)
        panel.SetSizerAndFit(vbox)
        # self.Centre()
        self.Show()
        self.SetTitle("医生 - 添加个人信息")

    def OnAdd(self,e):
        global res
        global userdata
        name = self.UserNameTextCtrl1.GetValue()
        wx.MessageBox(name)
        # # 用户姓名
        # self.UserNameTextCtrl1.GetValue()
        # # 编号
        # self.MedicalNumberTextCtrl1.GetValue()
        # # 联系方式
        # self.PhoneTextCtrl1.GetValue()
        # # 地址
        # self.HomeTextCtrl1.GetValue()
        # # 性别
        # self.GenderTextCtrl1.GetValue()
        # # 年龄
        # self.YearOldTextCtrl1.GetValue()
        # # 工作
        # self.JobTextCtrl1.GetValue()
        # # 家族病史
        # self.FamilyMedicalHistoryTextCtrl1.GetValue()
        # # 过敏史
        # self.AllergyTextCtrl1.GetValue()
        # # 个人病史
        # self.PersonalMedicalHistoryTextCtrl.GetValue()
        res = '-1'
        cs = ClientSend('add', 'unumber=' + userdata['unumber'] + '&pname=' + self.UserNameTextCtrl1.GetValue() + '&pnumber=' + self.MedicalNumberTextCtrl1.GetValue() +'&gender=' + self.GenderTextCtrl1.GetValue() +'&yearold=' + self.YearOldTextCtrl1.GetValue() +'&home=' + self.HomeTextCtrl1.GetValue() +'&job=' + self.JobTextCtrl1.GetValue() +'&phone=' + self.PhoneTextCtrl1.GetValue() +'&allergy=' + self.AllergyTextCtrl1.GetValue() +'&family_medical_history=' + self.FamilyMedicalHistoryTextCtrl1.GetValue() +'&personal_medical_history=' + self.PersonalMedicalHistoryTextCtrl1.GetValue())
        del cs
        cv = ClientRecv()
        del cv
        if res != '-1':
            wx.MessageBox('增加成功！')

    def OnClear(self,e):
        self.UserNameTextCtrl1.SetValue('')
        # 编号
        self.MedicalNumberTextCtrl1.SetValue('')
        # 联系方式
        self.PhoneTextCtrl1.SetValue('')
        # 地址
        self.HomeTextCtrl1.SetValue('')
        # 性别
        self.GenderTextCtrl1.SetValue('')
        # 年龄
        # self.YearOldTextCtrl1.SetValue('')
        # 工作
        self.JobTextCtrl1.SetValue('')
        # 家族病史
        self.FamilyMedicalHistoryTextCtrl1.SetValue('')
        # 过敏史
        self.AllergyTextCtrl1.SetValue('')
        # 个人病史
        self.PersonalMedicalHistoryTextCtrl1.SetValue('')


    # 创建 体温 页面
    def CreateTemperaturePanel(self):
        global userdata
        self.panel.Destroy()

        self.panel = panel = wx.Panel(self, -1)

        self.YearChoices = YearChoices = [u"2019年", u"2018年"]
        self.YearChoiceBox = YearChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 150), choices=YearChoices)
        YearChoiceBox.SetSelection(userdata['year'])

        self.MonthChoices = MonthChoices = [u"01月", u"02月", u"03月", u"04月", u"05月", u"06月",
                                            u"07月", u"08月", u"09月", u"10月", u"11月", u"12月"]
        self.MonthChoiceBox = MonthChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 200), choices=MonthChoices)
        MonthChoiceBox.SetSelection(userdata['month'])

        self.DayChoices = DayChoices = [
            u"01日", u"02日", u"03日", u"04日", u"05日",
            u"06日", u"07日", u"08日", u"09日", u"10日",
            u"11日", u"12日", u"13日", u"14日", u"15日",
            u"16日", u"17日", u"18日", u"19日", u"20日",
            u"21日", u"22日", u"23日", u"24日", u"25日",
            u"26日", u"27日", u"28日", u"29日", u"30日", u"31日"]
        self.DayChoiceBox = DayChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 250), choices=DayChoices)
        DayChoiceBox.SetSelection(userdata['day'])

        NumberLabel = wx.StaticText(
            panel,  wx.ID_ANY, pos=(682, 80), label="病历号:")

        self.NumberTextCtrl = NumberTextCtrl = wx.TextCtrl(
            panel, wx.ID_ANY, pos=(682, 100),)

        SubmitBtn = wx.Button(panel, label="确定", pos=(682, 300))

        SubmitBtn.Bind(
            wx.EVT_BUTTON, lambda event: self.CallRenderGraph(
                event, 'temperature'))

        self.NumberTextCtrl.SetValue('p1')
        self.ChangeData(userdata['temperature'], 'temperature')

        # p1|d1|2019-05-20|37.5|37.6|37.7|37.8|37.9|38.5|38.4|38|37.5|37.3|37|37.5
        self.SetTitle("患者 - 查看患者体温信息")

    def CallRenderGraph(self, e, graphtype):
        # print(type)
        self.ChangeData(None, graphtype)

    #! 抽离可在三个界面中使用
    def ChangeData(self, data, graphtype):
        if data != None:
            # global userdata
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
            self.axes_score.set_title(graphtype)
            self.axes_score.grid(True)
            self.axes_score.set_xlabel('time')
            self.axes_score.set_ylabel('')
            FigureCanvas(self.panel, -1, self.figure_score)
            self.panel.Fit()
        else:
            global res
            global userdata
            res = '-1'
            # userdata['unumber']
            usernumber = self.NumberTextCtrl.GetValue()
            if usernumber == '':
                wx.MessageBox('不能为空！')
                return
            year = self.YearChoices[self.YearChoiceBox.GetSelection()]
            month = self.MonthChoices[self.MonthChoiceBox.GetSelection()]
            day = self.DayChoices[self.DayChoiceBox.GetSelection()]
            # year,month,day
            date = year[0:-1] + '-' + month[0:-1] + '-' + day[0:-1]
            # print(date)
            # 患者的从自己的编号汇总获取，医生自己输入
            cs = ClientSend(graphtype, 'unumber=' +
                            usernumber + '&date=' + date)
            del cs
            cv = ClientRecv()
            del cv
            # print(res)
            if res != 'None':
                resarr = res.split(',')
                # print(resarr)
                data1 = []
                for i in range(12):
                    data1.append(
                        float(resarr[i+3].replace(' ', '').replace(')', '')))
                scores = data1
                # -----------------------

                userdata[graphtype] = data1
                userdata['year'] = self.YearChoiceBox.GetSelection()
                userdata['month'] = self.MonthChoiceBox.GetSelection()
                userdata['day'] = self.DayChoiceBox.GetSelection()

                # ----------------------
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

                self.axes_score.plot(
                    t_score, s_score, 'ro', t_score, s_score, 'k')
                self.axes_score.axhline(y=average, color='r')
                self.axes_score.set_title(u'')
                self.axes_score.grid(True)
                self.axes_score.set_xlabel('time')
                self.axes_score.set_ylabel('')
                FigureCanvas(self.panel, -1, self.figure_score)
                self.panel.Fit()
            else:
                wx.MessageBox('您选择的日期没有数据！')


    # 创建 脉搏 页面

    def CreatePulsePanel(self):
        global userdata
        self.panel.Destroy()

        self.panel = panel = wx.Panel(self, -1)

        self.YearChoices = YearChoices = [u"2019年", u"2018年"]
        self.YearChoiceBox = YearChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 150), choices=YearChoices)
        YearChoiceBox.SetSelection(userdata['year'])

        self.MonthChoices = MonthChoices = [u"01月", u"02月", u"03月", u"04月", u"05月", u"06月",
                                            u"07月", u"08月", u"09月", u"10月", u"11月", u"12月"]
        self.MonthChoiceBox = MonthChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 200), choices=MonthChoices)
        MonthChoiceBox.SetSelection(userdata['month'])

        self.DayChoices = DayChoices = [
            u"01日", u"02日", u"03日", u"04日", u"05日",
            u"06日", u"07日", u"08日", u"09日", u"10日",
            u"11日", u"12日", u"13日", u"14日", u"15日",
            u"16日", u"17日", u"18日", u"19日", u"20日",
            u"21日", u"22日", u"23日", u"24日", u"25日",
            u"26日", u"27日", u"28日", u"29日", u"30日", u"31日"]
        self.DayChoiceBox = DayChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 250), choices=DayChoices)
        DayChoiceBox.SetSelection(userdata['day'])

        NumberLabel = wx.StaticText(
            panel,  wx.ID_ANY, pos=(682, 80), label="病历号:")

        self.NumberTextCtrl = NumberTextCtrl = wx.TextCtrl(
            panel, wx.ID_ANY, pos=(682, 100),)

        self.NumberTextCtrl.SetValue('p1')

        SubmitBtn = wx.Button(panel, label="确定", pos=(682, 300))
        SubmitBtn.Bind(
            wx.EVT_BUTTON, lambda event: self.CallRenderGraph(
                event, 'pulse'))
        self.ChangeData(userdata['pulse'], 'pulse')

        self.SetTitle('医生 — 查看患者脉搏信息')

    # 创建 心电 页面
    def CreateHeartPanel(self):
        global userdata
        self.panel.Destroy()

        self.panel = panel = wx.Panel(self, -1)

        self.YearChoices = YearChoices = [u"2019年", u"2018年"]
        self.YearChoiceBox = YearChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 150), choices=YearChoices)
        YearChoiceBox.SetSelection(userdata['year'])

        self.MonthChoices = MonthChoices = [u"01月", u"02月", u"03月", u"04月", u"05月", u"06月",
                                            u"07月", u"08月", u"09月", u"10月", u"11月", u"12月"]
        self.MonthChoiceBox = MonthChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 200), choices=MonthChoices)
        MonthChoiceBox.SetSelection(userdata['month'])

        self.DayChoices = DayChoices = [
            u"01日", u"02日", u"03日", u"04日", u"05日",
            u"06日", u"07日", u"08日", u"09日", u"10日",
            u"11日", u"12日", u"13日", u"14日", u"15日",
            u"16日", u"17日", u"18日", u"19日", u"20日",
            u"21日", u"22日", u"23日", u"24日", u"25日",
            u"26日", u"27日", u"28日", u"29日", u"30日", u"31日"]
        self.DayChoiceBox = DayChoiceBox = wx.Choice(
            panel, wx.ID_ANY, pos=(682, 250), choices=DayChoices)
        DayChoiceBox.SetSelection(userdata['day'])

        NumberLabel = wx.StaticText(
            panel,  wx.ID_ANY, pos=(682, 80), label="病历号:")

        self.NumberTextCtrl = NumberTextCtrl = wx.TextCtrl(
            panel, wx.ID_ANY, pos=(682, 100),)
        self.NumberTextCtrl.SetValue('p1')
        SubmitBtn = wx.Button(panel, label="确定", pos=(682, 300))
        SubmitBtn.Bind(
            wx.EVT_BUTTON, lambda event: self.CallRenderGraph(
                event, 'heart'))
        self.ChangeData(userdata['heart'], 'heart')

        self.SetTitle('医生 — 查看患者心电信息')

    # 退出程序
    def OnQuit(self, e):
        wx.MessageBox("已退出登录！")
        self.Close()


class ClientSend:
    def __init__(self, action, data):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))  # 创建一个连接
        channel = connection.channel()  # 创建通道

        # 一次请求
        # 请求都为字符串（流），根据字符不同进行不同任务！=_=
        channel.queue_declare(queue='server_recv')  # 把消息队列的名字为hello

        channel.basic_publish(
            exchange='', routing_key='server_recv',

            # !body为请求内容

            body='action=' + action + '&' + data)  # 设置routing_key（消息队列的名称）和body（发送的内容）

        connection.close()  # 关闭连接


class ClientRecv:
    def __init__(self):

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))  # 创建一个连接
        channel = connection.channel()  # 建立通道

        channel.queue_declare(
            queue='server_send')  # 把消费者和queue绑定起来，生产者和queue的也是hello

        def callback(ch, method, properties, body):  # 回调函数get消息体
            global res  # 赋值给全局变量

            # body为服务器的响应

            res = self.decode_char(body)
            connection.close()  # 关闭连接

        channel.basic_consume('server_send', callback)

        channel.start_consuming()

    def decode_char(self, *args):
        response = args[0]
        return response.decode('utf8')


def main():
    app = wx.App()
    DoctorFrame(None, title='医生 - 搜索个人信息',user='')
    app.MainLoop()


if __name__ == '__main__':
    main()
