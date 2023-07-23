# -*- coding: utf-8 -*-
import os

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
from pathlib import Path
from framework.gui.icon_repo.class_icon_repo import IconRepo, FontIconIconRepoCategory, LocalIconRepoCategory
from mbt.application.log.class_logger import get_logger

_log = get_logger('application.art_provider')


class MBTArtProvider(wx.ArtProvider):
    def __init__(self):
        wx.ArtProvider.__init__(self)
        self._localImagePaths = [os.path.join(os.path.dirname(__file__), 'arts')]
        _img_files = self.gather_local_image_resources(self._localImagePaths, ['.jpg', '.png', '.svg'])
        self.iconRepo = IconRepo()
        self.fontIconCategory = FontIconIconRepoCategory(name='fi')
        self.localIconCategory = LocalIconRepoCategory(name='local', files=_img_files)
        self.iconRepo.register(self.fontIconCategory)
        self.iconRepo.register(self.localIconCategory)

    def CreateBitmap(self, art_id: str, client=wx.ART_TOOLBAR, size=wx.Size(16, 16)):
        # You can do anything here you want, such as using the same
        # image for any size, any client, etc., or using specific
        # images for specific sizes, whatever...
        if art_id.startswith('wxART'):
            return super().CreateBitmap(art_id, client, size)
        if art_id.startswith('local.'):
            _cat=self.localIconCategory.name
            art_id = art_id.replace('local.', '')
        else:
            _cat=self.fontIconCategory.name
        # See end of file for the image data
        _bmp = wx.NullBitmap
        _bmp = self.iconRepo.get_bmp(category=_cat, name=art_id, size=size)
        if not _bmp.IsOk():
            _log.error("MBTArtProvider error: providing %s:%s at size %s failed.\n" % (art_id, client, size))
        return _bmp

    def GetBitmapEnhance(self, art_id: str, client=wx.ART_OTHER, size=wx.DefaultSize, **kwargs):
        if isinstance(size, tuple):
            size = wx.Size(*size)
        if art_id.startswith('wxART'):
            return super().CreateBitmap(art_id, client, size)
        if art_id.startswith('local.'):
            _cat=self.localIconCategory.name
            art_id=art_id.replace('local.','')
        else:
            _cat=self.fontIconCategory.name
        _bmp = self.iconRepo.get_bmp(category=_cat, name=art_id, size=size, **kwargs)
        if not _bmp.IsOk():
            print("MBTArtProvider error: providing %s:%s at size %s \n" % (art_id, client, size))
        return _bmp
    @staticmethod
    def gather_local_image_resources(dir_paths: list, valid_ext: list):
        _imgs = dict()
        for p in dir_paths:
            for x in os.listdir(p):
                _, _ext = os.path.splitext(x)
                if _ext.lower() not in valid_ext:
                    continue
                _k=Path(x).stem.lower()
                _imgs.update({_k: os.path.join(p,x)})
        return _imgs
