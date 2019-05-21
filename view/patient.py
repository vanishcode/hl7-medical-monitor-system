# # # # # # # # # # # # -*- coding: utf-8 -*-
# # # # # # # # # # # """
# # # # # # # # # # # desc: 空页面
# # # # # # # # # # # last modified: 2019.5.19
# # # # # # # # # # # """

# # # # # # # # # # # import wx


# # # # # # # # # # # class Frame(wx.Frame):

# # # # # # # # # # #     def __init__(self, parent, title):
# # # # # # # # # # #         super(Frame, self).__init__(
# # # # # # # # # # #             parent, title=title, size=(1000, 600))

# # # # # # # # # # #         self.InitUI()
# # # # # # # # # # #         self.Centre()
# # # # # # # # # # #         # self.SetMinSize((1000, 600))
# # # # # # # # # # #         # self.SetMaxSize((1000, 600))
# # # # # # # # # # #         self.Show()

# # # # # # # # # # #     def InitUI(self):

# # # # # # # # # # #         panel = wx.Panel(self)
# # # # # # # # # # #         vbox = wx.BoxSizer(wx.VERTICAL)
# # # # # # # # # # #         nm = wx.StaticBox(panel, -1, 'Name:')
# # # # # # # # # # #         nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

# # # # # # # # # # #         nmbox = wx.BoxSizer(wx.HORIZONTAL)
# # # # # # # # # # #         fn = wx.StaticText(panel, -1, "First Name")

# # # # # # # # # # #         nmbox.Add(fn, 0, wx.ALL | wx.CENTER, 5)
# # # # # # # # # # #         nm1 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
# # # # # # # # # # #         nm2 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
# # # # # # # # # # #         ln = wx.StaticText(panel, -1, "Last Name")

# # # # # # # # # # #         nmbox.Add(nm1, 0, wx.ALL | wx.CENTER, 5)
# # # # # # # # # # #         nmbox.Add(ln, 0, wx.ALL | wx.CENTER, 5)
# # # # # # # # # # #         nmbox.Add(nm2, 0, wx.ALL | wx.CENTER, 5)
# # # # # # # # # # #         nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 10)

# # # # # # # # # # #         panel.SetSizer(vbox)

# # # # # # # # # # #     def OnClose(self, e):
# # # # # # # # # # #         self.Close(True)


# # # # # # # # # # # def main():
# # # # # # # # # # #     app = wx.App()
# # # # # # # # # # #     Frame(None, title='x')
# # # # # # # # # # #     app.MainLoop()


# # # # # # # # # # # if __name__ == '__main__':
# # # # # # # # # # #     main()
# # # # # # # # # # import wx


# # # # # # # # # # class Mywin(wx.Frame):
# # # # # # # # # #     def __init__(self, parent, title):
# # # # # # # # # #         super(Mywin, self).__init__(parent, title=title, size=(900, 300))

# # # # # # # # # #         panel = wx.Panel(self)
# # # # # # # # # #         vbox = wx.BoxSizer(wx.VERTICAL)
# # # # # # # # # #         # name
# # # # # # # # # #         nm = wx.StaticBox(panel, -1, '用户查找条件')
# # # # # # # # # #         nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

# # # # # # # # # #         nmbox = wx.BoxSizer(wx.HORIZONTAL)

# # # # # # # # # #         fn = wx.StaticText(panel, -1, "按病历编号查找：")
# # # # # # # # # #         nmbox.Add(fn, 0, wx.ALL | wx.CENTER, 5)

# # # # # # # # # #         nm1 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
# # # # # # # # # #         nmbox.Add(nm1, 0, wx.ALL | wx.CENTER, 5)

# # # # # # # # # #         ln = wx.StaticText(panel, -1, "按姓名查找：")
# # # # # # # # # #         nmbox.Add(ln, 0, wx.ALL | wx.CENTER, 5)

# # # # # # # # # #         nm2 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
# # # # # # # # # #         nmbox.Add(nm2, 0, wx.ALL | wx.CENTER, 5)

# # # # # # # # # #         ln1 = wx.StaticText(panel, -1, "按联系方式查找：")
# # # # # # # # # #         nmbox.Add(ln1, 0, wx.ALL | wx.CENTER, 5)

# # # # # # # # # #         nm3 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT)
# # # # # # # # # #         nmbox.Add(nm3, 0, wx.ALL | wx.CENTER, 5)

