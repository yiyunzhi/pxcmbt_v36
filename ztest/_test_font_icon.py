# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_font_icon.py
# ------------------------------------------------------------------------------
#
# File          : _test_font_icon.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx, json
from framework.gui.icon_repo.class_icon_repo import IconRepo, FontIconIconRepoCategory


class MBTArtProvider(wx.ArtProvider):
    def __init__(self):
        wx.ArtProvider.__init__(self)
        self.iconRepo = IconRepo()
        self.fontIconCategory = FontIconIconRepoCategory(name='fi')
        self.iconRepo.register(self.fontIconCategory)

    def CreateBitmap(self, art_id: str, client=wx.ART_TOOLBAR, size=wx.Size(16, 16)):
        # You can do anything here you want, such as using the same
        # image for any size, any client, etc., or using specific
        # images for specific sizes, whatever...
        if art_id.startswith('wxART'):
            return super().CreateBitmap(art_id, client, size)
        # See end of file for the image data
        _bmp = wx.NullBitmap
        _bmp = self.iconRepo.get_bmp(category=self.fontIconCategory.name, name=art_id, size=size)
        if not _bmp.IsOk():
            print("MBTArtProvider error: providing %s:%s at size %s \n" % (art_id, client, size))
        return _bmp

    def GetBitmapEnhance(self, art_id:str, client=wx.ART_OTHER, size=wx.DefaultSize, **kwargs):
        if isinstance(size, tuple):
            size = wx.Size(*size)
        if art_id.startswith('wxART'):
            return super().CreateBitmap(art_id, client, size)
        _bmp = self.iconRepo.get_bmp(category=self.fontIconCategory.name, name=art_id, size=size, **kwargs)
        if not _bmp.IsOk():
            print("MBTArtProvider error: providing %s:%s at size %s \n" % (art_id, client, size))
        return _bmp


_mbt_art_provider = MBTArtProvider()

wx.ArtProvider.Push(_mbt_art_provider)


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.mainLayout = wx.BoxSizer(wx.HORIZONTAL)
        # self.ti = FontIcon(self)

        # self.label = wx.BitmapButton(self, bitmap=get_bmp('\uf019'), size=(32, 32))
        self.label = wx.BitmapButton(self, bitmap=wx.ArtProvider.GetBitmap('fa47.user'), size=(32, 32))
        # self.label2 = wx.BitmapButton(self, bitmap=get_bmp('\uf0fe'), size=(32, 32))
        self.label2 = wx.BitmapButton(self, bitmap=wx.ArtProvider.GetBitmap('ri.user-line', size=(24, 24)),
                                      size=(32, 32))
        # self.bmp1 = wx.StaticBitmap(self, bitmap=get_bmp('\uf13a'))
        self.bmp1 = wx.StaticBitmap(self, bitmap=wx.ArtProvider.GetBitmap('pi.user', size=(24, 24)), size=(48, 48))
        self.bmp2 = wx.StaticBitmap(self, bitmap=wx.ArtProvider.GetBitmap('md5.content-save-all', size=(24, 24)),
                                    size=(48, 48))
        self.bmp3 = wx.StaticBitmap(self,
                                    bitmap=_mbt_art_provider.GetBitmapEnhance('md5.account-child-circle', size=(64, 64),
                                                                              color='red'), size=(64, 64))
        self.bmp4 = wx.StaticBitmap(self, bitmap=wx.ArtProvider.GetBitmap(wx.ART_ERROR, size=(24, 24)), size=(48, 48))
        # self.bmp2.SetBackgroundColour(wx.Colour('red'))

        self.label.Disable()
        self.mainLayout.Add(self.label, 0)
        self.mainLayout.Add(self.label2, 0)
        self.mainLayout.Add(self.bmp1, 0)
        self.mainLayout.Add(self.bmp2, 0)
        self.mainLayout.Add(self.bmp3, 0)
        self.mainLayout.Add(self.bmp4, 0)
        self.SetSizer(self.mainLayout)
        self.Layout()


app = wx.App()
frame = Frame()
frame.Show()
app.MainLoop()
