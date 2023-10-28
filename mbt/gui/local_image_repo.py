# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : local_image_repo.py
# ------------------------------------------------------------------------------
#
# File          : local_image_repo.py
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
from framework.gui.base import MappedImageList
from framework.gui.wxgraph import WxShapeBase
from framework.gui.icon_repo.class_icon_repo import LocalIconRepoCategory
from mbt.gui.art_provider.class_art_provider import MBTArtProvider
from mbt.resources import XPMS_PATH, IMAGES_PATH


class MBTCodeItemImageList(MappedImageList):
    _artNameList = [('function', 'function'),
                    ('function_link', 'function_link'),
                    ('function_locked', 'function_locked'),
                    ('param', 'param'),
                    ('variable', 'variable'),
                    ('variable_link', 'variable_link'),
                    ('variable_locked', 'variable_locked')
                    ]

    def __init__(self, width=16, height=16, mask=True, initial_count=1):
        MappedImageList.__init__(self, width, height, mask, initial_count, default=wx.ART_LIST_VIEW)

    def initialize(self):
        _map = {v: k for k, v in self._artNameList}
        for art, name in _map.items():
            _bmp: wx.Bitmap = LOCAL_MODULE_XPM_IMAGE_REPO_CATEGORY.get_bmp(name=art)
            _idx = self.Add(_bmp)
            self.add_index_map(_idx, name)
        _bmp_default = wx.ArtProvider.GetBitmap(self.defaultArt, size=self.GetSize())
        if _bmp_default.IsOk():
            _idx = self.Add(_bmp_default)
            self.add_index_map(_idx, 'default')


class MBTModulePNGImageList(MappedImageList):
    _artNameList = [('back-left-arrow-square', 'iod_out'),
                    ('back-right-arrow-square', 'iod_in'),
                    ('left-right-arrows-square', 'iod_data'),
                    ('logo', 'logo'),
                    ('splash', 'splash'),
                    ]

    def __init__(self, width=16, height=16, mask=True, initial_count=1):
        MappedImageList.__init__(self, width, height, mask, initial_count, default=wx.ART_LIST_VIEW)

    def initialize(self):
        for art, name in self._artNameList:
            _bmp: wx.Bitmap = LOCAL_MODULE_PNG_IMAGE_REPO_CATEGORY.get_bmp(name=art)
            _idx = self.Add(_bmp)
            self.add_index_map(_idx, name)
        _bmp_default = wx.ArtProvider.GetBitmap(self.defaultArt, size=self.GetSize())
        if _bmp_default.IsOk():
            _idx = self.Add(_bmp_default)
            self.add_index_map(_idx, 'default')


def get_xpm_resources_icon(**kwargs):
    return LOCAL_MODULE_XPM_IMAGE_REPO_CATEGORY.get_bmp(**kwargs)


def get_png_image_resources_icon(**kwargs):
    return LOCAL_MODULE_PNG_IMAGE_REPO_CATEGORY.get_bmp(**kwargs)


_LOCAL_MODULE_XPM_IMAGE_MAP = dict()
_LOCAL_MODULE_PNG_IMAGE_MAP = dict()
if not _LOCAL_MODULE_XPM_IMAGE_MAP:
    _LOCAL_MODULE_XPM_IMAGE_MAP = MBTArtProvider.gather_local_image_resources([XPMS_PATH], ['.xpm'])
if not _LOCAL_MODULE_PNG_IMAGE_MAP:
    _LOCAL_MODULE_PNG_IMAGE_MAP = MBTArtProvider.gather_local_image_resources([IMAGES_PATH], ['.png'])

LOCAL_MODULE_XPM_IMAGE_REPO_CATEGORY = LocalIconRepoCategory(files=_LOCAL_MODULE_XPM_IMAGE_MAP)
LOCAL_MODULE_PNG_IMAGE_REPO_CATEGORY = LocalIconRepoCategory(files=_LOCAL_MODULE_PNG_IMAGE_MAP)