# # # # # # # # # #         LoginBtn = wx.Button(panel, label="查找")
# # # # # # # # # #         LoginBtn.Bind(wx.EVT_BUTTON, self.OnLogin)
# # # # # # # # # #         nmbox.Add(LoginBtn, 0, wx.ALL | wx.CENTER, 5)

# # # # # # # # # #         nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 10)

# # # # # # # # # #         vbox.Add(nmSizer, 0, wx.ALL | wx.CENTER, 5)

# # # # # # # # # #         panel.SetSizer(vbox)
# # # # # # # # # #         self.Centre()

# # # # # # # # # #         panel.Fit()
# # # # # # # # # #         self.Show()

# # # # # # # # # #     def OnLogin(self):
# # # # # # # # # #         pass


# # # # # # # # # # app = wx.App()
# # # # # # # # # # Mywin(None,  'Staticboxsizer')
# # # # # # # # # # app.MainLoop()
# # # # # # # # # import wx
# # # # # # # # # import wx.grid


# # # # # # # # # class GridFrame(wx.Frame):
# # # # # # # # #     def __init__(self, parent):
# # # # # # # # #         wx.Frame.__init__(self, parent)

# # # # # # # # #         # Create a wxGrid object
# # # # # # # # #         grid = wx.grid.Grid(self, -1)

# # # # # # # # #         # Then we call CreateGrid to set the dimensions of the grid
# # # # # # # # #         # (100 rows and 10 columns in this example)
# # # # # # # # #         grid.CreateGrid(10, 8)

# # # # # # # # #         # We can set the sizes of individual rows and columns
# # # # # # # # #         # in pixels
# # # # # # # # #         # grid.SetRowSize(0, 00)
# # # # # # # # #         grid.SetColSize(0, 100)

# # # # # # # # #         # And set grid cell contents as strings
# # # # # # # # #         grid.SetCellValue(0, 0, 'wxGrid is good')

# # # # # # # # #         # We can specify that some cells are read.only
# # # # # # # # #         grid.SetCellValue(0, 3, 'This is read.only')
# # # # # # # # #         # grid.SetReadOnly(0, 3)

# # # # # # # # #         # Colours can be specified for grid cell contents
# # # # # # # # #         # grid.SetCellValue(3, 3, 'green on grey')
# # # # # # # # #         # grid.SetCellTextColour(3, 3, wx.GREEN)
# # # # # # # # #         # grid.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)

# # # # # # # # #         # We can specify the some cells will store numeric
# # # # # # # # #         # values rather than strings. Here we set grid column 5
# # # # # # # # #         # to hold floating point values displayed with width of 6
# # # # # # # # #         # and precision of 2

# # # # # # # # #         self.Show()


# # # # # # # # # if __name__ == '__main__':

# # # # # # # # #     app = wx.App(0)
# # # # # # # # #     frame = GridFrame(None)
# # # # # # # # #     app.MainLoop()
# # # # # # # # import wx
# # # # # # # # import wx.grid as grid
# # # # # # # # #


# # # # # # # # class Frame(wx.Frame):
# # # # # # # #     def __init__(self, parent):
# # # # # # # #         wx.Frame.__init__(self, parent, -1, "Grid", size=(350, 250))
# # # # # # # #         self.grid = grid.Grid(self)
# # # # # # # #         self.grid.CreateGrid(20, 20)
# # # # # # # #         # self.but = Button(None, self)


# # # # # # # # if __name__ == '__main__':
# # # # # # # #     app = wx.PySimpleApp()
# # # # # # # #     frame = Frame(None)
# # # # # # # #     frame.Show()
# # # # # # # #     app.MainLoop()
# # # # # # # import wx
# # # # # # # import wx.grid as gridlib


# # # # # # # class TestTable(wx.grid.PyGridTableBase):
# # # # # # #     def __init__(self):
# # # # # # #         gridlib.PyGridTableBase.__init__(self)
# # # # # # #         self.rowLabels = ["uno", "dos", "tres", "quatro", "cinco"]
# # # # # # #         self.colLabels = ["homer", "marge", "bart", "lisa", "maggie"]

# # # # # # #     def GetNumberRows(self):
# # # # # # #         return 5

# # # # # # #     def GetNumberCols(self):
# # # # # # #         return 5

