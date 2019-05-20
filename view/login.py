# -*- coding: utf-8 -*-
"""
登录
2019.5.19
"""
import wx
import doctor


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

        UserNameLabel = wx.StaticText(panel, label="用户名:")
        sizer.Add(UserNameLabel, pos=(0, 0), flag=wx.ALL, border=5)

        self.UserNameTextCtrl = UserNameTextCtrl = wx.TextCtrl(panel)
        sizer.Add(UserNameTextCtrl, pos=(0, 1), span=(1, 3),
                  flag=wx.ALL, border=5)

        PassWordLabel = wx.StaticText(panel, label="密 码:")
        sizer.Add(PassWordLabel, pos=(1, 0), flag=wx.ALL, border=5)

        PassWordTextCtrl = wx.TextCtrl(panel)
        sizer.Add(PassWordTextCtrl, pos=(1, 1), span=(1, 3),
                  flag=wx.ALL, border=5)

        # 身份选择list
        IdentityLabel = wx.StaticText(panel, label="身 份:")
        sizer.Add(IdentityLabel, pos=(2, 0), flag=wx.ALL, border=5)

        IdentityChoices = [u"患者", u"医生"]
        IdentityChoiceBox = wx.Choice(
            panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, IdentityChoices, 0)
        IdentityChoiceBox.SetSelection(0)
        sizer.Add(IdentityChoiceBox, pos=(2, 1), span=(
            1, 3), flag=wx.ALL, border=5)
        # sizer.AddGrowableRow(2)

        LoginBtn = wx.Button(panel, label="登录")
        LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)

        RegisterBtn = wx.Button(panel, label="注册")
        RegisterBtn.Bind(wx.EVT_BUTTON, self.OnRegister)

        sizer.Add(LoginBtn, pos=(3, 0), span=(1, 2), flag=wx.ALL, border=5)
        sizer.Add(RegisterBtn, pos=(3, 2), span=(1, 2), flag=wx.ALL, border=5)

        panel.SetSizerAndFit(sizer)

    def OnLogin(self, e):
        # print(self.UserNameTextCtrl.GetValue())
        self.Destroy()
        doctor.DoctorFrame(None, title='医生 - 搜索个人信息')

    def OnRegister(self, e):
        pass


def main():
    app = wx.App()
    LoginFrame(None, title='用户登录')
    app.MainLoop()


if __name__ == '__main__':
    main()
