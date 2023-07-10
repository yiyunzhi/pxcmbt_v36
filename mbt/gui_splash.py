import os, wx
import wx.lib.agw.advancedsplash as advsp
from mbt.application.define_base import APP_NAME, APP_VERSION
from mbt.resources import SPLASH_IMAGE
from framework.gui.utils import gui_util_get_default_font


class SplashScreen:
    def __init__(self, parent=None, timeout=5000):
        self.img = wx.Bitmap(SPLASH_IMAGE,wx.BITMAP_TYPE_PNG)
        self.titleTxt = '%s v%s' % (APP_NAME, APP_VERSION)
        self.messageTxtLst = [self.titleTxt, '']
        self.splash = advsp.AdvancedSplash(parent, wx.ID_ANY, timeout=timeout,
                                           bitmap=self.img,shadowcolour=wx.LIGHT_GREY)
        #self.splash.SetWindowStyle(self.splash.GetWindowStyle()|advsp.AS_SHADOW_BITMAP)
        self.splash.SetBackgroundColour(wx.WHITE)
        self.splash.SetTextPosition((10, 15))
        self.splash.SetTextFont(gui_util_get_default_font(10))
        self.splash.SetTextColour(wx.Colour('#777'))

    def set_message(self, msg):
        self.messageTxtLst.append(msg)
        _txt = '\n'.join(self.messageTxtLst)
        self.splash.SetText(_txt)

    def close(self):
        self.splash.Destroy()