# # # # # # #     def IsEmptyCell(self, row, col):
# # # # # # #         return False

# # # # # # #     def GetValue(self, row, col):
# # # # # # #         return "(%s,%s)" % (self.rowLabels[row], self.colLabels[col])

# # # # # # #     def SetValue(self, row, col, value):
# # # # # # #         pass

# # # # # # #     def GetColLabelValue(self, col):
# # # # # # #         return self.colLabels[col]

# # # # # # #     def GetRowLabelValue(self, row):
# # # # # # #         return self.rowLabels[row]


# # # # # # # class CustTableGrid(gridlib.Grid):
# # # # # # #     def __init__(self, parent):
# # # # # # #         gridlib.Grid.__init__(self, parent, -1)

# # # # # # #         table = TestTable()

# # # # # # #         # The second parameter means that the grid is to takeownership of the
# # # # # # #         # table and will destroy it when done.  Otherwise you wouldneed to keep
# # # # # # #         # a reference to it and call it's Destroy method later.
# # # # # # #         self.SetTable(table, True)

# # # # # # #         self.SetRowLabelSize(0)
# # # # # # #         self.SetMargins(0, 0)
# # # # # # #         self.AutoSizeColumns(False)


# # # # # # # class TestFrame(wx.Frame):
# # # # # # #     def __init__(self):
# # # # # # #         wx.Frame.__init__(self, None, title="Grid Table",
# # # # # # #                           )
# # # # # # #         panel1 = wx.Panel(self, -1)
# # # # # # #         panel2 = wx.Panel(self, -1)
# # # # # # #         hbox1 = wx.BoxSizer(wx.HORIZONTAL)

# # # # # # #         hbox1.Add(panel1, 1, wx.EXPAND | wx.ALL, 3)
# # # # # # #         hbox1.Add(panel2, 1, wx.EXPAND | wx.ALL, 3)

# # # # # # #         table = CustTableGrid(panel2)
# # # # # # #         tblSizer = wx.BoxSizer(wx.VERTICAL)
# # # # # # #         tblSizer.Add(table, 1, wx.ALL | wx.EXPAND, 5)
# # # # # # #         panel2.SetSizer(tblSizer)

# # # # # # #         self.SetSizer(hbox1)


# # # # # # # app = wx.PySimpleApp()
# # # # # # # frame = TestFrame()
# # # # # # # frame.Show()
# # # # # # # app.MainLoop()
# # # # # # import sys
# # # # # # import wx

# # # # # # players = [('Tendulkar', '15000', '100'), ('Dravid', '14000', '1'),
# # # # # #            ('Kumble', '1000', '700'), ('KapilDev', '5000', '400'),
# # # # # #            ('Ganguly', '8000', '50')]


# # # # # # class Mywin(wx.Frame):
# # # # # #     def __init__(self, parent, title):
# # # # # #         super(Mywin, self).__init__(parent, title=title)

# # # # # #         panel = wx.Panel(self)

# # # # # #         box = wx.BoxSizer(wx.HORIZONTAL)

# # # # # #         self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
# # # # # #         self.list.InsertColumn(0, 'name', width=100)
# # # # # #         self.list.InsertColumn(1, 'runs', wx.LIST_FORMAT_RIGHT, 100)
# # # # # #         self.list.InsertColumn(2, 'wkts', wx.LIST_FORMAT_RIGHT, 100)

# # # # # #         for i in players:
# # # # # #             index = self.list.InsertStringItem(666, i[0])
# # # # # #             self.list.SetStringItem(index, 1, i[1])
# # # # # #             self.list.SetStringItem(index, 2, i[2])

# # # # # #         box.Add(self.list, 1, wx.EXPAND)
# # # # # #         panel.SetSizer(box)
# # # # # #         panel.Fit()

# # # # # #         self.Centre()

# # # # # #         self.Show(True)


# # # # # # ex = wx.App()
# # # # # # Mywin(None, 'ListCtrl Demo')
# # # # # # ex.MainLoop()

# # # # # import wx


# # # # # class MyForm(wx.Frame):

# # # # #     def __init__(self):
# # # # #         wx.Frame.__init__(self, None, wx.ID_ANY, 'My Form')

# # # # #         # Add a panel so it looks the correct on all platforms
# # # # #         self.panel = wx.Panel(self, wx.ID_ANY)

