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
import re
import json
import pika
from parse import hl72json

# 保存全局状态，基本信息，图表信息，不再继续请求
userdata = {}


class PatientFrame(wx.Frame):

    def __init__(self, parent, title, user):
        super(PatientFrame, self).__init__(
            parent, title=title, size=(800, 400))
        global userdata
        userdata = user
        # 用户 全局状态
        # print(userdata)
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

        self.nm1 = nm1 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm1, 0, wx.ALL | wx.CENTER, 5)

        ln = wx.StaticText(panel, -1, "按姓名查找：")
        nmbox.Add(ln, 0, wx.ALL | wx.CENTER, 5)

        self.nm2 = nm2 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm2, 0, wx.ALL | wx.CENTER, 5)

        ln1 = wx.StaticText(panel, -1, "按联系方式查找：")
        nmbox.Add(ln1, 0, wx.ALL | wx.CENTER, 5)

        self.nm3 = nm3 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
        nmbox.Add(nm3, 0, wx.ALL | wx.CENTER, 5)

        FindBtn = wx.Button(panel, label="查找")
        # LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
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
        sizer.Add(FamilyMedicalHistoryLabel, pos=(3, 4), flag=wx.ALL | wx.EXPAND, border=5)

        self.FamilyMedicalHistoryTextCtrl = FamilyMedicalHistoryTextCtrl = wx.TextCtrl(panel)
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
        sizer.Add(CheckRecordLabel, pos=(4, 4), flag=wx.ALL | wx.EXPAND, border=5)

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
       
        global res
        res = '-1'
        cs = ClientSend('getdata', 'unumber=p1' )  # userdata['unumber']
        del cs
        cv = ClientRecv()
        del cv
        if res != '-1':
            filejson = hl72json.hl72json(self,'patient.txt')
            after = filejson.replace('\n','')
            # 姓名
            names = re.findall(".*PID.2.6\"(.*)\"(PID.2.8).*", after)
            name = self.trim(names)
            self.nm2.SetValue(name)
            self.UserNameTextCtrl.SetValue(name)
            # 编号
            unumbers = re.findall(".*PID.2.4\"(.*)\"(PID.2.6).*", after)
            unumber = self.trim(unumbers)
            self.nm1.SetValue(unumber)
            self.MedicalNumberTextCtrl.SetValue(unumber)
            # 联系方式
            phones = re.findall(".*PID.2.14\"(.*)\"(PID.2.15).*", after)
            phone = self.trim(phones)
            self.nm3.SetValue(phone)
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

        # !注意顺序！
        self.Show()
        self.SetTitle("患者 - 搜索个人信息")

    def trim(self, origin):
        return origin[0][0].replace(' ', '').replace('\"', '').replace(',', '').replace(':', '').replace('}', '').replace('CDA.3', '').replace('ZCS.4', '')

    def toHL7file(self, patient):
        with open('patient.txt', 'w', encoding='utf-8') as f:
            f.write(patient)

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
    PatientFrame(None, title='患者 - 搜索个人信息', user='')
    app.MainLoop()


if __name__ == '__main__':
    main()
