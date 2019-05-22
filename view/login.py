# -*- coding: utf-8 -*-
"""
登录
2019.5.19
"""
import pika
import wx
import doctor
import patient


class LoginFrame(wx.Frame):
    def __init__(self, parent, title):
        super(LoginFrame, self).__init__(parent, title=title, size=(250, 150))

        self.InitUI()
        self.Centre()
        self.SetMinSize((250, 150))
        self.SetMaxSize((250, 150))
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0, 30)

        UserNameLabel = wx.StaticText(panel, label="姓名:")
        sizer.Add(UserNameLabel, pos=(0, 0), flag=wx.ALL, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl,
                  pos=(0, 1),
                  span=(1, 3),
                  flag=wx.ALL,
                  border=5)
        # 个人编号，id号
        PassWordLabel = wx.StaticText(panel, label="编号:")
        sizer.Add(PassWordLabel, pos=(1, 0), flag=wx.ALL, border=5)

        self.PassWordTextCtrl = PassWordTextCtrl = wx.TextCtrl(panel)
        sizer.Add(PassWordTextCtrl,
                  pos=(1, 1),
                  span=(1, 3),
                  flag=wx.ALL,
                  border=5)

        # 身份选择list
        IdentityLabel = wx.StaticText(panel, label="身 份:")
        sizer.Add(IdentityLabel, pos=(2, 0), flag=wx.ALL, border=5)

        self.IdentityChoices = IdentityChoices = [u"患者", u"医生"]
        self.IdentityChoicesEn = IdentityChoicesEn = ["patient", "doctor"]
        self.IdentityChoiceBox = IdentityChoiceBox = wx.Choice(
            panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            IdentityChoices, 0)
        IdentityChoiceBox.SetSelection(0)
        sizer.Add(IdentityChoiceBox,
                  pos=(2, 1),
                  span=(1, 3),
                  flag=wx.ALL,
                  border=5)
        # sizer.AddGrowableRow(2)

        LoginBtn = wx.Button(panel, label="登录")
        LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)

        sizer.Add(LoginBtn, pos=(3, 2), span=(1, 2), flag=wx.ALL, border=5)

        panel.SetSizerAndFit(sizer)

    def OnLogin(self, e):
        uname = self.UserNameTextCtrl.GetValue()
        unumber = self.PassWordTextCtrl.GetValue()
        uid = self.IdentityChoiceBox.GetSelection()

        if uname == '':
            wx.MessageBox('姓名不能为空！')
            return

        elif unumber == '':
            wx.MessageBox('ID不能为空！')

        else:
            global res
            res = '-1'
            cs = ClientSend('login', 'uname=' + uname + '&unumber=' +
                            unumber + '&uid=' + self.IdentityChoicesEn[uid])
            del cs
            cv = ClientRecv()
            del cv
            if res == '0':
                userdata = {'uname': uname, 'unumber': unumber}
                if self.IdentityChoicesEn[uid] == 'doctor':
                    self.Destroy()
                    doctor.DoctorFrame(
                        None, title='医生 - 搜索个人信息', user=userdata)
                else:
                    self.Destroy()
                    patient.PatientFrame(
                        None, title='患者 - 个人信息', user=userdata)

            else:
                wx.MessageBox('用户名或密码错误！')


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
    LoginFrame(None, title='用户登录')
    app.MainLoop()


if __name__ == '__main__':
    main()