# # # # #         bmp = wx.ArtProvider.GetBitmap(
# # # # #             wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
# # # # #         font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)

# # # # #         titleIco = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)
# # # # #         title = wx.StaticText(self.panel, wx.ID_ANY, 'My Title')
# # # # #         title.SetFont(font)

# # # # #         # 1st row of widgets
# # # # #         bmp = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (16, 16))
# # # # #         inputOneIco = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)
# # # # #         labelOne = wx.StaticText(self.panel, wx.ID_ANY, 'Name')
# # # # #         inputTxtOne = wx.TextCtrl(self.panel, wx.ID_ANY)

# # # # #         sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
# # # # #                       'six', 'seven', 'eight']
# # # # #         rb = wx.RadioBox(
# # # # #             self.panel, wx.ID_ANY, "wx.RadioBox", wx.DefaultPosition,
# # # # #             wx.DefaultSize, sampleList, 2, wx.RA_SPECIFY_COLS
# # # # #         )

# # # # #         # 2nd row of widgets
# # # # #         multiTxt = wx.TextCtrl(self.panel, wx.ID_ANY,
# # # # #                                size=(200, 100),
# # # # #                                style=wx.TE_MULTILINE)
# # # # #         sampleList = ['one', 'two', 'three', 'four']
# # # # #         combo = wx.ComboBox(self.panel, wx.ID_ANY, 'Default', wx.DefaultPosition,
# # # # #                             (100, -1), sampleList, wx.CB_DROPDOWN)

# # # # #         # Create the sizers
# # # # #         topSizer = wx.BoxSizer(wx.VERTICAL)
# # # # #         titleSizer = wx.BoxSizer(wx.HORIZONTAL)
# # # # #         bagSizer = wx.GridBagSizer(hgap=5, vgap=5)

# # # # #         # Add widgets to sizers
# # # # #         titleSizer.Add(titleIco, 0, wx.ALL, 5)
# # # # #         titleSizer.Add(title, 0, wx.ALL, 5)

# # # # #         bagSizer.Add(inputOneIco, pos=(0, 0),
# # # # #                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
# # # # #                      border=5)
# # # # #         bagSizer.Add(labelOne, pos=(0, 1),
# # # # #                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
# # # # #                      border=5)
# # # # #         bagSizer.Add(inputTxtOne, pos=(0, 2),
# # # # #                      flag=wx.EXPAND | wx.ALL,
# # # # #                      border=10)
# # # # #         bagSizer.AddGrowableCol(2, 0)
# # # # #         bagSizer.Add(rb, pos=(0, 3), span=(3, 2))

# # # # #         bagSizer.Add(multiTxt, pos=(1, 0),
# # # # #                      flag=wx.ALL,
# # # # #                      border=5)
# # # # #         bagSizer.Add(combo, pos=(1, 1),
# # # # #                      flag=wx.ALL,
# # # # #                      border=5)

# # # # #         # Add sub-sizers to topSizer
# # # # #         topSizer.Add(titleSizer, 0, wx.CENTER)
# # # # #         topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL | wx.EXPAND, 5)
# # # # #         topSizer.Add(bagSizer, 0, wx.ALL | wx.EXPAND, 5)

# # # # #         self.panel.SetSizer(topSizer)

# # # # #         # SetSizeHints(minW, minH, maxW, maxH)
# # # # #         self.SetSizeHints(250, 200, 700, 300)
# # # # #         topSizer.Fit(self)


# # # # # # Run the program
# # # # # if __name__ == '__main__':
# # # # #     app = wx.PySimpleApp()
# # # # #     frame = MyForm().Show()
# # # # #     app.MainLoop()

# # # # import wx
# # # # import sys
# # # # import traceback


# # # # def show_error():
# # # #     message = ''.join(traceback.format_exception(*sys.exc_info()))
# # # #     dialog = wx.MessageDialog(None, message, 'Error!', wx.OK | wx.ICON_ERROR)
# # # #     dialog.ShowModal()


# # # # class MyPanels(wx.Panel):

# # # #     def __init__(self, parent, id):
# # # #         wx.Panel.__init__(self, parent)
# # # #         self.parent = parent


# # # # class MyFrame(wx.Frame):
# # # #     def __init__(self, parent, id, title):
# # # #         wx.Frame.__init__(self, parent, id, title, size=(1000, 480))
# # # #         self.parent = parent

