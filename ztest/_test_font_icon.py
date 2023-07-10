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


#
# _ret = True
#
# _ret = wx.Font.AddPrivateFont('fontawesome5-solid-webfont.ttf')
# _ret &= wx.Font.AddPrivateFont('remixicon.ttf')
# print(_ret, '\uea67', '\uf066', wx.Font.CanUsePrivateFont())
#
#
# class FontIcon(wx.Panel):
#     def __init__(self, *args, **kwargs):
#         wx.Panel.__init__(self, *args, **kwargs)
#         self.Bind(wx.EVT_PAINT, self.on_paint)
#         self.bmp = wx.Bitmap()
#
#     def on_paint(self, evt):
#         _dc = wx.PaintDC(self)
#         _dc.SetFont(wx.Font(wx.FontInfo(24).FaceName('FontAwesome')))
#         _dc.DrawText('\uf238', 0, 0)
#         self.bmp = _dc.GetAsBitmap()
#
#
# def get_bmp(code, w=24, h=24, color=None):
#     _gbmp = wx.Bitmap(w * 2, h * 2)
#     _ddc = wx.MemoryDC(_gbmp)
#     _ddc.Clear()
#     # Create graphics context from it
#     gcdc = wx.GCDC(_ddc)
#     # gc = wx.GraphicsContext.Create(_ddc)
#     # gc.SetAntialiasMode(wx.ANTIALIAS_DEFAULT)
#     # _ddc.SetFont(wx.Font(wx.FontInfo(min(w, h)-4).FaceName('FontAwesome')))
#     # _ddc.DrawText(code, 0, -2)
#     # todo: code like fa.ffs->faceName and Name.
#     # gcdc.SetFont(wx.Font(wx.FontInfo(min(w*2, h*2) - 4*2).FaceName('FontAwesome')))
#     gcdc.SetFont(wx.Font(wx.FontInfo(min(w * 2, h * 2) - 4 * 2).FaceName('remixicon')))
#     gcdc.SetTextForeground(wx.Colour('#3f3f3f'))
#     gcdc.DrawText(code, 0, -2)
#     # gc.SetFont(wx.Font(wx.FontInfo(min(w, h) - 4).FaceName('FontAwesome')), wx.Colour('#3f3f3f'))
#     # gc.DrawText(code, 0, -2)
#     gcdc.Destroy()
#     _gbmp.Rescale(_gbmp, wx.Size(w, h))
#     return _gbmp


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
        self.bmp2 = wx.StaticBitmap(self, bitmap=wx.ArtProvider.GetBitmap('md5.account-child-circle', size=(24, 24)),
                                    size=(48, 48))
        self.bmp3 = wx.StaticBitmap(self,
                                    bitmap=_mbt_art_provider.GetBitmapEnhance('md5.account-child-circle', size=(24, 24),
                                                                              color='red'), size=(48, 48))
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
