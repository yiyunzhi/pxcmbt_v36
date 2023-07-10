# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       :
# Sourcefile(s) : class_art_provider.py
# ------------------------------------------------------------------------------
#
# File          : class_art_provider.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx
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

    def GetBitmapEnhance(self, art_id: str, client=wx.ART_OTHER, size=wx.DefaultSize, **kwargs):
        if isinstance(size, tuple):
            size = wx.Size(*size)
        if art_id.startswith('wxART'):
            return super().CreateBitmap(art_id, client, size)
        _bmp = self.iconRepo.get_bmp(category=self.fontIconCategory.name, name=art_id, size=size, **kwargs)
        if not _bmp.IsOk():
            print("MBTArtProvider error: providing %s:%s at size %s \n" % (art_id, client, size))
        return _bmp