# # # #         self.panel = wx.Panel(self, -1)
# # # #         self.panel.SetBackgroundColour("grey")

# # # #         self.leftpanel = MyPanels(self.panel, 1)
# # # #         self.rightpanel = MyPanels(self.panel, 1)
# # # #         self.leftpanel.SetBackgroundColour("red")
# # # #         self.rightpanel.SetBackgroundColour("green")

# # # #         self.basicsizer = wx.BoxSizer(wx.HORIZONTAL)
# # # #         self.basicsizer.Add(self.leftpanel, 1, wx.EXPAND)
# # # #         self.basicsizer.Add(self.rightpanel, 1, wx.EXPAND)
# # # #         self.panel.SetSizer(self.basicsizer)

# # # #         button = wx.Button(self.leftpanel, 1, 'DIE DIE DIE', (50, 130))
# # # #         buttonres = wx.Button(self.leftpanel, 2, 'Resurrect', (50, 230))
# # # #         buttonextra = wx.Button(self.leftpanel, 3, 'Test', (50, 330))

# # # #         self.Bind(wx.EVT_BUTTON, self.destroyPanel, button)
# # # #         self.Bind(wx.EVT_BUTTON, self.CreateNewPanel, buttonres)

# # # #     def CreateNewPanel(self, event):
# # # #         self.rightpanel = MyPanels(self.panel, 1)
# # # #         self.rightpanel.SetBackgroundColour("green")
# # # #         self.basicsizer.Add(self.rightpanel, 1, wx.EXPAND)
# # # #         self.panel.Layout()

# # # #         self.Show(True)
# # # #         self.Centre()

# # # #     def destroyPanel(self, event):
# # # #         self.rightpanel.Hide()
# # # #         self.panel.Layout()


# # # # def main():
# # # #     app = wx.App()
# # # #     try:
# # # #         frame = MyFrame(None, -1, 'Die.py')
# # # #         frame.Show()
# # # #         app.MainLoop()
# # # #     except:
# # # #         show_error()


# # # # if __name__ == '__main__':
# # # #     main()

# # # import wx
# # # import wx.grid as gridlib

# # # ########################################################################


# # # class PanelOne(wx.Panel):
# # #     """"""

# # #     # ----------------------------------------------------------------------
# # #     def __init__(self, parent):
# # #         """Constructor"""
# # #         wx.Panel.__init__(self, parent=parent)
# # #         txt = wx.TextCtrl(self)

# # # ########################################################################


# # # class PanelTwo(wx.Panel):
# # #     """"""

# # #     # ----------------------------------------------------------------------
# # #     def __init__(self, parent):
# # #         """Constructor"""
# # #         wx.Panel.__init__(self, parent=parent)

# # #         grid = gridlib.Grid(self)
# # #         grid.CreateGrid(25, 12)

# # #         sizer = wx.BoxSizer(wx.VERTICAL)
# # #         sizer.Add(grid, 0, wx.EXPAND)
# # #         self.SetSizer(sizer)

# # # ########################################################################


# # # class MyForm(wx.Frame):

# # #     # ----------------------------------------------------------------------
# # #     def __init__(self):
# # #         wx.Frame.__init__(self, None, wx.ID_ANY,
# # #                           "Panel Switcher Tutorial")

# # #         self.panel_one = PanelOne(self)
# # #         self.panel_two = PanelTwo(self)
# # #         self.panel_two.Hide()

# # #         self.sizer = wx.BoxSizer(wx.VERTICAL)
# # #         self.sizer.Add(self.panel_one, 1, wx.EXPAND)
# # #         self.sizer.Add(self.panel_two, 1, wx.EXPAND)
# # #         self.SetSizer(self.sizer)

# # #         menubar = wx.MenuBar()
# # #         fileMenu = wx.Menu()
# # #         switch_panels_menu_item = fileMenu.Append(wx.ID_ANY,
# # #                                                   "Switch Panels",
# # #                                                   "Some text")
# # #         self.Bind(wx.EVT_MENU, self.onSwitchPanels,
# # #                   switch_panels_menu_item)
# # #         menubar.Append(fileMenu, '&File')
# # #         self.SetMenuBar(menubar)

