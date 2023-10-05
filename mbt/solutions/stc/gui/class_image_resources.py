# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_image_resources.py
# ------------------------------------------------------------------------------
#
# File          : class_image_resources.py
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
from framework.gui.icon_repo.class_icon_repo import LocalIconRepoCategory
from mbt.gui.art_provider.class_art_provider import MBTArtProvider
from ..resources import THIS_IMAGE_PATH, THIS_XPMS_PATH


class STCEditorSideImageList(MappedImageList):
    _artNameList = [('pi.stack', 'history'),
                    ('pi.tree-structure', 'structure'),
                    ('pi.database', 'iod'),
                    ('pi.compass', 'minimap'),
                    ('pi.fingerprint', 'property'),
                    ('pi.gear', 'setting'),
                    ]

    def __init__(self, width=16, height=16, mask=True, initial_count=1):
        MappedImageList.__init__(self, width, height, mask, initial_count)

    def initialize(self):
        for art, name in self._artNameList:
            _idx = self.Add(wx.ArtProvider.GetBitmap(art, size=self.GetSize()))
            self.add_index_map(_idx, name)


_LOCAL_IMAGE_MAP = dict()
if not _LOCAL_IMAGE_MAP:
    _LOCAL_IMAGE_MAP = MBTArtProvider.gather_local_image_resources([THIS_XPMS_PATH], ['.xpm'])

LOCAL_XPM_IMAGE_REPO_CATEGORY = LocalIconRepoCategory(files=_LOCAL_IMAGE_MAP)
