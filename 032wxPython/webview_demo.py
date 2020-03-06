# coding:utf-8
"""
create on Mar 6, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

尝试着在wxpython中内嵌浏览器

"""
import wx
from wx.html2 import WebView


class MyHtmlFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(1024, 768))
        web_view = WebView.New(self)
        web_view.LoadURL("http://www.mryu.top/")


app = wx.App()
frm = MyHtmlFrame(None, "Browser")
frm.Show()
app.MainLoop()