# # #     # ----------------------------------------------------------------------
# # #     def onSwitchPanels(self, event):
# # #         """"""
# # #         if self.panel_one.IsShown():
# # #             self.SetTitle("Panel Two Showing")
# # #             self.panel_one.Hide()
# # #             self.panel_two.Show()
# # #         else:
# # #             self.SetTitle("Panel One Showing")
# # #             self.panel_one.Show()
# # #             self.panel_two.Hide()
# # #         self.Layout()


# # # # Run the program
# # # if __name__ == "__main__":
# # #     app = wx.App(False)
# # #     frame = MyForm()
# # #     frame.Show()
# # #     app.MainLoop()

# # import wx
# # from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
# # from matplotlib.figure import Figure

# # import numpy


# # class MainFrame(wx.Frame):
# #     def __init__(self, *args, **kwargs):
# #         wx.Frame.__init__(self, *args, **kwargs)

# #         panel = wx.Panel(self)
# #         sizer = wx.BoxSizer(wx.HORIZONTAL)
# #         sizer.Add(MakePlot(panel), 1, wx.EXPAND | wx.ALL, border=5)
# #         sizer.Add(MakePlot(panel), 1, wx.EXPAND | wx.ALL, border=5)
# #         panel.SetSizer(sizer)
# #         # don't do Fit(), as it sets the canvases to its minimum size
# #         panel.Layout()


# # class MakePlot(wx.Window):
# #     def __init__(self, *args, **kwargs):
# #         wx.Window.__init__(self, *args, **kwargs)

# #         scores = [36, 36.5, 37.5, 38, 37, 37.5, 37, 37.5, 37.5, 37.5]
# #         sum = 0
# #         for s in scores:
# #             sum += s
# #         average = sum / len(scores)

# #         t_score = numpy.arange(1, len(scores) + 1, 1)
# #         s_score = numpy.array(scores)

# #         self.figure_score = Figure()
# #         self.figure_score.set_figheight(3.6)
# #         self.figure_score.set_figwidth(7.8)
# #         self.axes_score = self.figure_score.add_subplot(111)

# #         self.axes_score.plot(t_score, s_score, 'ro', t_score, s_score, 'k')
# #         self.axes_score.axhline(y=average, color='r')
# #         self.axes_score.set_title(u'My Scores')
# #         self.axes_score.grid(True)
# #         self.axes_score.set_xlabel('T')
# #         self.axes_score.set_ylabel('score')

# #         self.canvas = FigureCanvasWxAgg(self, wx.ID_ANY, self.figure_score)
# #         # FigureCanvas(self.scorePanel, -1, self.figure_score)
# #         # setting the minimum canvas size as small as possible
# #         self.canvas.SetMinSize(wx.Size(1, 1))

# #         sizer = wx.BoxSizer(wx.HORIZONTAL)
# #         # added wx.EXPAND so that the canvas can stretch vertically
# #         sizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND, border=20)
# #         self.SetSizer(sizer)


# # if __name__ == "__main__":
# #     app = wx.App()
# #     MainFrame(parent=None, size=(800, 500)).Show()
# #     app.MainLoop()

# import wx
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_wx import NavigationToolbar2Wx
# from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
# from numpy import arange, sin, pi
# import matplotlib
# matplotlib.use('WXAgg')


# class CanvasPanel(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#         self.figure = Figure()
#         self.axes = self.figure.add_subplot(111)
#         self.canvas = FigureCanvas(self, -1, self.figure)
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
#         self.SetSizer(self.sizer)
#         self.Fit()

#     def draw(self):
#         t = arange(0.0, 3.0, 0.01)
#         s = sin(2 * pi * t)
#         self.axes.plot(t, s)


# if __name__ == "__main__":
#     app = wx.PySimpleApp()
#     fr = wx.Frame(None, title='test')
#     panel = CanvasPanel(fr)
#     panel.draw()
#     fr.Show()
#     app.MainLoop()
import pyecharts
# //设置行名
columns = ["Jan", "Feb", "Mar", "Apr", "May",
           "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# //设置数据
data1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
data2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
# //设置柱状图的主标题与副标题
bar = pyecharts.Bar("柱状图", "一年的降水量与蒸发量")
# //添加柱状图的数据及配置项
bar.add("降水量", columns, data1, mark_line=[
        "average"], mark_point=["max", "min"])
bar.add("蒸发量", columns, data2, mark_line=[
        "average"], mark_point=["max", "min"])
# //生成本地文件（默认为.html文件）
bar.render()
