# -*- coding: utf-8 -*-
"""
desc: 空页面
last modified: 2019.5.19
"""

import wx


class Frame(wx.Frame):

    def __init__(self, parent, title):
        super(Frame, self).__init__(
            parent, title=title, size=(1000, 600))

        self.InitUI()
        self.Centre()
        self.SetMinSize((1000, 600))
        self.SetMaxSize((1000, 600))
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0, 30)

        # sizer.Add(RegisterBtn, pos=(3, 2), span=(1, 2), flag=wx.ALL, border=5)
        # self.sb = self.CreateStatusBar()

        # toolbar.Bind(wx.EVT_TOOL_ENTER, self.OnMove)
        # qtool.SetToolTipString("This is a BIG button...")
        # self.Bind(wx.EVT_LEFT_UP, self.OnWidgetEnter, qtool)

        panel.SetSizerAndFit(sizer)

    def onLogin(self, e):
        print(self.UserNameTextCtrl.GetValue())


def main():
    app = wx.App()
    Frame(None, title='x')
    app.MainLoop()


if __name__ == '__main__':
    main()
